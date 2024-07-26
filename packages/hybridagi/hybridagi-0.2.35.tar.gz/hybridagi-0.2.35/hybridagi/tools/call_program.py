"""The call program tool. Copyright (C) 2024 SynaLinks. License: GPL-3.0"""

import copy
import dspy
from .base import BaseTool
from typing import Optional, Callable
from ..hybridstores.program_memory.program_memory import ProgramMemory
from ..types.state import AgentState
from ..output_parsers.program_name import ProgramNameOutputParser
from ..output_parsers.prediction import PredictionOutputParser

class CallProgramSignature(dspy.Signature):
    """You will be given an objective, purpose and context
    Using the prompt to help you, you will infer the correct routine to select"""
    objective = dspy.InputField(desc = "The long-term objective (what you are doing)")
    context = dspy.InputField(desc = "The previous actions (what you have done)")
    purpose = dspy.InputField(desc = "The purpose of the action (what you have to do now)")
    prompt = dspy.InputField(desc = "The action specific instructions (How to do it)")
    selected_routine = dspy.OutputField(desc = "The name of the selected routine", prefix="Routine:")

class CallProgramTool(BaseTool):

    def __init__(
            self,
            program_memory: ProgramMemory,
            agent_state: AgentState,
            lm: Optional[dspy.LM] = None,
        ):
        super().__init__(name = "CallProgram", lm = lm)
        self.agent_state = agent_state
        self.program_memory = program_memory
        self.program_name_parser = ProgramNameOutputParser()
        self.prediction_parser = PredictionOutputParser()
        self.predict = dspy.Predict(CallProgramSignature)

    def call_program(self, program_name: str):
        """Method to call a program"""
        if not self.program_memory.exists(program_name):
            return "Error occured: This program does not exist, verify its name"
        if self.program_memory.is_protected(program_name):
            return "Error occured: Trying to call a protected program"
        current_program = self.agent_state.get_current_program()
        current_node = self.agent_state.get_current_node()
        next_node = self.program_memory.get_next_node(current_node, current_program)
        self.agent_state.set_current_node(next_node)
        called_program = self.program_memory.get_graph(program_name)
        first_node = self.program_memory.get_starting_node(program_name)
        self.agent_state.call_program(first_node, called_program)
        return "Successfully called"
        
    def forward(
            self,
            context: str,
            objective: str,
            purpose: str,
            prompt: str,
            disable_inference: bool = False,
        ) -> dspy.Prediction:
        """Method to perform DSPy forward prediction"""
        if not disable_inference:
            with dspy.context(lm=self.lm if self.lm is not None else dspy.settings.lm):
                pred = self.predict(
                    context = context,
                    objective = objective,
                    purpose = purpose,
                    prompt = prompt,
                )
            pred.selected_routine = self.prediction_parser.parse(
                pred.selected_routine, prefix="Routine:", stop=["\n", " "]
            )
            pred.selected_routine = self.program_name_parser.parse(pred.selected_routine)
            observation = self.call_program(pred.selected_routine)
            return dspy.Prediction(
                selected_routine = pred.selected_routine,
                observation = observation,
            )
        else:
            observation = self.call_program(prompt)
            return dspy.Prediction(
                selected_routine = prompt,
                observation = observation,
            )

    def __deepcopy__(self, memo):
        cpy = (type)(self)(
            program_memory = self.program_memory,
            agent_state = self.agent_state,
            lm = self.lm,
        )
        cpy.predict = copy.deepcopy(self.predict)
        return cpy