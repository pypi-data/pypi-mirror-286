from pydantic.v1 import ValidationError
import time
from pycardano import TransactionBody

from ogmios.client import Client
from ogmios.datatypes import Era

"""
This module contains helpful utilities for working with Ogmios.
"""


class GenesisParameters:
    """A class representing the genesis parameters of the blockchain. Each era has its own genesis
    configuration, whose parameters are additive to all previous eras. Therefore, to get the full set
    of genesis parameters, we need to query all eras up to the present and combine their parameters.

    :param latest_era: The latest era of the blockchain for which to compile genesis parameters
    :type latest_era: Era
    """

    def __init__(
        self,
        client: Client,
        latest_era: Era = Era.conway,
    ):
        # Query the genesis parameters for each era up to the latest era
        for i in range(len(Era)):
            era = Era.by_index(i)
            self.era = era.value
            try:
                genesis_parameters, _ = client.query_genesis_configuration.execute(era.value)

                # Unpack the genesis parameters into the class
                for key, value in genesis_parameters.__dict__.items():
                    setattr(self, key, value)
            except ValidationError:
                # Not all eras contain genesis parameters, so we can ignore the error
                pass

            if Era.by_index(i) == latest_era:
                break


def get_current_era(client: Client) -> Era:
    """
    Get the current era of the blockchain

    :param client: The Ogmios client object
    :type client: Client
    :return: The current era of the blockchain
    :rtype: Era
    """
    era_summaries, _ = client.query_era_summaries.execute()
    return Era.by_index(len(era_summaries) - 1)


def wait_for_empty_mempool(client: Client, timeout_s=60) -> None:
    """
    Wait for the mempool to be empty

    :param client: The Ogmios client object
    :type client: Client
    """
    start_time = time.time()
    while True:
        client.acquire_mempool.execute()
        tx, id = client.next_transaction.execute()
        client.release_mempool.execute()
        if tx is None:
            break
        if time.time() - start_time > timeout_s:
            raise TimeoutError("Mempool did not empty within the timeout period")
        time.sleep(1)


def get_mempool_transactions(client: Client) -> list:
    """
    Get the contents of the mempool

    :param client: The Ogmios client object
    :type client: Client
    :return: The contents of the mempool (list of transactions)
    :rtype: list
    """
    client.acquire_mempool.execute()
    mempool_txs = []
    while True:
        tx, id = client.next_transaction.execute()
        if tx is None:
            break
        mempool_txs.append(tx)
    client.release_mempool.execute()
    return mempool_txs


def tx_dict_to_pycardano_tx(tx_dict: dict) -> TransactionBody:
    """
    Convert a transaction dictionary to a PyCardano Transaction

    :param tx_dict: The transaction dictionary
    :type tx_dict: dict
    :return: The PyCardano Transaction
    :rtype: pyc.Transaction
    """
    return TransactionBody(tx_dict)
