# Copyright ©, 2022-present, Lightspark Group, Inc. - All Rights Reserved

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

from lightspark.exceptions import LightsparkException
from lightspark.requests.requester import Requester
from lightspark.utils.enums import parse_enum, parse_enum_optional

from .CurrencyAmount import CurrencyAmount
from .CurrencyAmount import from_json as CurrencyAmount_from_json
from .Entity import Entity
from .PaymentFailureReason import PaymentFailureReason
from .PaymentRequestData import from_json as PaymentRequestData_from_json
from .PostTransactionData import from_json as PostTransactionData_from_json
from .RichText import from_json as RichText_from_json
from .RoutingTransactionFailureReason import RoutingTransactionFailureReason
from .TransactionStatus import TransactionStatus


@dataclass
class Transaction(Entity):
    """This object represents a payment transaction. The transaction can occur either on a Bitcoin Network, or over the Lightning Network. You can retrieve this object to receive specific information about a particular transaction tied to your Lightspark Node."""

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
    typename: str

    def to_json(self) -> Mapping[str, Any]:
        return {
            "__typename": self.typename,
            "transaction_id": self.id,
            "transaction_created_at": self.created_at.isoformat(),
            "transaction_updated_at": self.updated_at.isoformat(),
            "transaction_status": self.status.value,
            "transaction_resolved_at": (
                self.resolved_at.isoformat() if self.resolved_at else None
            ),
            "transaction_amount": self.amount.to_json(),
            "transaction_transaction_hash": self.transaction_hash,
        }


FRAGMENT = """
fragment TransactionFragment on Transaction {
    __typename
    ... on ChannelClosingTransaction {
        __typename
        channel_closing_transaction_id: id
        channel_closing_transaction_created_at: created_at
        channel_closing_transaction_updated_at: updated_at
        channel_closing_transaction_status: status
        channel_closing_transaction_resolved_at: resolved_at
        channel_closing_transaction_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_closing_transaction_transaction_hash: transaction_hash
        channel_closing_transaction_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        channel_closing_transaction_block_hash: block_hash
        channel_closing_transaction_block_height: block_height
        channel_closing_transaction_destination_addresses: destination_addresses
        channel_closing_transaction_num_confirmations: num_confirmations
        channel_closing_transaction_channel: channel {
            id
        }
    }
    ... on ChannelOpeningTransaction {
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
    ... on Deposit {
        __typename
        deposit_id: id
        deposit_created_at: created_at
        deposit_updated_at: updated_at
        deposit_status: status
        deposit_resolved_at: resolved_at
        deposit_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        deposit_transaction_hash: transaction_hash
        deposit_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        deposit_block_hash: block_hash
        deposit_block_height: block_height
        deposit_destination_addresses: destination_addresses
        deposit_num_confirmations: num_confirmations
        deposit_destination: destination {
            id
        }
    }
    ... on IncomingPayment {
        __typename
        incoming_payment_id: id
        incoming_payment_created_at: created_at
        incoming_payment_updated_at: updated_at
        incoming_payment_status: status
        incoming_payment_resolved_at: resolved_at
        incoming_payment_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        incoming_payment_transaction_hash: transaction_hash
        incoming_payment_is_uma: is_uma
        incoming_payment_destination: destination {
            id
        }
        incoming_payment_payment_request: payment_request {
            id
        }
        incoming_payment_uma_post_transaction_data: uma_post_transaction_data {
            __typename
            post_transaction_data_utxo: utxo
            post_transaction_data_amount: amount {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
        }
        incoming_payment_is_internal_payment: is_internal_payment
    }
    ... on OutgoingPayment {
        __typename
        outgoing_payment_id: id
        outgoing_payment_created_at: created_at
        outgoing_payment_updated_at: updated_at
        outgoing_payment_status: status
        outgoing_payment_resolved_at: resolved_at
        outgoing_payment_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        outgoing_payment_transaction_hash: transaction_hash
        outgoing_payment_is_uma: is_uma
        outgoing_payment_origin: origin {
            id
        }
        outgoing_payment_destination: destination {
            id
        }
        outgoing_payment_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        outgoing_payment_payment_request_data: payment_request_data {
            __typename
            ... on InvoiceData {
                __typename
                invoice_data_encoded_payment_request: encoded_payment_request
                invoice_data_bitcoin_network: bitcoin_network
                invoice_data_payment_hash: payment_hash
                invoice_data_amount: amount {
                    __typename
                    currency_amount_original_value: original_value
                    currency_amount_original_unit: original_unit
                    currency_amount_preferred_currency_unit: preferred_currency_unit
                    currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                    currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                }
                invoice_data_created_at: created_at
                invoice_data_expires_at: expires_at
                invoice_data_memo: memo
                invoice_data_destination: destination {
                    __typename
                    ... on GraphNode {
                        __typename
                        graph_node_id: id
                        graph_node_created_at: created_at
                        graph_node_updated_at: updated_at
                        graph_node_alias: alias
                        graph_node_bitcoin_network: bitcoin_network
                        graph_node_color: color
                        graph_node_conductivity: conductivity
                        graph_node_display_name: display_name
                        graph_node_public_key: public_key
                    }
                    ... on LightsparkNodeWithOSK {
                        __typename
                        lightspark_node_with_o_s_k_id: id
                        lightspark_node_with_o_s_k_created_at: created_at
                        lightspark_node_with_o_s_k_updated_at: updated_at
                        lightspark_node_with_o_s_k_alias: alias
                        lightspark_node_with_o_s_k_bitcoin_network: bitcoin_network
                        lightspark_node_with_o_s_k_color: color
                        lightspark_node_with_o_s_k_conductivity: conductivity
                        lightspark_node_with_o_s_k_display_name: display_name
                        lightspark_node_with_o_s_k_public_key: public_key
                        lightspark_node_with_o_s_k_owner: owner {
                            id
                        }
                        lightspark_node_with_o_s_k_status: status
                        lightspark_node_with_o_s_k_total_balance: total_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_o_s_k_total_local_balance: total_local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_o_s_k_local_balance: local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_o_s_k_remote_balance: remote_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_o_s_k_blockchain_balance: blockchain_balance {
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
                        lightspark_node_with_o_s_k_uma_prescreening_utxos: uma_prescreening_utxos
                        lightspark_node_with_o_s_k_balances: balances {
                            __typename
                            balances_owned_balance: owned_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                            balances_available_to_send_balance: available_to_send_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                            balances_available_to_withdraw_balance: available_to_withdraw_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                        }
                        lightspark_node_with_o_s_k_encrypted_signing_private_key: encrypted_signing_private_key {
                            __typename
                            secret_encrypted_value: encrypted_value
                            secret_cipher: cipher
                        }
                    }
                    ... on LightsparkNodeWithRemoteSigning {
                        __typename
                        lightspark_node_with_remote_signing_id: id
                        lightspark_node_with_remote_signing_created_at: created_at
                        lightspark_node_with_remote_signing_updated_at: updated_at
                        lightspark_node_with_remote_signing_alias: alias
                        lightspark_node_with_remote_signing_bitcoin_network: bitcoin_network
                        lightspark_node_with_remote_signing_color: color
                        lightspark_node_with_remote_signing_conductivity: conductivity
                        lightspark_node_with_remote_signing_display_name: display_name
                        lightspark_node_with_remote_signing_public_key: public_key
                        lightspark_node_with_remote_signing_owner: owner {
                            id
                        }
                        lightspark_node_with_remote_signing_status: status
                        lightspark_node_with_remote_signing_total_balance: total_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_remote_signing_total_local_balance: total_local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_remote_signing_local_balance: local_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_remote_signing_remote_balance: remote_balance {
                            __typename
                            currency_amount_original_value: original_value
                            currency_amount_original_unit: original_unit
                            currency_amount_preferred_currency_unit: preferred_currency_unit
                            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                        }
                        lightspark_node_with_remote_signing_blockchain_balance: blockchain_balance {
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
                        lightspark_node_with_remote_signing_uma_prescreening_utxos: uma_prescreening_utxos
                        lightspark_node_with_remote_signing_balances: balances {
                            __typename
                            balances_owned_balance: owned_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                            balances_available_to_send_balance: available_to_send_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                            balances_available_to_withdraw_balance: available_to_withdraw_balance {
                                __typename
                                currency_amount_original_value: original_value
                                currency_amount_original_unit: original_unit
                                currency_amount_preferred_currency_unit: preferred_currency_unit
                                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
                            }
                        }
                    }
                }
            }
        }
        outgoing_payment_failure_reason: failure_reason
        outgoing_payment_failure_message: failure_message {
            __typename
            rich_text_text: text
        }
        outgoing_payment_uma_post_transaction_data: uma_post_transaction_data {
            __typename
            post_transaction_data_utxo: utxo
            post_transaction_data_amount: amount {
                __typename
                currency_amount_original_value: original_value
                currency_amount_original_unit: original_unit
                currency_amount_preferred_currency_unit: preferred_currency_unit
                currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
                currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
            }
        }
        outgoing_payment_payment_preimage: payment_preimage
        outgoing_payment_is_internal_payment: is_internal_payment
        outgoing_payment_idempotency_key: idempotency_key
    }
    ... on RoutingTransaction {
        __typename
        routing_transaction_id: id
        routing_transaction_created_at: created_at
        routing_transaction_updated_at: updated_at
        routing_transaction_status: status
        routing_transaction_resolved_at: resolved_at
        routing_transaction_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        routing_transaction_transaction_hash: transaction_hash
        routing_transaction_incoming_channel: incoming_channel {
            id
        }
        routing_transaction_outgoing_channel: outgoing_channel {
            id
        }
        routing_transaction_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        routing_transaction_failure_message: failure_message {
            __typename
            rich_text_text: text
        }
        routing_transaction_failure_reason: failure_reason
    }
    ... on Withdrawal {
        __typename
        withdrawal_id: id
        withdrawal_created_at: created_at
        withdrawal_updated_at: updated_at
        withdrawal_status: status
        withdrawal_resolved_at: resolved_at
        withdrawal_amount: amount {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        withdrawal_transaction_hash: transaction_hash
        withdrawal_fees: fees {
            __typename
            currency_amount_original_value: original_value
            currency_amount_original_unit: original_unit
            currency_amount_preferred_currency_unit: preferred_currency_unit
            currency_amount_preferred_currency_value_rounded: preferred_currency_value_rounded
            currency_amount_preferred_currency_value_approx: preferred_currency_value_approx
        }
        withdrawal_block_hash: block_hash
        withdrawal_block_height: block_height
        withdrawal_destination_addresses: destination_addresses
        withdrawal_num_confirmations: num_confirmations
        withdrawal_origin: origin {
            id
        }
    }
}
"""


def from_json(requester: Requester, obj: Mapping[str, Any]) -> Transaction:
    # pylint: disable=too-many-return-statements
    if obj["__typename"] == "ChannelClosingTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.ChannelClosingTransaction import (
            ChannelClosingTransaction,
        )

        return ChannelClosingTransaction(
            requester=requester,
            typename="ChannelClosingTransaction",
            id=obj["channel_closing_transaction_id"],
            created_at=datetime.fromisoformat(
                obj["channel_closing_transaction_created_at"]
            ),
            updated_at=datetime.fromisoformat(
                obj["channel_closing_transaction_updated_at"]
            ),
            status=parse_enum(
                TransactionStatus, obj["channel_closing_transaction_status"]
            ),
            resolved_at=(
                datetime.fromisoformat(obj["channel_closing_transaction_resolved_at"])
                if obj["channel_closing_transaction_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(
                requester, obj["channel_closing_transaction_amount"]
            ),
            transaction_hash=obj["channel_closing_transaction_transaction_hash"],
            fees=(
                CurrencyAmount_from_json(
                    requester, obj["channel_closing_transaction_fees"]
                )
                if obj["channel_closing_transaction_fees"]
                else None
            ),
            block_hash=obj["channel_closing_transaction_block_hash"],
            block_height=obj["channel_closing_transaction_block_height"],
            destination_addresses=obj[
                "channel_closing_transaction_destination_addresses"
            ],
            num_confirmations=obj["channel_closing_transaction_num_confirmations"],
            channel_id=(
                obj["channel_closing_transaction_channel"]["id"]
                if obj["channel_closing_transaction_channel"]
                else None
            ),
        )
    if obj["__typename"] == "ChannelOpeningTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.ChannelOpeningTransaction import (
            ChannelOpeningTransaction,
        )

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
            status=parse_enum(
                TransactionStatus, obj["channel_opening_transaction_status"]
            ),
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
                CurrencyAmount_from_json(
                    requester, obj["channel_opening_transaction_fees"]
                )
                if obj["channel_opening_transaction_fees"]
                else None
            ),
            block_hash=obj["channel_opening_transaction_block_hash"],
            block_height=obj["channel_opening_transaction_block_height"],
            destination_addresses=obj[
                "channel_opening_transaction_destination_addresses"
            ],
            num_confirmations=obj["channel_opening_transaction_num_confirmations"],
            channel_id=(
                obj["channel_opening_transaction_channel"]["id"]
                if obj["channel_opening_transaction_channel"]
                else None
            ),
        )
    if obj["__typename"] == "Deposit":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Deposit import Deposit

        return Deposit(
            requester=requester,
            typename="Deposit",
            id=obj["deposit_id"],
            created_at=datetime.fromisoformat(obj["deposit_created_at"]),
            updated_at=datetime.fromisoformat(obj["deposit_updated_at"]),
            status=parse_enum(TransactionStatus, obj["deposit_status"]),
            resolved_at=(
                datetime.fromisoformat(obj["deposit_resolved_at"])
                if obj["deposit_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(requester, obj["deposit_amount"]),
            transaction_hash=obj["deposit_transaction_hash"],
            fees=(
                CurrencyAmount_from_json(requester, obj["deposit_fees"])
                if obj["deposit_fees"]
                else None
            ),
            block_hash=obj["deposit_block_hash"],
            block_height=obj["deposit_block_height"],
            destination_addresses=obj["deposit_destination_addresses"],
            num_confirmations=obj["deposit_num_confirmations"],
            destination_id=obj["deposit_destination"]["id"],
        )
    if obj["__typename"] == "IncomingPayment":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.IncomingPayment import IncomingPayment

        return IncomingPayment(
            requester=requester,
            typename="IncomingPayment",
            id=obj["incoming_payment_id"],
            created_at=datetime.fromisoformat(obj["incoming_payment_created_at"]),
            updated_at=datetime.fromisoformat(obj["incoming_payment_updated_at"]),
            status=parse_enum(TransactionStatus, obj["incoming_payment_status"]),
            resolved_at=(
                datetime.fromisoformat(obj["incoming_payment_resolved_at"])
                if obj["incoming_payment_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(requester, obj["incoming_payment_amount"]),
            transaction_hash=obj["incoming_payment_transaction_hash"],
            is_uma=obj["incoming_payment_is_uma"],
            destination_id=obj["incoming_payment_destination"]["id"],
            payment_request_id=(
                obj["incoming_payment_payment_request"]["id"]
                if obj["incoming_payment_payment_request"]
                else None
            ),
            uma_post_transaction_data=(
                list(
                    map(
                        # pylint: disable=unnecessary-lambda
                        lambda e: PostTransactionData_from_json(requester, e),
                        obj["incoming_payment_uma_post_transaction_data"],
                    )
                )
                if obj["incoming_payment_uma_post_transaction_data"]
                else None
            ),
            is_internal_payment=obj["incoming_payment_is_internal_payment"],
        )
    if obj["__typename"] == "OutgoingPayment":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.OutgoingPayment import OutgoingPayment

        return OutgoingPayment(
            requester=requester,
            typename="OutgoingPayment",
            id=obj["outgoing_payment_id"],
            created_at=datetime.fromisoformat(obj["outgoing_payment_created_at"]),
            updated_at=datetime.fromisoformat(obj["outgoing_payment_updated_at"]),
            status=parse_enum(TransactionStatus, obj["outgoing_payment_status"]),
            resolved_at=(
                datetime.fromisoformat(obj["outgoing_payment_resolved_at"])
                if obj["outgoing_payment_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(requester, obj["outgoing_payment_amount"]),
            transaction_hash=obj["outgoing_payment_transaction_hash"],
            is_uma=obj["outgoing_payment_is_uma"],
            origin_id=obj["outgoing_payment_origin"]["id"],
            destination_id=(
                obj["outgoing_payment_destination"]["id"]
                if obj["outgoing_payment_destination"]
                else None
            ),
            fees=(
                CurrencyAmount_from_json(requester, obj["outgoing_payment_fees"])
                if obj["outgoing_payment_fees"]
                else None
            ),
            payment_request_data=(
                PaymentRequestData_from_json(
                    requester, obj["outgoing_payment_payment_request_data"]
                )
                if obj["outgoing_payment_payment_request_data"]
                else None
            ),
            failure_reason=parse_enum_optional(
                PaymentFailureReason, obj["outgoing_payment_failure_reason"]
            ),
            failure_message=(
                RichText_from_json(requester, obj["outgoing_payment_failure_message"])
                if obj["outgoing_payment_failure_message"]
                else None
            ),
            uma_post_transaction_data=(
                list(
                    map(
                        # pylint: disable=unnecessary-lambda
                        lambda e: PostTransactionData_from_json(requester, e),
                        obj["outgoing_payment_uma_post_transaction_data"],
                    )
                )
                if obj["outgoing_payment_uma_post_transaction_data"]
                else None
            ),
            payment_preimage=obj["outgoing_payment_payment_preimage"],
            is_internal_payment=obj["outgoing_payment_is_internal_payment"],
            idempotency_key=obj["outgoing_payment_idempotency_key"],
        )
    if obj["__typename"] == "RoutingTransaction":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.RoutingTransaction import RoutingTransaction

        return RoutingTransaction(
            requester=requester,
            typename="RoutingTransaction",
            id=obj["routing_transaction_id"],
            created_at=datetime.fromisoformat(obj["routing_transaction_created_at"]),
            updated_at=datetime.fromisoformat(obj["routing_transaction_updated_at"]),
            status=parse_enum(TransactionStatus, obj["routing_transaction_status"]),
            resolved_at=(
                datetime.fromisoformat(obj["routing_transaction_resolved_at"])
                if obj["routing_transaction_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(
                requester, obj["routing_transaction_amount"]
            ),
            transaction_hash=obj["routing_transaction_transaction_hash"],
            incoming_channel_id=(
                obj["routing_transaction_incoming_channel"]["id"]
                if obj["routing_transaction_incoming_channel"]
                else None
            ),
            outgoing_channel_id=(
                obj["routing_transaction_outgoing_channel"]["id"]
                if obj["routing_transaction_outgoing_channel"]
                else None
            ),
            fees=(
                CurrencyAmount_from_json(requester, obj["routing_transaction_fees"])
                if obj["routing_transaction_fees"]
                else None
            ),
            failure_message=(
                RichText_from_json(
                    requester, obj["routing_transaction_failure_message"]
                )
                if obj["routing_transaction_failure_message"]
                else None
            ),
            failure_reason=parse_enum_optional(
                RoutingTransactionFailureReason,
                obj["routing_transaction_failure_reason"],
            ),
        )
    if obj["__typename"] == "Withdrawal":
        # pylint: disable=import-outside-toplevel
        from lightspark.objects.Withdrawal import Withdrawal

        return Withdrawal(
            requester=requester,
            typename="Withdrawal",
            id=obj["withdrawal_id"],
            created_at=datetime.fromisoformat(obj["withdrawal_created_at"]),
            updated_at=datetime.fromisoformat(obj["withdrawal_updated_at"]),
            status=parse_enum(TransactionStatus, obj["withdrawal_status"]),
            resolved_at=(
                datetime.fromisoformat(obj["withdrawal_resolved_at"])
                if obj["withdrawal_resolved_at"]
                else None
            ),
            amount=CurrencyAmount_from_json(requester, obj["withdrawal_amount"]),
            transaction_hash=obj["withdrawal_transaction_hash"],
            fees=(
                CurrencyAmount_from_json(requester, obj["withdrawal_fees"])
                if obj["withdrawal_fees"]
                else None
            ),
            block_hash=obj["withdrawal_block_hash"],
            block_height=obj["withdrawal_block_height"],
            destination_addresses=obj["withdrawal_destination_addresses"],
            num_confirmations=obj["withdrawal_num_confirmations"],
            origin_id=obj["withdrawal_origin"]["id"],
        )
    graphql_typename = obj["__typename"]
    raise LightsparkException(
        "UNKNOWN_INTERFACE",
        f"Couldn't find a concrete type for interface Transaction corresponding to the typename={graphql_typename}",
    )
