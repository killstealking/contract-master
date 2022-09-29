from decimal import Decimal
from typing import Literal, Optional, Union

from pydantic import BaseModel


class TokenBalance(BaseModel):
    token: str
    balance: int
    decimals: int


class CommonServiceItem(BaseModel):
    type: Literal["common"] = "common"
    data: TokenBalance


class FarmingServiceItem(BaseModel):
    class FarmingServiceData(BaseModel):
        supply: list[TokenBalance]
        reward: list[TokenBalance]
        description: Optional[str] = None

    type: Literal["farming"] = "farming"
    data: FarmingServiceData


class StakedServiceItem(BaseModel):
    class StakedServiceData(BaseModel):
        supply: list[TokenBalance]
        reward: list[TokenBalance]
        description: Optional[str] = None

    type: Literal["staked"] = "staked"
    data: StakedServiceData


class LiquidityPoolServiceItem(BaseModel):
    class LiquidityPoolServiceData(BaseModel):
        supply: list[TokenBalance]
        description: Optional[str] = None

    type: Literal["liquidity pool"] = "liquidity pool"
    data: LiquidityPoolServiceData


class LendingServiceItem(BaseModel):
    class LendingServiceData(BaseModel):
        supply: list[TokenBalance]
        borrow: list[TokenBalance]
        reward: list[TokenBalance]
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
