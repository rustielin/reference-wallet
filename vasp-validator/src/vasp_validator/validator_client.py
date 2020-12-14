#  Copyright (c) The Diem Core Contributors
#  SPDX-License-Identifier: Apache-2.0

import logging
import random
import string
import time

from .lrw_proxy import LrwProxy
from .models import OffChainSequenceInfo, RegistrationStatus


class ValidatorClient:
    def __init__(self, lrw):
        self.lrw = lrw

    @classmethod
    def create(cls, lrw_url) -> "ValidatorClient":
        lrw = LrwProxy(lrw_url)

        user_name = f"gurkiAndBond@{get_random_string(8)}"
        password = get_random_string(12)

        # generate user and token in DB
        logging.info("create_new_user")
        lrw.create_new_user(user_name, password)

        logging.info("get_user")
        user = lrw.get_user()

        # generate account in DB
        logging.info("update_user")
        user = lrw.update_user(
            user,
            first_name=get_random_string(8),
            last_name=get_random_string(8),
        )

        num_of_retries = 20
        for i in range(num_of_retries):
            if user.registration_status == RegistrationStatus.Approved:
                break
            time.sleep(1)
            user = lrw.get_user()
        else:
            raise Exception("Filed to create an approved user")

        return cls(lrw)

    def get_receiving_address(self) -> str:
        return self.lrw.get_receiving_address()

    def knows_transaction(self, version):
        """
        Checks whether the transaction with the specified version is recognized by
        the validator as received by the current user.

        Note: Consider checking other transaction properties too;
        e.g., amount, currency etc.
        """
        num_of_retries = 5

        for i in range(num_of_retries):
            txs = self.lrw.get_transaction_list()
            if txs and version in [tx.blockchain_tx.version for tx in txs]:
                return True
            time.sleep(1)

        return False

    def get_offchain_state(self, reference_id) -> OffChainSequenceInfo:
        return self.lrw.get_offchain_state(reference_id)

    def kyc_abort(self):
        """
        Configure the validator that all the following off-chain travel rule
        sequences should fail the KYC check.
        """

    def kyc_manual_review(self):
        """
        Configure the validator that all the following off-chain travel rule
        sequences should stop pending KYC manual review.
        """


def get_random_string(length):
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))
