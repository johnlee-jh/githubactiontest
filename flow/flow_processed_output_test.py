"""Contains test cases for flow_processed_output.py.

Classes:
    testDetectorIdToRoadSections: Test cases for DetectorIdToRoadSections.
    testOutputFlowDataSet: Test cases for OutputFlowDataSet.
    create_DITRS_Dataset: Class to randomly generate DetectorIdToRoadSections.
    create_OFDS_Dataset: Class to randomly generate OutputFlowDataSet.

To run all test cases, use the following command:
    >>> python3 flow_processed_output_test.py
"""

#this is a comment that flake8 would NOT like! (no space after hashtag)
#woot23dfasdasdfasdfasd
#yeetmode1234

import datetime
import flow_processed_output
import os
import pickle
import random
from typing import List
import unittest
import warnings


class testDetectorIdToRoadSections(unittest.TestCase):
    """Test the export_to_file() and _import_from_file() methods of
    the DetectorIdToRoadSections() class in flow_processed_output.py.

    This is done by checking that exporting and importing the same
    DetectorIdToRoadSections object maintains equality with the original copy.
    Errors such as exporting empty DetectorIdToRoadSections and importing from
    wrong files are tested by checking that Exceptions or Warnings are
    appropriately raised.
    """
    def test_DITRS_export_create_file(self):
        """Verify whether export_to_file() creates a new file."""
        filepath = '1.txt'
        ditrs = flow_processed_output.DetectorIdToRoadSections()
        ditrs.aimsun_detector_locations = create_DITRS_Dataset(1).dataset
        ditrs.export_to_file(filepath)
        # Check if file was created at filepath
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_DITRS_import_equals_export(self):
        """Verify that export_to_file() and _import_to_file() will
        return the same values."""
        filepath = '2.txt'
        original_ditrs = flow_processed_output.DetectorIdToRoadSections()
        original_ditrs.aimsun_detector_locations = (
                                            create_DITRS_Dataset(10).dataset)
        original_ditrs.export_to_file(filepath)
        # Import using constructor
        new_ditrs = flow_processed_output.DetectorIdToRoadSections(filepath)
        os.remove(filepath)
        # Check if new_ditrs contains the same attributes as the original_ditrs
        self.assertTrue(new_ditrs == original_ditrs)
        # Check if new_ditrs is not equal to a different ditrs of same size
        different_ditrs = flow_processed_output.DetectorIdToRoadSections()
        different_ditrs.aimsun_detector_locations = (
                                            create_DITRS_Dataset(10).dataset)
        self.assertFalse(new_ditrs == different_ditrs)

    def test_DITRS_export_existing_file(self):
        """Verify that export_to_file() raises a warning if a file
        already exists at given filepath."""
        filepath = '3.txt'
        existing_file = open(filepath, 'x')
        existing_file.write("This file is existing.")
        existing_file.close()
        ditrs = flow_processed_output.DetectorIdToRoadSections()
        ditrs.aimsun_detector_locations = create_DITRS_Dataset(5).dataset
        # Check if warning was raised for existing file
        with warnings.catch_warnings(record=True) as w:
            ditrs.export_to_file(filepath)
            self.assertTrue(len(w) == 1)
        os.remove(filepath)

    def test_DITRS_export_empty_dataset(self):
        """Verify that export_to_file() throws an exception when
        DetectorIdToRoadSections object has empty flow_data_set."""
        filepath = '4.txt'
        empty_ditrs = flow_processed_output.DetectorIdToRoadSections()
        empty_ditrs.aimsun_detector_locations = create_DITRS_Dataset(0).dataset
        # Check if exception was raised for empty aimsun_detector_locations
        with self.assertRaises(Exception):
            empty_ditrs.export_to_file(filepath)

    def test_DITRS_import_wrong_file_serialized(self):
        """Verify that _import_from_file() throws an exception when
        given file contains wrong data type."""
        filepath = '5.txt'
        with open(filepath, 'wb') as file:
            pickle.dump(["This is a wrong dataset"], file)
        # Check if exception was raised for wrong data type
        with self.assertRaises(Exception):
            flow_processed_output.DetectorIdToRoadSections(filepath)
        os.remove(filepath)

    def test_DITRS_import_wrong_file_unserialized(self):
        """Verify that _import_from_file() throws an exception when given
        file did not follow serialization protocols at export_to_file()."""
        filepath = '6.txt'
        wrong_file = open(filepath, 'x')
        wrong_file.write("This is not a serialized detector flow data")
        wrong_file.close()
        # Check if exception was raised for wrong serialization
        with self.assertRaises(Exception):
            flow_processed_output.DetectorIdToRoadSections(filepath)
        os.remove(filepath)


# TODO(Theo/John): modify test cases if the year attribute is used
class testOutputFlowDataSet(unittest.TestCase):
    """Test the export_to_file() and _import_from_file() methods
    of the OutputFlowDataSet() class in flow_processed_output.py.

    This is done by checking that exporting and importing the same
    OutputFlowDataSet instance maintains equality with the original copy.
    Errors such as exporting empty OutputFlowDataSet and importing from
    wrong files are tested by checking that Exceptions or Warnings are
    appropriately raised.
    """

    def test_OFDS_export_create_file(self):
        """Verify whether export_to_file() creates a new file."""
        filepath = '1.txt'
        ofds = flow_processed_output.OutputFlowDataSet()
        ofds.flow_data_set = create_OFDS_Dataset(1).dataset
        ofds.export_to_file(filepath)
        # Check if file was created at filepath
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_OFDS_import_equals_export(self):
        """Verify that export_to_file() and _import_to_file() will
        return the same values."""
        filepath = '2.txt'
        original_ofds = flow_processed_output.OutputFlowDataSet()
        original_ofds.flow_data_set = create_OFDS_Dataset(10).dataset
        original_ofds.export_to_file(filepath)
        # Import using constructor
        new_ofds = flow_processed_output.OutputFlowDataSet(filepath)
        os.remove(filepath)
        # Check if new_ofds contains the same attributes as the original_ofds
        self.assertTrue(new_ofds == original_ofds)
        # Check if new_ofds is not equal to a different ofds of same size
        different_ofds = flow_processed_output.OutputFlowDataSet()
        different_ofds.flow_data_set = create_OFDS_Dataset(10).dataset
        self.assertFalse(new_ofds == different_ofds)

    def test_OFDS_export_existing_file(self):
        """Verify that export_to_file() raises a warning if a file
        already exists at given filepath."""
        filepath = '3.txt'
        existing_file = open(filepath, 'x')
        existing_file.write("This file is existing.")
        existing_file.close()
        ofds = flow_processed_output.OutputFlowDataSet()
        ofds.flow_data_set = create_OFDS_Dataset(5).dataset
        # Check if warning was raised for existing file
        with warnings.catch_warnings(record=True) as w:
            ofds.export_to_file(filepath)
            self.assertTrue(len(w) == 1)
        os.remove(filepath)

    def test_OFDS_export_empty_dataset(self):
        """Verify that export_to_file() throws an exception when
        OutputFlowDataSet object has empty flow_data_set."""
        filepath = '4.txt'
        empty_ofds = flow_processed_output.OutputFlowDataSet()
        empty_ofds.flow_data_set = create_OFDS_Dataset(0).dataset
        # Check if exception was raised for empty flow_data_set
        with self.assertRaises(Exception):
            empty_ofds.export_to_file(filepath)

    def test_OFDS_import_wrong_file_serialized(self):
        """Verify that _import_from_file() throws an exception when
        given file contains wrong data type."""
        filepath = '5.txt'
        with open(filepath, 'wb') as file:
            pickle.dump(["This is a wrong dataset"], file)
        # Check if exception was raised for wrong data type
        with self.assertRaises(Exception):
            flow_processed_output.OutputFlowDataSet(filepath)
        os.remove(filepath)

    def test_OFDS_import_wrong_file_unserialized(self):
        """Verify that _import_from_file() throws an exception when given
        file did not follow serialization protocols at export_to_file()."""
        filepath = '6.txt'
        wrong_file = open(filepath, 'x')
        wrong_file.write("This is not a serialized detector flow data")
        wrong_file.close()
        # Check if exception was raised for wrong serialization
        with self.assertRaises(Exception):
            flow_processed_output.OutputFlowDataSet(filepath)
        os.remove(filepath)


class create_DITRS_Dataset:
    """Generator class for DetectorIdToRoadSections's aimsun_detector_locations.

    This class creates aimsun_detector_locations for the
    DetectorIdToRoadSections class to be used for various test cases.

    To create a dataset, use the following command:
        >>> ditrs = flow_processed_output.DetectorIdToRoadSections()
        >>> ditrs.aimsun_detector_locations
                            = create_DITRS_Dataset(datasize).dataset

    Attributes:
        dataset: Ramdomly generated aimsun_detector_locations.
        datasize: Number of data in dataset.
    """
    dataset: List[flow_processed_output.DetectorIdToRoadSection]
    datasize: int

    def __init__(self, datasize: int):
        """Create dataset of size datasize"""
        self.dataset = []
        self.datasize = datasize
        self.generate_dataset()

    def generate_dataset(self):
        """Add DetectorIdToRoadSection to dataset"""
        for _ in range(self.datasize):
            detector_section_ids = (
                flow_processed_output.DetectorIdToRoadSection())
            # Generate random detector_id
            random_detector_id = flow_processed_output.DetectorId(
                                 random.randint(0, 9999))
            assert isinstance(random_detector_id,
                              flow_processed_output.DetectorId(int))
            # Generate random section_id
            random_section_id = flow_processed_output.SectionId(
                                random.randint(0, 9999))
            assert isinstance(random_section_id,
                              flow_processed_output.SectionId(int))
            # Add random detector_id and section_id to detector_section_ids
            detector_section_ids.detector_id = random_detector_id
            detector_section_ids.section_id = random_section_id
            self.dataset += [detector_section_ids]
        assert len(self.dataset) == self.datasize


class create_OFDS_Dataset:
    """Generator class for OutputFlowDataSet's flow_data_set.

    This class creates flow_data_set for the OutputFlowDataSet
    class to be used for various test cases.

    To create a dataset, use the following command:
        >>> ofds = flow_processed_output.OutputFlowDataSet()
        >>> ofds.flow_data_set = create_OFDS_Dataset(datasize).dataset

    Attributes:
        dataset: Ramdomly generated flow_data_set.
        datasize: Number of data in dataset.
    """
    dataset: List[flow_processed_output.OutputFlowData]
    datasize: int

    def __init__(self, datasize: int):
        """Create dataset of size datasize"""
        self.dataset = []
        self.datasize = datasize
        self.generate_dataset()

    def generate_dataset(self):
        """Add OutputFlowData to dataset"""
        for _ in range(self.datasize):
            output_flow_data = self.generate_output_flow_data()
            self.dataset += [output_flow_data]
        assert len(self.dataset) == self.datasize

    def generate_output_flow_data(self):
        """Generate flow data for a detector"""
        # Generate random detector_id
        random_detector_id = flow_processed_output.DetectorId(
                             random.randint(0, 9999))
        assert isinstance(random_detector_id,
                          flow_processed_output.DetectorId(int))
        # Generate random section_id
        random_section_id = flow_processed_output.SectionId(
                            random.randint(0, 9999))
        assert isinstance(random_section_id,
                          flow_processed_output.SectionId(int))
        # Generate random flow_data
        random_flow_data = self.generate_flowdata()
        # Create OutputFlowData with above parameters
        random_output_flow_data = flow_processed_output.OutputFlowData()
        random_output_flow_data.detector_id = random_detector_id
        random_output_flow_data.section_id = random_section_id
        random_output_flow_data.flow_data = random_flow_data
        assert isinstance(random_output_flow_data,
                          flow_processed_output.OutputFlowData)
        return random_output_flow_data

    def generate_flowdata(self):
        """Generate a random flow data for a detector."""
        random_flowdata = {}
        datasize = random.randint(0, 100)
        for _ in range(datasize):
            timestamp = self.generate_datetime()
            flowsize = self.generate_flowsize()
            random_flowdata.update({timestamp: flowsize})
        assert isinstance(random_flowdata, dict)
        return random_flowdata

    def generate_datetime(self):
        """Generate a random datetime for a detector's flow data."""
        min_year = 1980
        max_year = 2021
        start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + datetime.timedelta(days=365 * years)
        random_datetime = start + (end - start) * random.random()
        assert isinstance(random_datetime, datetime.datetime)
        return random_datetime

    def generate_flowsize(self):
        """Generate a random flow size for a detector."""
        random_flowsize = round(random.uniform(0.0, 200.0), 3)
        assert isinstance(random_flowsize, float)
        return random_flowsize


if __name__ == '__main__':
    unittest.main()
