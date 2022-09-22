from contract_master.bsc.internal import load_master_data


def test_load_master_data():
    data = load_master_data()
    assert len(data) > 0
