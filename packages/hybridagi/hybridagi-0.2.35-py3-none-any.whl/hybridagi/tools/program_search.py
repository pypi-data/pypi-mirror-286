"""The program search tool. Copyright (C) 2024 SynaLinks. License: GPL-3.0"""

import copy
import dspy
from .base import BaseTool
from typing import Optional
from ..embeddings.base import BaseEmbeddings
from ..hybridstores.program_memory.program_memory import ProgramMemory
from ..retrievers.program import ProgramRetriever
from ..output_parsers.prediction import PredictionOutputParser
from ..output_parsers.list_query import ListQueryOutputParser

class ProgramSearchSignature(dspy.Signature):
    """You will be given an objective, purpose and context
    Using the prompt to help you, you will infer the correct similarity search query"""
    objective = dspy.InputField(desc = "The long-term objective (what you are doing)")
    context = dspy.InputField(desc = "The previous actions (what you have done)")
    purpose = dspy.InputField(desc = "The purpose of the action (what you have to do now)")
    prompt = dspy.InputField(desc = "The action specific instructions (How to do it)")
    query = dspy.OutputField(desc = "The similarity search query (only few words)")

class ProgramSearchTool(BaseTool):

    def __init__(
            self,
            program_memory: ProgramMemory,
            embeddings: BaseEmbeddings,
            distance_threshold: float = 1.5,
            k: int = 5,
            lm: Optional[dspy.LM] = None,
        ):
        super().__init__(name = "ProgramSearch", lm = lm)
        self.predict = dspy.Predict(ProgramSearchSignature)
        self.program_memory = program_memory
        self.embeddings = embeddings
        self.distance_threshold = distance_threshold
        self.k = k
        self.retriever = ProgramRetriever(
            program_memory = program_memory,
            embeddings = embeddings,
            distance_threshold = self.distance_threshold,
            k = self.k,
        )
        self.prediction_parser = PredictionOutputParser()
        self.query_parser = ListQueryOutputParser()
    
    def forward(
            self,
            context: str,
            objective: str,
            purpose: str,
            prompt: str,
            disable_inference: bool = False,
            k: Optional[int] = None,
        ) -> dspy.Prediction:
        """Method to perform DSPy forward prediction"""
        if not disable_inference:
            with dspy.context(lm=self.lm if self.lm is not None else dspy.settings.lm):
                pred = self.predict(
                    objective = objective,
                    context = context,
                    purpose = purpose,
                    prompt = prompt,
                )
            pred.query = self.prediction_parser.parse(pred.query, prefix="Query:", stop=["\n"])
            query = self.query_parser.parse(pred.query)
            result = self.retriever(query)
            return dspy.Prediction(
                query = query,
                routines = result.routines,
            )
        else:
            result = self.retriever(prompt)
            return dspy.Prediction(
                query = prompt,
                routines = result.routines,
            )

    def __deepcopy__(self, memo):
        cpy = (type)(self)(
            program_memory = self.program_memory,
            embeddings = self.embeddings,
            distance_threshold = self.distance_threshold,
            k = self.k,
            lm = self.lm,
        )
        cpy.predict = copy.deepcopy(self.predict)
        return cpy