import csv
from typing import AnyStr

from pydantic import BaseModel


class MasterData(BaseModel):
    address: str
    type: str
    application: str
    service: str
    name: str


def load_master_data(csv_file_path: AnyStr) -> dict[str, MasterData]:
    with open(csv_file_path, "r", newline="") as csvfile:
        data = csv.DictReader(csvfile)
        data = map(MasterData.parse_obj, data)
        data = map(lambda x: (x.address, x), data)
        return dict(list(data))
