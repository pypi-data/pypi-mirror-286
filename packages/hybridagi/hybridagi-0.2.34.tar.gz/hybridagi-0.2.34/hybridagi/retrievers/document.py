"""The document retriever. Copyright (C) 2024 SynaLinks. License: GPL-3.0"""

import dspy
from typing import Union, Optional, List
from dsp.utils import dotdict
from ..embeddings.base import BaseEmbeddings
from ..hybridstores.filesystem.filesystem import FileSystem

class DocumentRetriever(dspy.Retrieve):
    """Retrieve document chunks based on similarity"""

    def __init__(
            self,
            filesystem: FileSystem,
            embeddings: BaseEmbeddings,
            distance_threshold: float = 1.2,
            k: int = 3,
        ):
        """The retriever constructor"""
        super().__init__(k = k)
        self.filesystem = filesystem
        self.embeddings = embeddings
        self.distance_threshold = distance_threshold

    def forward(
            self,
            query_or_queries: Union[str, List[str]],
            k:Optional[int] = None,
        ) -> dspy.Prediction:
        """Method to perform DSPy forward prediction"""
        if not isinstance(query_or_queries, list):
            query_or_queries = [query_or_queries]
        query_vectors = self.embeddings.embed_text(query_or_queries)
        contents = []
        indexes = {}
        for vector in query_vectors:
            # For an obscure reason falkordb needs a bigger k to find more indexed items
            params = {"indexed_label": self.filesystem.indexed_label, "vector": list(vector), "k": 2*int(k or self.k)}
            query = " ".join([
                'CALL db.idx.vector.queryNodes($indexed_label, "embeddings_vector", $k, vecf32($vector)) YIELD node, score',
                'RETURN node.name AS name, score'])
            result = self.filesystem.hybridstore.query(
                query,
                params = params,
            )
            if len(result.result_set) > 0:
                for record in result.result_set:
                    if record[0] not in indexes:
                        indexes[record[0]] = True
                    else:
                        continue
                    content = self.filesystem.get_content(record[0])
                    metadata = self.filesystem.get_content_metadata(record[0])
                    distance = float(record[1])
                    if distance < self.distance_threshold:
                        contents.extend([{"passage": dotdict({"long_text": content, "metadata": metadata}), "distance": distance}])
        sorted_passages = sorted(
            contents,
            key=lambda x: x["distance"],
            reverse=False,
        )[: k or self.k]
        return dspy.Prediction(
            passages=[el["passage"] for el in sorted_passages]
        )