from datetime import datetime
from decimal import Decimal

from lark import Token
from lark.visitors import Transformer


class LEDES1998BTransformer(Transformer):
    def ledes_1998b_file(self, children):
        return {k: v for d in children for k, v in d.items()}

    def ledes_spec(self, children):
        (ledes_spec,) = children or ("",)
        return {"ledes_version": ledes_spec}

    def LEDES1998B(self, t: Token):
        return str(t.value)

    def header_row(self, children):
        # The headers must be in a static order anyway, so we can skip walking down to each one if we know parsing succeeded.
        HEADERS = "INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID"
        return {"headers": HEADERS.split("|")}

    def line_items(self, children):
        return {"line_items": children}

    def line_item(self, children):
        return {k: v for d in children for k, v in d.items()}


class LineItemTransformer(Transformer):
    def __init__(self, visit_tokens: bool = True) -> None:
        self._date_format = "%Y%m%d"
        super().__init__(visit_tokens)

    def line_item(self, children):
        # TODO: Make a class per line item type, to enforce individual validation.
        # Each class gets a set of specifications. This method would return the constructor with **children as the kwargs.
        # In the constructor, all specifications that can run at the line item level, do.
        # Raises an error if invlalid - else, passes validation up the chain to the invoice level.
        # Ultimately validation is a chain of responsibility pattern going from ledes file -> fields for each line item -> line item -> invoice (maybe)
        return {k: v for d in children for k, v in d.items()}

    def exp_fee_inv_adj_type(self, children):
        (exp_fee_inv_adj_type,) = children or ("",)
        return {"exp_fee_inv_adj_type": exp_fee_inv_adj_type}

    def EXP_FEE_INV_ADJ_TYPE(self, children):
        return str(children)

    def FEE(self, t: Token):
        return str(t.value)

    def EXPENSE(self, t: Token):
        return str(t.value)

    def INVOICE_LEVEL_ADJUSTMENT_TO_FEES(self, t: Token):
        return str(t.value)

    def INVOICE_LEVEL_ADJUSTMENT_TO_EXPENSES(self, t: Token):
        return str(t.value)

    def invoice_date(self, children):
        (invoice_date,) = children or ("",)
        return {"invoice_date": invoice_date}

    def INVOICE_DATE(self, t: Token):
        return datetime.strptime(t.value, self._date_format).date()

    def billing_start_date(self, children):
        (billing_start_date,) = children or ("",)
        return {"billing_start_date": billing_start_date}

    def BILLING_START_DATE(self, t: Token):
        return datetime.strptime(t.value, self._date_format).date()

    def billing_end_date(self, children):
        (billing_end_date,) = children or ("",)
        return {"billing_end_date": billing_end_date}

    def BILLING_END_DATE(self, t: Token):
        return datetime.strptime(t.value, self._date_format).date()

    def line_item_date(self, children):
        (line_item_date,) = children or ("",)
        return {"line_item_date": line_item_date}

    def LINE_ITEM_DATE(self, t: Token):
        return datetime.strptime(t.value, self._date_format).date()

    def client_id(self, children):
        (client_id,) = children or ("",)
        return {"client_id": client_id}

    def CLIENT_ID(self, t: Token):
        return str(t.value)

    def law_firm_matter_id(self, children):
        (law_firm_matter_id,) = children or ("",)
        return {"law_firm_matter_id": law_firm_matter_id}

    def LAW_FIRM_MATTER_ID(self, t: Token):
        return str(t.value)

    def invoice_total(self, children):
        (invoice_total,) = children or ("",)
        return {"invoice_total": invoice_total}

    def INVOICE_TOTAL(self, t: Token):
        return Decimal(t.value)

    def client_matter_id(self, children):
        (client_matter_id,) = children or ("",)
        return {"client_matter_id": client_matter_id}

    def CLIENT_MATTER_ID(self, t: Token):
        return str(t.value)

    def invoice_description(self, children):
        (invoice_description,) = children or ("",)
        return {"invoice_description": invoice_description}

    def INVOICE_DESCRIPTION(self, t: Token):
        return str(t.value)

    def line_item_number(self, children):
        (line_item_number,) = children or ("",)
        return {"line_item_number": line_item_number}

    def LINE_ITEM_NUMBER(self, t: Token):
        return str(t.value)

    def invoice_number(self, children):
        (invoice_number,) = children or ("",)
        return {"invoice_number": invoice_number}

    def INVOICE_NUMBER(self, t: Token):
        return str(t.value)

    def timekeeper_classification(self, children):
        (timekeeper_classification,) = children or ("",)
        return {"timekeeper_classification": timekeeper_classification}

    def TIMEKEEPER_CLASSIFICATION(self, t: Token):
        return str(t.value)

    def timekeeper_name(self, children):
        (timekeeper_name,) = children or ("",)
        return {"timekeeper_name": timekeeper_name}

    def TIMEKEEPER_NAME(self, t: Token):
        return str(t.value)

    def line_item_task_code(self, children):
        (line_item_task_code,) = children or ("",)
        return {"line_item_task_code": line_item_task_code}

    def LINE_ITEM_TASK_CODE(self, t: Token):
        return str(t.value)

    def line_item_activity_code(self, children):
        (line_item_activity_code,) = children or ("",)
        return {"line_item_activity_code": line_item_activity_code}

    def LINE_ITEM_ACTIVITY_CODE(self, t: Token):
        return str(t.value)

    def timekeeper_id(self, children):
        (timekeeper_id,) = children or ("",)
        return {"timekeeper_id": timekeeper_id}

    def TIMEKEEPER_ID(self, t: Token):
        return str(t.value)

    def line_item_description(self, children):
        (line_item_description,) = children or ("",)
        return {"line_item_description": line_item_description}

    def LINE_ITEM_DESCRIPTION(self, t: Token):
        return str(t.value)

    def law_firm_id(self, children):
        (law_firm_id,) = children or ("",)
        return {"law_firm_id": law_firm_id}

    def LAW_FIRM_ID(self, t: Token):
        return str(t.value)

    def line_item_expense_code(self, children):
        (line_item_expense_code,) = children or ("",)
        return {"line_item_expense_code": line_item_expense_code}

    def LINE_ITEM_EXPENSE_CODE(self, t: Token):
        return str(t.value)

    def line_item_unit_cost(self, children):
        (line_item_unit_cost,) = children or ("",)
        return {"line_item_unit_cost": line_item_unit_cost}

    def LINE_ITEM_UNIT_COST(self, t: Token):
        return Decimal(t.value)

    def line_item_number_of_units(self, children):
        (line_item_number_of_units,) = children or ("",)
        return {"line_item_number_of_units": line_item_number_of_units}

    def LINE_ITEM_NUMBER_OF_UNITS(self, t: Token):
        return Decimal(t.value)

    def line_item_adjustment_amount(self, children):
        (line_item_adjustment_amount,) = children or ("",)
        return {"line_item_adjustment_amount": line_item_adjustment_amount}

    def LINE_ITEM_ADJUSTMENT_AMOUNT(self, t: Token):
        return Decimal(t.value)

    def line_item_total(self, children):
        (line_item_total,) = children or ("",)
        return {"line_item_total": line_item_total}

    def LINE_ITEM_TOTAL(self, t: Token):
        return Decimal(t.value)
