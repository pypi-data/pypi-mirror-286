# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from lightspark.requests.requester import Requester

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json


@dataclass
class ChannelFees:
    """This represents the fee policies set for a channel on the Lightning Network."""

    requester: Requester

    base_fee: Optional[CurrencyAmount]

    fee_rate_per_mil: Optional[int]

    def to_json(self) -> Mapping[str, Any]:
        return {
            "channel_fees_base_fee": self.base_fee.to_json() if self.base_fee else None,
            "channel_fees_fee_rate_per_mil": self.fee_rate_per_mil,
        }


FRAGMENT = """
fragment ChannelFeesFragment on ChannelFees {
    __typename
    channel_fees_base_fee: base_fee {
        __typename
        currency_amount_original_value: original_value
        currency_amount_original_unit: original_unit
        currency_amount_preferred_currency_unit: preferred_currency_unit
        currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
        currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
    }
    channel_fees_fee_rate_per_mil: fee_rate_per_mil
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> ChannelFees:
    return ChannelFees(
        requester=requester,
        base_fee=(
            CurrencyAmount_from_json(requester, obj["channel_fees_base_fee"])
            if obj["channel_fees_base_fee"]
            else None
        ),
        fee_rate_per_mil=obj["channel_fees_fee_rate_per_mil"],
    )
