# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): ErrorHandling, Exceptions; TECH(5): Python]
## @modulecontract
## @purpose To serve as the namespace package root for all dedoc exception classes, providing a single re-export surface for error types.
## @scope Error type namespace aggregation.
## @input None
## @output None (namespace package marker)
## @links [USES_API(8): dedoc.common.exceptions.*]
## @invariants
## - This is always a namespace package — no runtime logic.
## @rationale
## Q: Why does this file exist empty?
## A: Python requires __init__.py for package discovery in legacy namespace packages.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup added.]
## @modulemap
## PKG 2[Namespace package marker] => exceptions
## @usecases
## - [exceptions]: AnyModule → ImportExceptions → ErrorTypesAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: exceptions, errors, namespace, package, init, dedoc
# STRUCTURE: ▶ ┌exceptions package root┐ → ∅ (namespace marker)
