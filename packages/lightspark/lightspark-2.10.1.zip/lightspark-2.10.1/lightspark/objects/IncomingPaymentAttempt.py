# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .IncomingPaymentAttemptStatus import IncomingPaymentAttemptStatus


@dataclass
class IncomingPaymentAttempt(Entity):
    """This object represents any attempted payment sent to a Lightspark node on the Lightning Network. You can retrieve this object to receive payment related information about a specific incoming payment attempt."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when the entity was first created."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    status: IncomingPaymentAttemptStatus
    """The status of the incoming payment attempt."""

    resolved_at: Optional[datetime]
    """The time the incoming payment attempt failed or succeeded."""

    amount: CurrencyAmount
    """The total amount of that was attempted to send."""

    channel_id: str
    """The channel this attempt was made on."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "IncomingPaymentAttempt",
            "incoming_payment_attempt_id": self.id,
            "incoming_payment_attempt_created_at": self.created_at.isoformat(),
            "incoming_payment_attempt_updated_at": self.updated_at.isoformat(),
            "incoming_payment_attempt_status": self.status.value,
            "incoming_payment_attempt_resolved_at": (
                self.resolved_at.isoformat() if self.resolved_at else None
            ),
            "incoming_payment_attempt_amount": self.amount.to_json(),
            "incoming_payment_attempt_channel": {"id": self.channel_id},
        }


FRAGMENT = """
fragment IncomingPaymentAttemptFragment on IncomingPaymentAttempt {
    __typename
    incoming_payment_attempt_id: id
    incoming_payment_attempt_created_at: created_at
    incoming_payment_attempt_updated_at: updated_at
    incoming_payment_attempt_status: status
    incoming_payment_attempt_resolved_at: resolved_at
    incoming_payment_attempt_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    incoming_payment_attempt_channel: channel {
        id
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> IncomingPaymentAttempt:
    return IncomingPaymentAttempt(
        requester=requester,
        typename="IncomingPaymentAttempt",
        id=obj["incoming_payment_attempt_id"],
        created_at=datetime.fromisoformat(obj["incoming_payment_attempt_created_at"]),
        updated_at=datetime.fromisoformat(obj["incoming_payment_attempt_updated_at"]),
        status=parse_enum(
            IncomingPaymentAttemptStatus, obj["incoming_payment_attempt_status"]
        ),
        resolved_at=(
            datetime.fromisoformat(obj["incoming_payment_attempt_resolved_at"])
            if obj["incoming_payment_attempt_resolved_at"]
            else None
        ),
        amount=CurrencyAmount_from_json(
            requester, obj["incoming_payment_attempt_amount"]
        ),
        channel_id=obj["incoming_payment_attempt_channel"]["id"],
    )
