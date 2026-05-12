# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, StructureConstruction; CONCEPT(7): PackageInit, Exports; TECH(3): PythonImport]
## @modulecontract
## @purpose Provide a unified public API surface for the structure_constructors package, re-exporting all concrete and abstract structure constructors.
## @scope Package initialization, public symbol export.
## @input None (package-level init).
## @output __all__ list with exported class names.
## @links [USES_API(7): AbstractStructureConstructor, LinearConstructor, TreeConstructor, StructureConstructorComposition]
## @invariants
## - __all__ ALWAYS contains all 4 exported class names.
## @rationale
## Q: Why a separate init with explicit __all__?
## A: Explicit exports prevent namespace pollution and give agents a clear contract of what this package provides.
## @changes
## LAST_CHANGE: [v1.0.0 – Semantic template markup added]
## @modulemap
## CONST 5[Package public symbol list] => __all__
## @usecases
## - [__all__]: Agent (Import discovery) → ReadPackageAPI → KnowExportedSymbols
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: PackageInit, Exports, StructureConstructors, AbstractStructureConstructor, LinearConstructor, TreeConstructor, StructureConstructorComposition
# STRUCTURE: ▶ ┌submodules┐ → ⊕ __all__ = [AbstractStructureConstructor, LinearConstructor, TreeConstructor, StructureConstructorComposition]

from .abstract_structure_constructor import AbstractStructureConstructor
from .concrete_structure_constructors.linear_constructor import LinearConstructor
from .concrete_structure_constructors.tree_constructor import TreeConstructor
from .structure_constructor_composition import StructureConstructorComposition

__all__ = ['AbstractStructureConstructor', 'LinearConstructor', 'TreeConstructor', 'StructureConstructorComposition']
