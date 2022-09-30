from abc import ABC, abstractmethod

from pydantic.main import BaseModel

from .models import ServiceItem


class BalanceResult(BaseModel):
    """
    ContractMaster.get_balanceで資産取得が成功した場合の結果
    """

    application: str
    service: str
    item: ServiceItem


class IgnoredResult(BaseModel):
    """
    ContractMaster.get_balanceでトークンが対象外の場合の結果
    """

    token: str


class ContractMaster(ABC):
    MASTER_CSV_FILE_PATH: str

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_token_balance(
        self, contract_address: str, user_address: str, block_height: int | None = None
    ) -> BalanceResult | IgnoredResult:
        pass

    @abstractmethod
    def get_balance(
        self, contract_address: str, user_address: str, block_height: int | None = None
    ) -> BalanceResult | IgnoredResult:
        pass
