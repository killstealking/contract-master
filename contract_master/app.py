import argparse
import os
from typing import Any

from dotenv import load_dotenv
from pydantic.main import BaseModel

from contract_master.bsc.main import BscContractMaster

load_dotenv: Any
load_dotenv()


class Arguments(BaseModel):
    platform: str
    user_address: str
    contract_address: str
    block_height: int | None
    quicknode_endpoint: str


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--platform",
        help="--platfrom [platform]",
    )
    parser.add_argument("--contract_address", help="--contract_address [contract_address]")
    parser.add_argument("--user_address", help="--user_address [user_address]")
    parser.add_argument("--block_height", help="--block_height [block_height]")
    parser.add_argument("--quicknode_endpoint", help="--quicknode_endpoint [quicknode_endpoint]")
    args = parser.parse_args()

    return Arguments(
        platform=args.platform or "bsc",
        user_address=args.contract_address or "0xda28ecfc40181a6dad8b52723035dfba3386d26e",
        contract_address=args.contract_address or "0x0ed7e52944161450477ee417de9cd3a859b14fd0",
        block_height=args.block_height if args.block_height else None,
        quicknode_endpoint=args.quicknode_endpoint or os.getenv("QUICKNODE_BSC_ENDPOINT", ""),
    )


def validate_args(args: Arguments) -> None:
    if args.platform == "bsc" and args.quicknode_endpoint is None:
        raise Exception("No quicknode_endpoint")


if __name__ == "__main__":
    args = parse_args()
    validate_args(args)

    if args.platform == "bsc":
        contract_master = BscContractMaster(quicknode_endpoint=args.quicknode_endpoint)
        bep20_balance = contract_master.get_balance(
            contract_address=args.contract_address, user_address=args.user_address, block_height=args.block_height
        )
        print("bep20_balance : {}".format(bep20_balance))

    else:
        raise Exception(f"platform={args.platform} not supported")
