# region MODULE_CONTRACT [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @modulecontract
## @purpose Unit tests for module builders module.
## @scope Unit testing of dedoc module: module, builders.
## @input Test data files from tests/data/.
## @output Test results (pass/fail) with LDD telemetry.
## @links [USES_API(7): unittest.TestCase]
## @invariants
## - All original test logic and assertions remain unchanged.
## - LDD telemetry is printed BEFORE assertions.
## @rationale
## Q: Why add LDD telemetry to tests?
## A: On failure, critical log trajectory is visible before assert traceback.
## @changes
## LAST_CHANGE: [v1.0.0 – Added LDD telemetry and semantic markup.]
## @modulemap
## CLASS 8[Unit tests] => TestBuilders
## @usecases
## - [Tests]: QA Agent (Verify) => RunTestsWithTelemetry => DiagnosticTrajectoryVisible
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: module, builders, TestBuilders, test_creation_of_builders, unit_test, unittest, LDD_telemetry, semantic_markup, unit_test
# STRUCTURE: ▶ Init → ◇ Execute → ⊕ Verify → ∑ assertions → ⎋ PASS/FAIL


import logging

logger = logging.getLogger(__name__)

import unittest

from dedoc.structure_extractors.hierarchy_level_builders.header_builder.header_hierarchy_level_builder import HeaderHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.application_builder.application_foiv_hierarchy_level_builder import \
    ApplicationFoivHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.application_builder.application_law_hierarchy_level_builder import \
    ApplicationLawHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.body_foiv_hierarchy_level_builder import BodyFoivHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.body_builder.body_law_hierarchy_level_builder import BodyLawHierarchyLevelBuilder
from dedoc.structure_extractors.hierarchy_level_builders.law_builders.composition_hierarchy_level_builder import HierarchyLevelBuilderComposition


# region CLASS_TestBuilders [DOMAIN(7): Testing; CONCEPT(8): UnitTest, LDD_Telemetry; TECH(8): unittest, pytest]
## @purpose Test suite for module, builders module.
class TestBuilders(unittest.TestCase):
    builders = [
        HeaderHierarchyLevelBuilder(),
        BodyLawHierarchyLevelBuilder(),
        BodyFoivHierarchyLevelBuilder(),
        ApplicationLawHierarchyLevelBuilder(),
        ApplicationFoivHierarchyLevelBuilder()
    ]
    composition_builder = HierarchyLevelBuilderComposition(builders=builders)

    # region METHOD_test_creation_of_builders [DOMAIN(7): Testing; CONCEPT(8): LDD_Telemetry; TECH(8): unittest]
    ## @purpose Verify: creation of builders.
    ## @complexity 5
    def test_creation_of_builders(self) -> None:
        # LDD TELEMETRY: log execution context before assertions
        print(f"\n--- LDD TRAJECTORY (IMP:7-10) for TestBuilders::test_creation_of_builders ---")
        print(f"  [LDD_TEST][IMP:8][TestBuilders][test_creation_of_builders] Test logic executed, entering assertion phase")
        builders = self.composition_builder._get_builders(["header"], "law")
        self.assertTrue(isinstance(builders[0], HeaderHierarchyLevelBuilder))

        builders = self.composition_builder._get_builders(["header"], "foiv")
        self.assertTrue(isinstance(builders[0], HeaderHierarchyLevelBuilder))

        builders = self.composition_builder._get_builders(["application"], "law")
        self.assertTrue(isinstance(builders[0], ApplicationLawHierarchyLevelBuilder))

        builders = self.composition_builder._get_builders(["application"], "foiv")
        self.assertTrue(isinstance(builders[0], ApplicationFoivHierarchyLevelBuilder))

        builders = self.composition_builder._get_builders(["body"], "foiv")
        self.assertTrue(isinstance(builders[0], BodyFoivHierarchyLevelBuilder))

        builders = self.composition_builder._get_builders(["body"], "law")
        self.assertTrue(isinstance(builders[0], BodyLawHierarchyLevelBuilder))

    # endregion METHOD_test_creation_of_builders
# endregion CLASS_TestBuilders