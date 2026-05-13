from dedoc.data_structures.concrete_annotations.bold_annotation import BoldAnnotation
from dedoc.readers.pdf_reader.data_classes.page_with_bboxes import PageWithBBox
from dedoc.readers.pdf_reader.pdf_image_reader.line_metadata_extractor.bold_classifier.bold_classifier import BoldClassifier

import logging

logger = logging.getLogger(__name__)


# region CLASS_FontTypeClassifier [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader; TECH(6): Python]
class FontTypeClassifier:
    # region METHOD___init__ [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    def __init__(self) -> None:
        super().__init__()
        self.bold_classifier = BoldClassifier()

    # region METHOD_predict_annotations [DOMAIN(7): DocumentProcessing; CONCEPT(6): Method; TECH(6): Python]
    # endregion METHOD___init__
    def predict_annotations(self, page: PageWithBBox) -> PageWithBBox:
        if len(page.bboxes) == 0:
            return page

        bboxes = [word.bbox for line in page.bboxes for word in line.words]
        bold_probabilities = self.bold_classifier.classify(page.image, bboxes)

        bbox_id = 0
        for line in page.bboxes:
            current_text_len = 0

            for word in line.words:
                current_text_len = current_text_len + 1 if current_text_len > 0 else current_text_len  # add len of " " (space between words)
                extended_text_len = current_text_len + len(word.text)
                if bold_probabilities[bbox_id] > 0.5:
                    line.annotations.append(BoldAnnotation(start=current_text_len, end=extended_text_len, value="True"))
                current_text_len = extended_text_len
                bbox_id += 1

# endregion CLASS_FontTypeClassifier
        return page

    # endregion METHOD_predict_annotations


# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): Reader_font_type_classifier; TECH(6): Python, dedoc]
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
## CLASS [4][FontTypeClassifier reader/processor] => FontTypeClassifier
## @usecases
## - [read]: System (Pipeline) → ParseDocument(PDF) → UnstructuredDocument
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: font_type_classifier, dedoc, reader, PDF, PdfReader, BaseReader, PDF, pdfminer, tabby, OCR, tables, image, txtlayer, columns, orientation, paragraphs, metadata, extraction, line, bbox, FontTypeClassifier
# STRUCTURE: ▶ Init ┌PDF file┐ → [FontTypeClassifier] ○ can_read? → ○ read → [__init__ → predict_annotations] → ⊕ UnstructuredDocument(lines, tables, attachments)
