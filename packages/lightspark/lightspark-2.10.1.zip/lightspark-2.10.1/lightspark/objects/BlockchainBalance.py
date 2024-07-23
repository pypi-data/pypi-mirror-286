# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class BlockchainBalance:
    """This is an object representing a detailed breakdown of the balance for a Lightspark Node."""

    requester: Requester

    total_balance: Optional[CurrencyAmount]
    """The total wallet balance, including unconfirmed UTXOs."""

    confirmed_balance: Optional[CurrencyAmount]
    """The balance of confirmed UTXOs in the wallet."""

    unconfirmed_balance: Optional[CurrencyAmount]
    """The balance of unconfirmed UTXOs in the wallet."""

    locked_balance: Optional[CurrencyAmount]
    """The balance that's locked by an on-chain transaction."""

    required_reserve: Optional[CurrencyAmount]
    """Funds required to be held in reserve for channel bumping."""

    available_balance: Optional[CurrencyAmount]
    """Funds available for creating channels or withdrawing."""

    def to_json(self) -> Mapping[str, Any]:
        return {
            "blockchain_balance_total_balance": (
                self.total_balance.to_json() if self.total_balance else None
            ),
            "blockchain_balance_confirmed_balance": (
                self.confirmed_balance.to_json() if self.confirmed_balance else None
            ),
            "blockchain_balance_unconfirmed_balance": (
                self.unconfirmed_balance.to_json() if self.unconfirmed_balance else None
            ),
            "blockchain_balance_locked_balance": (
                self.locked_balance.to_json() if self.locked_balance else None
            ),
            "blockchain_balance_required_reserve": (
                self.required_reserve.to_json() if self.required_reserve else None
            ),
            "blockchain_balance_available_balance": (
                self.available_balance.to_json() if self.available_balance else None
            ),
        }


FRAGMENT = """
fragment BlockchainBalanceFragment on BlockchainBalance {
    __typename
    blockchain_balance_total_balance: total_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    blockchain_balance_confirmed_balance: confirmed_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    blockchain_balance_unconfirmed_balance: unconfirmed_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    blockchain_balance_locked_balance: locked_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    blockchain_balance_required_reserve: required_reserve {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    blockchain_balance_available_balance: available_balance {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> BlockchainBalance:
    return BlockchainBalance(
        requester=requester,
        total_balance=(
            CurrencyAmount_from_json(requester, obj["blockchain_balance_total_balance"])
            if obj["blockchain_balance_total_balance"]
            else None
        ),
        confirmed_balance=(
            CurrencyAmount_from_json(
                requester, obj["blockchain_balance_confirmed_balance"]
            )
            if obj["blockchain_balance_confirmed_balance"]
            else None
        ),
        unconfirmed_balance=(
            CurrencyAmount_from_json(
                requester, obj["blockchain_balance_unconfirmed_balance"]
            )
            if obj["blockchain_balance_unconfirmed_balance"]
            else None
        ),
        locked_balance=(
            CurrencyAmount_from_json(
                requester, obj["blockchain_balance_locked_balance"]
            )
            if obj["blockchain_balance_locked_balance"]
            else None
        ),
        required_reserve=(
            CurrencyAmount_from_json(
                requester, obj["blockchain_balance_required_reserve"]
            )
            if obj["blockchain_balance_required_reserve"]
            else None
        ),
        available_balance=(
            CurrencyAmount_from_json(
                requester, obj["blockchain_balance_available_balance"]
            )
            if obj["blockchain_balance_available_balance"]
            else None
        ),
    )
