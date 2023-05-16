import datetime as dt
import logging

import pandas as pd
import stripe
import xlwings as xw
from fastapi import APIRouter, Body, Security

from .. import settings
from ..core.auth import User, authenticate

# Require authentication for all endpoints for this router
router = APIRouter(
    dependencies=[Security(authenticate)],
    prefix="/stripe",
    tags=["Stripe"],
)

logger = logging.getLogger(__name__)


@router.post("/dashboard")
def dashboard(data: dict = Body, current_user: User = Security(authenticate)):
    # Spreadsheet objects
    with xw.Book(json=data) as book:
        sheet = book.sheets["Dashboard"]
        overview_cell = sheet["overview"]
        details_cell = sheet["details"]

        # Clear existing data
        overview_cell.expand().clear_contents()
        details_cell.expand().clear_contents()

        # Query Stripe for outstanding invoices
        logger.info(f"Running stripe query for {current_user.email}")
        stripe.api_key = settings.stripe_api_key
        invoices = stripe.Invoice.list(status="open", limit=100)

        if not invoices.data:
            sheet["overview"].offset(row_offset=1).value = "N/A"
            sheet["details"].offset(row_offset=1).value = "N/A"
            return book.json()

        # Get all invoices from the paginated Stripe response as DataFrame
        data = []
        for invoice in invoices.auto_paging_iter():
            data.append(invoice)
        invoices = pd.DataFrame(data)

        # Data cleaning/wrangling
        invoices = invoices[
            [
                "id",
                "customer_name",
                "currency",
                "amount_due",
                "attempted",
                "due_date",
            ]
        ]
        invoices = invoices.sort_values("due_date")
        invoices = invoices.set_index("id")
        invoices["due_date"] = pd.to_datetime(invoices["due_date"], unit="s").dt.date
        invoices["Due in (days)"] = (invoices["due_date"] - dt.date.today()).dt.days
        invoices["amount_due"] /= 100
        invoices["customer_name"] = (
            '=HYPERLINK("'
            + "https://dashboard.stripe.com/invoices/"
            + invoices.index
            + '", "'
            + invoices["customer_name"]
            + '")'
        )
        invoices["currency"] = invoices["currency"].str.upper()

        invoices = invoices.rename(
            columns={
                "currency": "Currency",
                "amount_due": "Amount Due",
                "customer_name": "Customer",
                "attempted": "Attempted to Pay",
                "due_date": "Due Date",
            }
        )

        invoices_overview = invoices[["Currency", "Amount Due"]].groupby("Currency").sum()

        # Write results to the sheet
        overview_cell.value = invoices_overview
        details_cell.options(index=False).value = invoices
        sheet["last_updated"].value = dt.datetime.now(dt.timezone.utc)

        return book.json()
