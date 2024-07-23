# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from enum import Enum


class PaymentFailureReason(Enum):
    """This is an enum of the potential reasons why an OutgoingPayment sent from a Lightspark Node may have failed."""

    ___FUTURE_VALUE___ = "___FUTURE_VALUE___"
    """This is an enum value that represents future values that could be added in the future. Clients should support unknown values as more of them could be added without notice."""
    NONE = "NONE"
    TIMEOUT = "TIMEOUT"
    NO_ROUTE = "NO_ROUTE"
    ERROR = "ERROR"
    INCORRECT_PAYMENT_DETAILS = "INCORRECT_PAYMENT_DETAILS"
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    INVOICE_ALREADY_PAID = "INVOICE_ALREADY_PAID"
    SELF_PAYMENT = "SELF_PAYMENT"
    INVOICE_EXPIRED = "INVOICE_EXPIRED"
    INVOICE_CANCELLED = "INVOICE_CANCELLED"
    RISK_SCREENING_FAILED = "RISK_SCREENING_FAILED"
    INSUFFICIENT_BALANCE_ON_SINGLE_PATH_INVOICE = (
        "INSUFFICIENT_BALANCE_ON_SINGLE_PATH_INVOICE"
    )
