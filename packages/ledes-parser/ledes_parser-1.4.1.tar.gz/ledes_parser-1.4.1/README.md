# ledes-parser
A package for parsing LEDES format files.

## Warning
This is very much a work in progress. DO NOT RELY ON THIS FOR YOUR LEGAL INVOICING.

## Installation

To install the package, run:

```bash
pip install ledes-parser
```
# Example Usage
The default transformer maps the ledes file into a simple python dict.

```python
from ledes_parser import get_parser

raw_ledes_text = """
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|2|F|2.00|0|700|19990115|L510||A102|22547|Research attorney's fees, Trial pleading|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
"""

parser = get_parser(spec="1998B")
result = parser.parse(raw_ledes_text)
import pprint
pprint.pprint(result)
```

If you prefer to create and use a custom transformer, you can set `ast_only=True` to have the parser return only the abstract syntax tree.
```python
from ledes_parser import get_parser

with open('path/to/the/ledes_file.txt', 'r') as f:
    raw_ledes_text = f.read()

parser = get_parser(spec="1998B", ast_only=True)
result = parser.parse(raw_ledes_text)
print(result.pretty())
```

# LEDES File Formats
This package supports parsing the following LEDES file formats:

* LEDES1998B
* (TBD) LEDES1998BI
* (TBD) LEDES1998BIV2
* (TBD) LEDES2000
* (TBD) LEDESXML20
* (TBD) LEDESXML21

# Contributing
Fork the repository on GitHub.
Create a new branch with your changes.
Commit your changes and push them to your fork.
Create a pull request against the main branch of the original repository.
