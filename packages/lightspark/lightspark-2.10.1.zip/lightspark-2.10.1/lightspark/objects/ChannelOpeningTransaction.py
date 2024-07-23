# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping, Optional

from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .OnChainTransaction import OnChainTransaction
from .Transaction import Transaction
from .TransactionStatus import TransactionStatus


@dataclass
class ChannelOpeningTransaction(OnChainTransaction, Transaction, Entity):
    """This is an object representing a transaction which opens a channel on the Lightning Network. This object occurs only for channels funded by the local Lightspark node."""

    requester: Requester

    id: str
    """The unique identifier of this entity across all Lightspark systems. Should be treated as an opaque string."""

    created_at: datetime
    """The date and time when this transaction was initiated."""

    updated_at: datetime
    """The date and time when the entity was last updated."""

    status: TransactionStatus
    """The current status of this transaction."""

    resolved_at: Optional[datetime]
    """The date and time when this transaction was completed or failed."""

    amount: CurrencyAmount
    """The amount of money involved in this transaction."""

    transaction_hash: Optional[str]
    """The hash of this transaction, so it can be uniquely identified on the Lightning Network."""

    fees: Optional[CurrencyAmount]
    """The fees that were paid by the node for this transaction."""

    block_hash: Optional[str]
    """The hash of the block that included this transaction. This will be null for unconfirmed transactions."""

    block_height: int
    """The height of the block that included this transaction. This will be zero for unconfirmed transactions."""

    destination_addresses: List[str]
    """The Bitcoin blockchain addresses this transaction was sent to."""

    num_confirmations: Optional[int]
    """The number of blockchain confirmations for this transaction in real time."""

    channel_id: Optional[str]
    """If known, the channel this transaction is opening."""
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": "ChannelOpeningTransaction",
            "channel_opening_transaction_id": self.id,
            "channel_opening_transaction_created_at": self.created_at.isoformat(),
            "channel_opening_transaction_updated_at": self.updated_at.isoformat(),
            "channel_opening_transaction_status": self.status.value,
            "channel_opening_transaction_resolved_at": (
                self.resolved_at.isoformat() if self.resolved_at else None
            ),
            "channel_opening_transaction_amount": self.amount.to_json(),
            "channel_opening_transaction_transaction_hash": self.transaction_hash,
            "channel_opening_transaction_fees": (
                self.fees.to_json() if self.fees else None
            ),
            "channel_opening_transaction_block_hash": self.block_hash,
            "channel_opening_transaction_block_height": self.block_height,
            "channel_opening_transaction_destination_addresses": self.destination_addresses,
            "channel_opening_transaction_num_confirmations": self.num_confirmations,
            "channel_opening_transaction_channel": (
                {"id": self.channel_id} if self.channel_id else None
            ),
        }


FRAGMENT = """
fragment ChannelOpeningTransactionFragment on ChannelOpeningTransaction {
    __typename
    channel_opening_transaction_id: id
    channel_opening_transaction_created_at: created_at
    channel_opening_transaction_updated_at: updated_at
    channel_opening_transaction_status: status
    channel_opening_transaction_resolved_at: resolved_at
    channel_opening_transaction_amount: amount {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_opening_transaction_transaction_hash: transaction_hash
    channel_opening_transaction_fees: fees {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_opening_transaction_block_hash: block_hash
    channel_opening_transaction_block_height: block_height
    channel_opening_transaction_destination_addresses: destination_addresses
    channel_opening_transaction_num_confirmations: num_confirmations
    channel_opening_transaction_channel: channel {
        id
    }
}
"""


def from_json(
    requester: Requester, obj: Mapping[str, Any]
) -> ChannelOpeningTransaction:
    return ChannelOpeningTransaction(
        requester=requester,
        typename="ChannelOpeningTransaction",
        id=obj["channel_opening_transaction_id"],
        created_at=datetime.fromisoformat(
            obj["channel_opening_transaction_created_at"]
        ),
        updated_at=datetime.fromisoformat(
            obj["channel_opening_transaction_updated_at"]
        ),
        status=parse_enum(TransactionStatus, obj["channel_opening_transaction_status"]),
        resolved_at=(
            datetime.fromisoformat(obj["channel_opening_transaction_resolved_at"])
            if obj["channel_opening_transaction_resolved_at"]
            else None
        ),
        amount=CurrencyAmount_from_json(
            requester, obj["channel_opening_transaction_amount"]
        ),
        transaction_hash=obj["channel_opening_transaction_transaction_hash"],
        fees=(
            CurrencyAmount_from_json(requester, obj["channel_opening_transaction_fees"])
            if obj["channel_opening_transaction_fees"]
            else None
        ),
        block_hash=obj["channel_opening_transaction_block_hash"],
        block_height=obj["channel_opening_transaction_block_height"],
        destination_addresses=obj["channel_opening_transaction_destination_addresses"],
        num_confirmations=obj["channel_opening_transaction_num_confirmations"],
        channel_id=(
            obj["channel_opening_transaction_channel"]["id"]
            if obj["channel_opening_transaction_channel"]
            else None
        ),
    )
