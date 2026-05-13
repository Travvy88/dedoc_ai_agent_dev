# ======================================================================
# SEMANTIC TEMPLATE REFERENCE (ONE-SHOT EXAMPLE FOR AGENTS)
# Этот файл — эталон формата разметки. При обработке других файлов
# следуй ровно этому формату. Не отклоняйся.
# ======================================================================
# region MODULE_CONTRACT [DOMAIN(X): DomainName; CONCEPT(Y): ConceptName; TECH(Z): TechName]
## @modulecontract
## @purpose [Describe the GOAL of the module — what business/operational need it fulfills.]
## @scope [Main functional areas covered by the module.]
## @input [Module-wide input data.]
## @output [What the module provides to the rest of the system.]
## @links [USES_API(X): ...; READS_DATA_FROM(Y): ...]
## @links_to_spec [Technical requirements points, if applicable]
## @invariants
## - [Condition/State that always holds]
## @rationale
## Q: [Why was it implemented this way?]
## A: [Justification, environmental constraints.]
## @changes
## LAST_CHANGE: [Current version - Brief description of latest changes]
## @modulemap
## FUNC/CLASS [Weight 1-10][Entity description] => [entity_name]
## @usecases
## - [Entity]: [Actor] => [Action] => [Goal]
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: [Comma-separated keywords for grep search]
# STRUCTURE: [Creative one-line mini block diagram]

import logging

logger = logging.getLogger(__name__)

# region CLASS_ExampleClass [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
## @purpose [Goal of the class — what it enables the user/agent to do.]
class ExampleClass:
    # region METHOD_example_method [DOMAIN(X): ...; ...]
    ## @purpose [Goal of the method.]
    ## @uses [APIs or modules used]
    ## @io [Input types] -> [Output types]
    ## @complexity [1-10]
    def example_method(self, param1: int) -> str:
        # LDD-log: flow start
        logger.debug(f"[IMP:4][ExampleClass][INIT] Starting with param1={param1}")
        result = str(param1 * 2)
        # LDD-log: business result
        logger.info(f"[IMP:9][ExampleClass][RESULT] Computed result={result}")
        return result
    # endregion METHOD_example_method
# endregion CLASS_ExampleClass

# region FUNC_example_function [DOMAIN(X): ...; CONCEPT(Y): ...; TECH(Z): ...]
## @purpose [Describe the GOAL of this function.]
## @uses [APIs or modules used]
## @io [Input types] -> [Output types]
## @complexity [1-10]
def example_function(data: list) -> int:
    # LDD-log: initialization
    logger.debug(f"[IMP:4][example_function][INIT] Input data length={len(data)}")

    total = 0
    for item in data:
        total += item
        logger.debug(f"[IMP:3][example_function][LOOP] item={item}, running_total={total}")

    # LDD-log: business result
    logger.info(f"[IMP:9][example_function][RESULT] Sum computed: {total}")
    return total
# endregion FUNC_example_function
