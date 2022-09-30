from decimal import Decimal
from typing import Literal, Optional, Union

from pydantic import BaseModel


class TokenAmount(BaseModel):
    uti: str
    amount: str
    original_id: str
    balance: int
    decimals: int
    symbol: str


class CommonServiceItem(BaseModel):
    type: Literal["common"] = "common"
    data: TokenAmount


class FarmingServiceItem(BaseModel):
    class FarmingServiceData(BaseModel):
        supply: list[TokenAmount]
        reward: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["farming"] = "farming"
    data: FarmingServiceData


class StakedServiceItem(BaseModel):
    class StakedServiceData(BaseModel):
        supply: list[TokenAmount]
        reward: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["staked"] = "staked"
    data: StakedServiceData


class LiquidityPoolServiceItem(BaseModel):
    class LiquidityPoolServiceData(BaseModel):
        supply: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["liquidity pool"] = "liquidity pool"
    data: LiquidityPoolServiceData


class LendingServiceItem(BaseModel):
    class LendingServiceData(BaseModel):
        supply: list[TokenAmount]
        borrow: list[TokenAmount]
        reward: list[TokenAmount]
        health_rate: Optional[Decimal] = None

    type: Literal["lending"] = "lending"
    data: LendingServiceData


ServiceItem = Union[
    CommonServiceItem,
    FarmingServiceItem,
    StakedServiceItem,
    LendingServiceItem,
    LiquidityPoolServiceItem,
]
