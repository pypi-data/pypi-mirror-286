import datetime
from pydantic import BaseModel


class Sales(BaseModel):
    concept: list[str]
    sales_date: list[datetime.date]
    expiration: list[datetime.date]
    status: list[str]
    sales_credit: list[bool]
    customer: list[str]
    prod_serv: list[str]
    amount: list[float]
    paid: list[float]
    unit_price: list[float]
    bank_account: list[str]
    way_pay: list[str]
    sector: list[str]
    invoice_folio: list[float]
    date_issue: list[datetime.date]
    final_price: list[float]
    discount: list[float]
    income: list[float]
    product_cost: list[float]
