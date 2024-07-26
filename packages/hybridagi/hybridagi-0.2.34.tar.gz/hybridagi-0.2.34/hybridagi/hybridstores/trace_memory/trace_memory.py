"""The trace memory. Copyright (C) 2023 SynaLinks. License: GPL-3.0"""

import uuid
import json
from typing import Union, List
from ...types.actions import AgentAction, AgentDecision, ProgramCall, ProgramEnd
from ...embeddings.base import BaseEmbeddings
from ..hybridstore import HybridStore

class TraceMemory(HybridStore):
    """The trace memory"""

    def __init__(
            self,
            index_name: str,
            embeddings: BaseEmbeddings,
            graph_index: str = "trace_memory",
            hostname: int = "localhost",
            port: int = 6379,
            username: str = "",
            password: str = "",
            indexed_label: str = "Content",
            wipe_on_start: bool = False,
            ):
        super().__init__(
            index_name = index_name,
            graph_index = graph_index,
            embeddings = embeddings,
            hostname = hostname,
            port = port,
            username = username,
            password = password,
            indexed_label = indexed_label,
            wipe_on_start = wipe_on_start,
        )
        self.current_commit = None

    def commit(
            self,
            step: Union[
                AgentAction,
                AgentDecision,
                ProgramCall,
                ProgramEnd,
            ]
        ) -> str:
        new_commit = ""
        content_index = ""
        if isinstance(step, AgentAction):
            new_commit = str(uuid.uuid4().hex)
            # avoid recursive recall by not indexing the past action search
            if step.prediction and step.tool != "PastActionSearch":
                prediction = json.dumps(dict(step.prediction), indent=2)
                indexes = self.add_texts(texts = [prediction])
                content_index = indexes[0]
            else:
                if step.tool == "PastActionSearch":
                    prediction = json.dumps(dict(step.prediction), indent=2)
                else:
                    prediction = "None"
            params = {
                "index" : new_commit,
                "hop" : step.hop,
                "objective" : step.objective,
                "purpose" : step.purpose,
                "tool" : step.tool,
                "prompt" : step.prompt,
                "prediction" : prediction,
                "log" : step.log,
            }
            self.hybridstore.query(
                'MERGE (:Action {name:$index, '+
                'hop:$hop, objective:$objective, '+
                'purpose:$purpose, '+
                'tool:$tool, '+
                'prompt:$prompt, '+
                'prediction:$prediction, '+
                'log:$log})',
                params = params,
            )
            if content_index:
                params = {
                    "commit_index" : new_commit,
                    "content_index": content_index,
                }
                self.hybridstore.query(
                    "MATCH (a:Action {name:$commit_index}), "+
                    "(c:"+self.indexed_label+" {name:$content_index}) MERGE (a)-[:CONTAINS]->(c)",
                    params = params,
                )
        elif isinstance(step, AgentDecision):
            new_commit = str(uuid.uuid4().hex)
            params = {
                "index" : new_commit,
                "hop" : step.hop,
                "objective" : step.objective,
                "purpose" : step.purpose,
                "question" : step.question,
                "options" : step.options,
                "answer" : step.answer,
                "log" : step.log,
            }
            self.hybridstore.query(
                'MERGE (:Decision {name:$index, '+
                'hop:$hop, objective:$objective, '+
                'purpose:$purpose, '+
                'question:$question, '+
                'answer:$answer, '+
                'log:$log})',
                params = params,
            )
        elif isinstance(step, ProgramCall):
            new_commit = str(uuid.uuid4().hex)
            params = {
                "index": new_commit,
                "program": step.program,
                "purpose": step.purpose,
            }
            self.hybridstore.query(
                'MERGE (:ProgramCall {name:$index,'+
                ' program:$program, purpose:$purpose})',
                params = params,
            )
        elif isinstance(step, ProgramEnd):
            new_commit = str(uuid.uuid4().hex)
            params = {"index": new_commit, "program": step.program}
            self.hybridstore.query(
                'MERGE (:ProgramEnd {name:$index, '+
                'program:$program})',
                params = params,
            )
        else:
            raise ValueError("Invalid step provided, could not commit to memory")
        params = {"current": self.current_commit, "new": new_commit}
        if self.current_commit:
            self.hybridstore.query(
                'MATCH (n {name:$current}), '+
                '(m {name:$new}) MERGE (n)-[:NEXT]->(m)',
                params = params,
            )
        self.current_commit = new_commit
        return new_commit if not content_index else content_index

    def start_new_trace(self):
        """Start a new trace"""
        self.current_commit = None

    def get_trace_indexes(
            self,
        ) -> List[str]:
        """Get the traces indexes (the first commit index of each trace)"""
        trace_indexes = []
        result = self.hybridstore.query('MATCH (n:ProgramCall {program:"main"}) RETURN n.name as name')
        for record in result.result_set:
            trace_indexes.append(record[0])
        return trace_indexes

    def is_finished(
            self,
            trace_index: str,
        ) -> bool:
        """Returns True if the execution of the program terminated"""
        params = {"index": trace_index}
        result = self.query(
            'MATCH (n:ProgramCall {name:$index, program:"main"})'
            +'-[:NEXT*]->(m:EndProgram {program:"main"}) RETURN m',
            params = params,
        )
        if len(result.result_set) == 0:
            return False
        return True