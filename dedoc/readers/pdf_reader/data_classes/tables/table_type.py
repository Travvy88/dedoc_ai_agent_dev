# region CLASS_TableTypeAdditionalOptions [DOMAIN(7): DocumentProcessing; CONCEPT(8): TableType, TableRecognition; TECH(6): Python]
## @purpose Define the enumeration of table recognition strategies for the PDF image table recognizer — controls which table detection algorithms are active.
## @uses None (pure data class)
## @io None -> None (constructor sets instance attributes)
## @complexity 2
class TableTypeAdditionalOptions:
    """
    Enum for table types of tables for the table recognizer.
    The value of the parameter specifies the type of tables recognized when processed by
    class :class:`~dedoc.readers.pdf_reader.pdf_image_reader.table_recognizer.table_recognizer.TableRecognizer`.

    * Parameter `table_type=wo_external_bounds` - recognize tables without external bounds.

    Example of a table of type `wo_external_bounds`::

       text   | text | text
      --------+------+------
       text   | text | text
      --------+------+------
       text   | text | text
      --------+------+------
       text   | text | text


    * Parameter `table_type=one_cell_table` - if a document contains a bounding box with text, it will be considered a table.

    Example of a page with a table of type `one_cell_table`::

         _________________________
         Header of document
         text text text +------+
         text           | text |  <--- it is a table
                        +------+
         ________________________

    * Parameter `table_type=split_last_column` - specified parameter for the merged last column of the table.

    Example of a table of type `split_last_column`::

         +--------+------+-------+
         | text   | text | text1 |
         +--------+------+       |
         | text0  | text | text2 |
         |        | -----|       |
         |        | text | text3 |
         +--------+------+       |
         | text   | text | text4 |
         +--------+------+-------+
                     |
                 Recognition
                    |
                    V
         +--------+------+-------+
         | text   | text | text1 |
         +--------+------+-------|
         | text0  | text | text2 |
         |--------+ -----+------ |
         | text0  | text | text3 |
         +--------+------+------ |
         | text   | text | text4 |
         +--------+------+-------+

    """
    # region METHOD___init__ [DOMAIN(7): TableRecognition; CONCEPT(6): Initialization; TECH(5): Python]
    ## @purpose Initialize table type configuration constants.
    ## @complexity 1
    def __init__(self) -> None:
        # LDD-log: initialization
        self.table_wo_external_bounds = "wo_external_bounds"
        self.detect_one_cell_table = "one_cell_table"
        self.split_last_column = "split_last_column"
    # endregion METHOD___init__
# endregion CLASS_TableTypeAdditionalOptions

# region MODULE_CONTRACT [DOMAIN(7): DocumentProcessing; CONCEPT(8): TableRecognition, TableType; TECH(6): Python]
## @modulecontract
## @purpose Define the enumeration of table recognition strategies (wo_external_bounds, one_cell_table, split_last_column) used by the PDF image table recognizer.
## @scope Table type configuration for the TableRecognizer subsystem.
## @input None (configuration class instantiated on demand).
## @output TableTypeAdditionalOptions instance with strategy flags.
## @links [USES_API(8): dedoc.readers.pdf_reader.pdf_image_reader.table_recognizer.TableRecognizer]
## @invariants
## - TableTypeAdditionalOptions ALWAYS provides three strategy flags.
## @rationale
## Q: Why class with string constants instead of Python Enum?
## A: Maintains backward compatibility with existing parameter passing via string values.
## @changes
## LAST_CHANGE: [v1.0.0 – Added SEMANTIC TEMPLATE markup and LDD logging.]
## @modulemap
## CLASS [8][Table recognition strategy enumerator] => TableTypeAdditionalOptions
## @usecases
## - [TableTypeAdditionalOptions]: TableRecognizer (Configure) → SelectStrategy → RecognitionModeActive
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: table_type, TableTypeAdditionalOptions, table_recognition, wo_external_bounds, one_cell_table, split_last_column, PDF, dedoc, reader
# STRUCTURE: ▶ TableTypeAdditionalOptions ∋ {wo_external_bounds, one_cell_table, split_last_column} → ○ TableRecognizer selects strategy → ⊕ recognized table
