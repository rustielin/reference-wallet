#  Copyright (c) The Diem Core Contributors
#  SPDX-License-Identifier: Apache-2.0

import os
import random
import string
from time import sleep

from vasp_validator.models import TransactionStatus
from vasp_validator.lrw_proxy import LrwProxy
from vasp_validator.vasp_proxy import VaspProxy, TxState, TxStatus

# TBD: Configure properly
LOCAL_LRW_URL = os.getenv("LOCAL_URL", "http://localhost:8080/api")


class VaspProxyTestee(VaspProxy):
    def __init__(self):
        self.lrw = LrwProxy(LOCAL_LRW_URL)

    def send_transaction(self, address, amount, currency) -> TxState:
        self.create_user()
        self.add_funds_to_local_account()

        # TBD: LRW should return the offchain refid, if applicable
        tx = self.lrw.send_transaction(address, amount, currency)

        retries_count = 10
        for i in range(retries_count):
            tx = self.lrw.get_transaction(tx.id)
            if tx.status != TransactionStatus.PENDING:
                break
            sleep(1)
        else:
            return TxState(
                status=TxStatus.PENDING,
                status_description="Timeout waiting for pending transaction",
                offchain_refid=tx.offchain_refid,
            )

        if tx.status != TransactionStatus.COMPLETED:
            return TxState(
                status=TxStatus.FAILED,
                status_description=f"Send transaction was not successful ({tx.status})",
                offchain_refid=tx.offchain_refid,
            )

        return TxState(
            onchain_version=tx.blockchain_tx.version,
            offchain_refid=tx.offchain_refid,
        )

    def get_offchain_state(self, reference_id):
        return {}

    def add_funds_to_local_account(self):
        amount = 900_000_000
        currency = "Coin1"

        quote_id = self.lrw.create_deposit_quote(amount, "Coin1_USD").quote_id
        self.lrw.execute_quote(quote_id)

        if not self.wait_for_balance(amount, currency):
            raise Exception("Failed to add funds to account")

    def wait_for_balance(self, amount, currency):
        retries_count = 10
        for i in range(retries_count):
            if self.lrw.get_balance(currency) >= amount:
                return True
            sleep(1)

        return False

    def create_user(self):
        user_name = f"bondAndGurki@{get_random_string(8)}"
        password = get_random_string(12)

        self.lrw.create_new_user(user_name, password)
        user = self.lrw.get_user()
        self.lrw.update_user(user)


def get_random_string(length):
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))
