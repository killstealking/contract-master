from os import path
from typing import Type

from web3 import Web3

from ..common import (
    BalanceResult,
    Contract,
    ContractMaster,
    ErroredResult,
    IgnoredResult,
    load_master_data,
)
from .contract import (
    Bep20TokenContract,
    PancakeIFO,
    PancakeLiquidityPool,
    PancakeStaking,
    PancakeVault,
)


class BscContractMaster(ContractMaster):
    MASTER_CSV_FILE_PATH = path.join(path.dirname(__file__), "./master.csv")

    def __init__(self, quicknode_endpoint: str):
        self.master = load_master_data(BscContractMaster.MASTER_CSV_FILE_PATH)
        self.web3 = Web3(Web3.HTTPProvider(quicknode_endpoint))
        if not self.web3.isConnected():
            raise Exception("QuickNodeConnectionError")

    def get_token_balance(
        self, contract_address: str, user_address: str, block_height: int | None = None
    ) -> BalanceResult | ErroredResult:
        try:
            return BalanceResult(
                application="bsc",
                service="spot",
                item=Bep20TokenContract(web3=self.web3, address=contract_address).balance_of(
                    account=user_address, block_height=block_height
                ),
            )
        except Exception as e:
            return ErroredResult(token=contract_address, reason=str(e))

    def get_balance(
        self, contract_address: str, user_address: str, block_height: int | None = None
    ) -> BalanceResult | IgnoredResult | ErroredResult:
        contract: Type[Contract]
        master = self.master.get(contract_address, None)
        if master is None:
            return ErroredResult(token=contract_address, reason=f"UndefinedAddress: {contract_address}")

        match master.type:
            case "pancake_ifo":
                contract = PancakeIFO
            case "pancake_lp":
                contract = PancakeLiquidityPool
            case "pancake_staking":
                contract = PancakeStaking
            case "pancake_vault":
                contract = PancakeVault
            case "ignored":
                return IgnoredResult(token=contract_address)
            case _:
                return ErroredResult(token=contract_address, reason=f"UnsupportedType: {contract_address}")

        try:
            return BalanceResult(
                application=master.application,
                service=master.service,
                item=contract(web3=self.web3, address=contract_address).balance_of(
                    account=user_address, block_height=block_height
                ),
            )
        except Exception as e:
            return ErroredResult(token=contract_address, reason=str(e))
