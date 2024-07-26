"""
Test the data level specification
"""
import pytest
import corgidrp.mocks as mocks
import corgidrp.l1_to_l2a as l1_to_l2a

def test_l1_to_l2a_good():
    """
    Tests a successful upgrade of L1 to L2a data. 
    """
    l1_dataset = mocks.create_prescan_files(obstype="SCI", numfiles=2)

    l2a_dataset = l1_to_l2a.update_to_l2a(l1_dataset)

    for frame in l2a_dataset:
        assert frame.ext_hdr['DATA_LEVEL'] == "L2a"


def test_l1_to_l2a_bad():
    """
    Tests an successful upgrade of L1 to L2a data because the input is not L1
    """
    l2a_dataset = mocks.create_dark_calib_files(numfiles=2)
    for frame in l2a_dataset:
        frame.ext_hdr['DATA_LEVEL'] = "L2a"
    
    # expect an exception
    with pytest.raises(ValueError):
        l2a_dataset_2 = l1_to_l2a.update_to_l2a(l2a_dataset)

if __name__ == "__main__":
    # test_l1_to_l2a_good()
    test_l1_to_l2a_bad()