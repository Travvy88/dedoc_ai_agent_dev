# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(6): CommonUtilities, ErrorHandling; TECH(5): Python]
## @modulecontract
## @purpose To serve as the root package for common dedoc utilities, errors, and shared infrastructure used across all processing modules.
## @scope Package namespace initialization, shared exception re-export surface.
## @input None
## @output None (namespace package marker)
## @links [READS_DATA_FROM(8): dedoc.common.exceptions]
## @invariants
## - This is always a namespace package — no runtime logic.
## @rationale
## Q: Why does this file exist empty?
## A: Python requires __init__.py for package discovery in legacy namespace packages.
## @changes
## LAST_CHANGE: [v1.0.0 — Semantic template markup added.]
## @modulemap
## PKG 2[Namespace package marker] => common
## @usecases
## - [common]: AnyModule → ImportCommon → SharedUtilitiesAvailable
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: common, namespace, package, init, dedoc
# STRUCTURE: ▶ ┌common package root┐ → ∅ (namespace marker)
