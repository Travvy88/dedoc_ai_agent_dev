# region MODULE_CONTRACT [DOMAIN(Testing): LDD; CONCEPT(Tests): TestRunner; TECH(Python): Unittest]
## @modulecontract
## @purpose To provide a custom unittest runner that numbers test cases during execution, improving readability of LDD test output for agent log analysis.
## @scope Test result formatting and test runner customisation.
## @input unittest test suite.
## @output Numbered, formatted test result output to stream.
## @links [USES_API(8): unittest.runner; USES_API(5): itertools]
## @invariants
## - Test numbers are sequential starting from 1.
## - Test numbering is only active when showAll (verbosity >= 2) is set.
## @rationale
## Q: Why custom test runner instead of pytest?
## A: unittest runner integrates directly with LDD log output format; numbering helps agents map log lines to specific test cases.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## CLASS 8[Numbered test result stream writer] => CustomTextTestResult
## CLASS 7[Numbered test runner entry point] => CustomTextTestRunner
## @usecases
## - CustomTextTestRunner: LDDTestSuite → RunWithNumbering → FormattedStreamOutput
## - CustomTextTestResult: TestCase → AssignNumber → LogPrefixInjection
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: custom test runner, unittest, test numbering, LDD, test result formatting, stream output
# STRUCTURE: ▶ Init ┌custom_test_runner┐ → ○ CustomTextTestResult.cls ∋ itertools.count → ⊕ startTest(numbering) → ○ CustomTextTestRunner.run → ⎋ formatted output

import itertools
import unittest.runner


class CustomTextTestResult(unittest.runner.TextTestResult):
    """Extension of TextTestResult to support numbering test cases"""

    def __init__(self, stream, descriptions, verbosity):
        """Initializes the test number generator, then calls super impl"""

        self.test_numbers = itertools.count(1)

        return super(CustomTextTestResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        """Writes the test number to the stream if showAll is set, then calls super impl"""

        if self.showAll:
            test_numbers = next(self.test_numbers)
            test_case_count = self.test_case_count
            progress = f"[{test_numbers}/{test_case_count}] "
            self.stream.write(progress)

            # Also store the progress in the test itself, so that if it errors,
            # it can be written to the exception information by our overridden
            # _exec_info_to_string method:
            test.progress_index = progress

        return super(CustomTextTestResult, self).startTest(test)

    def _exc_info_to_string(self, err, test):
        """Gets an exception info string from super, and prepends 'Test Number' line"""

        info = super(CustomTextTestResult, self)._exc_info_to_string(err, test)

        if self.showAll:
            index = test.progress_index
            test_info = info
            info = f"Test number: {index}\n{test_info}"

        return info


class CustomTextTestRunner(unittest.runner.TextTestRunner):
    """Extension of TextTestRunner to support numbering test cases"""

    resultclass = CustomTextTestResult

    def run(self, test):
        """Stores the total count of test cases, then calls super impl"""

        self.test_case_count = test.countTestCases()
        return super(CustomTextTestRunner, self).run(test)

    def _makeResult(self):
        """Creates and returns a result instance that knows the count of test cases"""

        result = super(CustomTextTestRunner, self)._makeResult()
        result.test_case_count = self.test_case_count
        return result
