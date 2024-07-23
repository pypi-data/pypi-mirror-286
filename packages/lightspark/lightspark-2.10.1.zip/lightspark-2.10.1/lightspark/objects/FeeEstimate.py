# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class FeeEstimate:
    """This object represents the estimated L1 transaction fees for the Bitcoin network. Fee estimates are separated by potential confirmation speeds for settlement."""

    requester: Requester

    fee_fast: CurrencyAmount

    fee_min: CurrencyAmount

    def to_json(self) -> Mapping[str, Any]:
        return {
            "fee_estimate_fee_fast": self.fee_fast.to_json(),
            "fee_estimate_fee_min": self.fee_min.to_json(),
        }


FRAGMENT = """
fragment FeeEstimateFragment on FeeEstimate {
    __typename
    fee_estimate_fee_fast: fee_fast {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    fee_estimate_fee_min: fee_min {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> FeeEstimate:
    return FeeEstimate(
        requester=requester,
        fee_fast=CurrencyAmount_from_json(requester, obj["fee_estimate_fee_fast"]),
        fee_min=CurrencyAmount_from_json(requester, obj["fee_estimate_fee_min"]),
    )
