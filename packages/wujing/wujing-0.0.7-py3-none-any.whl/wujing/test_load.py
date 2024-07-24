from wujing.load import load_dataset


def test_load_dataset():
    assert 1 == len(load_dataset("./testdata/person_info_1.json"))
    assert 1 == len(load_dataset("./testdata/person_info_2.json"))
    assert 3 == len(load_dataset("./testdata/person_info.xlsx"))
    assert 1 == len(load_dataset("./testdata/person_info_gbk.csv"))
    assert 6 == len(load_dataset("./testdata/person_info_1.json", "./testdata/person_info_2.json", "./testdata/person_info.xlsx", "./testdata/person_info_gbk.csv"))
