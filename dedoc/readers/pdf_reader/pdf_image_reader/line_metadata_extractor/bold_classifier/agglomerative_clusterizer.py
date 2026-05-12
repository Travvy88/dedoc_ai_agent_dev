import numpy as np
from scipy.stats import norm
from sklearn.cluster import AgglomerativeClustering

import logging

logger = logging.getLogger(__name__)


# region CLASS_BoldAgglomerativeClusterizer [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class BoldAgglomerativeClusterizer:
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        self.significance_level = 0.2

    # region METHOD_clusterize [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def clusterize(self, x: np.ndarray) -> np.ndarray:
        x_vectors = self.__get_prop_vectors(x)
        x_clusters = self.__get_clusters(x_vectors)
        x_indicator = self.__get_indicator(x, x_clusters)
        return x_indicator

    # region METHOD___get_prop_vectors [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD_clusterize
    def __get_prop_vectors(self, x: np.ndarray) -> np.ndarray:
        nearby_x = x.copy()
        nearby_x[:-1] += x[1:]
        nearby_x[1:] += x[:-1]
        nearby_x[0] += x[0]
        nearby_x[-1] += x[-1]
        nearby_x = nearby_x / 3.
        return np.stack((x, nearby_x), 1)

    # region METHOD___get_clusters [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_prop_vectors
    def __get_clusters(self, x_vectors: np.ndarray) -> np.ndarray:
        agg = AgglomerativeClustering()
        agg.fit(x_vectors)
        x_clusters = agg.labels_
        return x_clusters

    # region METHOD___get_indicator [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_clusters
    def __get_indicator(self, x: np.ndarray, x_clusters: np.ndarray) -> np.ndarray:
        # https://www.tsi.lv/sites/default/files/editor/science/Research_journals/Tr_Tel/2003/V1/yatskiv_gousarova.pdf
        # https://www.svms.org/classification/DuHS95.pdf
        # Pattern Classification and Scene Analysis (2nd ed.)
        # Part 1: Pattern Classification
        # Richard O. Duda, Peter E. Hart and David G. Stork
        # February 27, 1995
        f1 = self.__get_f1_homogeneous(x, x_clusters)
        f_cr = self.__get_f_criterion_homogeneous(n=len(x))

        if f_cr < f1:
            return np.zeros_like(x)
        if np.mean(x[x_clusters == 1]) < np.mean(x[x_clusters == 0]):
            x_clusters[x_clusters == 1] = 1.0
            x_clusters[x_clusters == 0] = 0.0
        else:
            x_clusters[x_clusters == 0] = 1.0
            x_clusters[x_clusters == 1] = 0.0

        return x_clusters

    # region METHOD___get_f1_homogeneous [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_indicator
    def __get_f1_homogeneous(self, x: np.ndarray, x_clusters: np.ndarray) -> float:
        x_clust0 = x[x_clusters == 0]
        x_clust1 = x[x_clusters == 1]
        if len(x_clust0) == 0 or len(x_clust1) == 0:
            return 1

        w1 = np.std(x) * len(x)
        w2 = np.std(x_clust0) * len(x_clust0) + np.std(x_clust1) * len(x_clust1)
        f1 = w2 / w1 if w1 != 0. else 0.
        return f1

    # region METHOD___get_f_criterion_homogeneous [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___get_f1_homogeneous
    def __get_f_criterion_homogeneous(self, n: int, p: int = 2) -> float:
        za1 = norm.ppf(1 - self.significance_level, loc=0, scale=1)
        f_cr = 1 - 2 / (np.pi * p) - za1 * np.sqrt(2 * (1 - 8 / (np.pi ** 2 * p)) / (n * p))
# endregion CLASS_BoldAgglomerativeClusterizer
        return f_cr

    # endregion METHOD___get_f_criterion_homogeneous


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_agglomerative_clusterizer; TECH(6): Python, dedoc]
## @modulecontract
## @purpose Read and parse PDF documents, extracting lines with metadata, tables, and attachments into UnstructuredDocument.
## @scope Machine learning classification for document layout analysis.
## @input [File path (str), parameters (Optional[dict]) — document on disk.]
## @output [UnstructuredDocument with lines, tables, attachments, and warnings.]
## @links [USES_API(9): dedoc.data_structures.*; USES_API(8): dedoc.readers.BaseReader]
## @invariants
## - read() ALWAYS returns an UnstructuredDocument.
## @rationale
## Q: Why is this reader separated from others?
## A: Each reader handles one format family — isolation prevents format coupling and simplifies extension.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [14][BoldAgglomerativeClusterizer reader/processor] => BoldAgglomerativeClusterizer
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: agglomerative_clusterizer, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, BoldAgglomerativeClusterizer
# STRUCTURE: ▶ Init ┌PDF file┐ → [BoldAgglomerativeClusterizer] ○ can_read? → ○ read → [__init__ → clusterize → __get_prop_vectors] → ⊕ UnstructuredDocument(lines, tables, attachments)
