# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing; CONCEPT(7): AttachmentHandling; TECH(3): PythonPackage]
## @modulecontract
## @purpose Expose the AttachmentsHandler class as the public API entry point for attachment processing orchestration.
## @scope Package initialization and public symbol re-export.
## @input None
## @output Public symbol AttachmentsHandler
## @links [USES_API(9): AttachmentsHandler]
## @invariants
## - __all__ ALWAYS contains "AttachmentsHandler".
## @rationale
## Q: Why a separate attachments_handler package?
## A: Attachment handling is an independent orchestration layer decoupled from individual extractors.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic markup added]
## @modulemap
## CLASS 10[Handles attachment processing orchestration] => AttachmentsHandler
## @usecases
## - [AttachmentsHandler]: DedocManager => OrchestrateAttachmentParsing => ParsedDocumentList
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: attachments, handler, orchestration, AttachmentsHandler, package_init
# STRUCTURE: ▶ Import AttachmentsHandler → ○ __all__ = ["AttachmentsHandler"] → ⎋

from .attachments_handler import AttachmentsHandler

__all__ = ["AttachmentsHandler"]
