"""Contains test cases for flow_processing_input.py.

Classes:
    testDetectorsLocation: Test cases for the DetectorsLocation class.
    testGroundFlowData: Test cases for the GroundFlowData class.
    createDLDataset: Data class for randomly generated DetectorsLocation.
    createGFDDataset: Data class for randomly generated GroundFlowData.

To run all test cases, use the following command:
    >>> python3 flow_processing_input_test.py
"""

import datetime
import os
import pickle
import random
import string
import unittest
import warnings

from shapely.geometry import Point
from typing import List, Dict, Tuple

import flow_processing_input


class testDetectorsLocation(unittest.TestCase):
    """Test the export_to_file() and import_from_file() methods
    of the DetectorsLocation() class in flow_processing_input.py.

    This is done by checking that exporting and importing the same
    DetectorsLocation instance maintains equality with the original copy.
    Errors such as exporting empty DetectorsLocation and importing from
    wrong files are tested by checking that Exceptions or Warnings are
    appropriately raised.
    """

    def test_DL_export_create_file(self):
        """Verify whether export_to_file() creates a new file."""
        filepath = '1.txt'
        dl = flow_processing_input.DetectorsLocation(2021)
        dl.detectors_location_dict = createDLDataset(1).dataset
        dl.export_to_file(filepath)
        # Check if file was created at filepath
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_DL_import_equals_export(self):
        """Verify that export_to_file() and import_to_file() will
        return the same values."""
        filepath = '2.txt'
        original_dl = flow_processing_input.DetectorsLocation(2021)
        original_dl.detectors_location_dict = createDLDataset(10).dataset
        original_dl.export_to_file(filepath)
        new_dl = flow_processing_input.DetectorsLocation(2021, filepath)
        os.remove(filepath)
        # Check if new_dl contains the same attributes as the original_dl
        self.assertTrue(new_dl == original_dl)
        # Check if new_dl is not equal to a different DL of same size
        random_dl = flow_processing_input.DetectorsLocation(2021)
        random_dl.detectors_location_dict = createDLDataset(10).dataset
        self.assertFalse(new_dl == random_dl)

    def test_DL_export_existing_file(self):
        """Verify that export_to_file() raises a warning if a file
        already exists at given filepath."""
        filepath = '3.txt'
        existing_file = open(filepath, 'x')
        existing_file.write("This file is existing.")
        existing_file.close()
        dl = flow_processing_input.DetectorsLocation(2021)
        dl.detectors_location_dict = createDLDataset(5).dataset
        # Check if warning was raised for existing file
        with warnings.catch_warnings(record=True) as w:
            dl.export_to_file(filepath)
            self.assertTrue(len(w) == 1)
        os.remove(filepath)

    def test_DL_export_empty_dataset(self):
        """Verify that export_to_file() throws an exception when
        GroundFlowData object has empty detector_flow_data."""
        filepath = '4.txt'
        empty_dl = flow_processing_input.DetectorsLocation(2021)
        empty_dl.detector_flow_data = createDLDataset(0).dataset
        # Check if exception was raised for empty detector_flow_data
        with self.assertRaises(Exception):
            empty_dl.export_to_file(filepath)

    def test_DL_import_wrong_file_serialized(self):
        """Verify that _import_from_file() throws an exception when
        given file contains wrong data type."""
        filepath = '5.txt'
        with open(filepath, 'wb') as file:
            pickle.dump(["This is a wrong dataset"], file)
        # Check if exception was raised for wrong data type
        with self.assertRaises(Exception):
            flow_processing_input.DetectorsLocation(9999, filepath)
        os.remove(filepath)

    def test_DL_import_wrong_file_unserialized(self):
        """Verify that _import_from_file() throws an exception when given
        file did not follow serialization protocols at export_to_file()."""
        filepath = '6.txt'
        wrong_file = open(filepath, 'x')
        wrong_file.write("This is not a serialized detector flow data")
        wrong_file.close()
        # Check if exception was raised for wrong serialization
        with self.assertRaises(Exception):
            flow_processing_input.DetectorsLocation(9999, filepath)
        os.remove(filepath)

    def test_DL_import_from_constructor(self):
        """Verify that adding a filepath to the constructor imports the
        given DetectorsLocation() class properly."""
        filepath = '7.txt'
        original_dl = flow_processing_input.DetectorsLocation(2021)
        original_dl.detectors_location_dict = createDLDataset(10).dataset
        original_dl.export_to_file(filepath)
        new_dl = flow_processing_input.DetectorsLocation(2021, filepath)
        os.remove(filepath)
        # Check if new_dl contains the same attributes as the original_dl
        self.assertTrue(new_dl == original_dl)


class testGroundFlowData(unittest.TestCase):
    """Test the export_to_file() and _import_from_file() methods
    of the GroundFlowData() class in flow_processing_input.py.

    This is done by checking that exporting and importing the same
    GroundFlowData instance maintains equality with the original copy.
    Errors such as exporting empty GroundFlowData and importing from
    wrong files are tested by checking that Exceptions or Warnings are
    appropriately raised.
    """

    def test_GFD_export_create_file(self):
        """Verify whether export_to_file() creates a new file."""
        filepath = '1.txt'
        gfd = flow_processing_input.GroundFlowData()
        gfd.detector_flow_data = createGFDDataset(1).dataset
        gfd.export_to_file(filepath)
        # Check if file was created at filepath
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_GFD_import_equals_export(self):
        """Verify that export_to_file() and import_to_file() will
        return the same values."""
        filepath = '2.txt'
        original_gfd = flow_processing_input.GroundFlowData()
        original_gfd.detector_flow_data = createGFDDataset(10).dataset
        original_gfd.export_to_file(filepath)
        new_gfd = flow_processing_input.GroundFlowData(filepath)
        os.remove(filepath)
        # Check if new_gfd contains the same attributes as the original_gfd
        self.assertTrue(new_gfd == original_gfd)
        # Check if new_gfd is not equal to a different gfd of same size
        random_gfd = flow_processing_input.GroundFlowData()
        random_gfd.detector_flow_data = createGFDDataset(10).dataset
        self.assertFalse(new_gfd == random_gfd)

    def test_GFD_export_existing_file(self):
        """Verify that export_to_file() raises a warning if a file
        already exists at given filepath."""
        filepath = '3.txt'
        existing_file = open(filepath, 'x')
        existing_file.write("This file is existing.")
        existing_file.close()
        gfd = flow_processing_input.GroundFlowData()
        gfd.detector_flow_data = createGFDDataset(5).dataset
        # Check if warning was raised for existing file
        with warnings.catch_warnings(record=True) as w:
            gfd.export_to_file(filepath)
            self.assertTrue(len(w) == 1)
        os.remove(filepath)

    def test_GFD_export_empty_dataset(self):
        """Verify that export_to_file() throws an exception when
        GroundFlowData object has empty detector_flow_data."""
        filepath = '4.txt'
        empty_gfd = flow_processing_input.GroundFlowData()
        empty_gfd.detector_flow_data = createGFDDataset(0).dataset
        # Check if exception was raised for empty detector_flow_data
        with self.assertRaises(Exception):
            empty_gfd.export_to_file(filepath)

    def test_GFD_import_wrong_file_serialized(self):
        """Verify that _import_from_file() throws an exception when
        given file contains wrong data type."""
        filepath = '5.txt'
        with open(filepath, 'wb') as file:
            pickle.dump(["This is a wrong dataset"], file)
        # Check if exception was raised for wrong data type
        with self.assertRaises(Exception):
            flow_processing_input.GroundFlowData(filepath)
        os.remove(filepath)

    def test_GFD_import_wrong_file_unserialized(self):
        """Verify that _import_from_file() throws an exception when given
        file did not follow serialization protocols at export_to_file()."""
        filepath = '6.txt'
        wrong_file = open(filepath, 'x')
        wrong_file.write("This is not a serialized detector flow data")
        wrong_file.close()
        # Check if exception was raised for wrong serialization
        with self.assertRaises(Exception):
            flow_processing_input.GroundFlowData(filepath)
        os.remove(filepath)

    def test_GFD_import_from_constructor(self):
        """Verify that adding a filepath to the constructor imports the
        given GroundFlowData() class properly."""
        filepath = '7.txt'
        original_gfd = flow_processing_input.GroundFlowData()
        original_gfd.detector_flow_data = createGFDDataset(10).dataset
        original_gfd.export_to_file(filepath)
        new_gfd = flow_processing_input.GroundFlowData(filepath)
        os.remove(filepath)
        # Check if new_gfd contains the same attributes as the original_gfd
        self.assertTrue(new_gfd == original_gfd)


class createDLDataset:
    """Generator class for DetectorsLocation's detectors_location_dict.

    This class creates detectors_location_dict for the DetectorsLocation
    class to be used for various test cases.

    To create a dataset, use the following command:
        >>> dl = flow_processing_input.DetectorsLocation(year)
        >>> dl.detectors_location_dict = createDLDataset(datasize).dataset

    Attributes:
        dataset: Ramdomly generated detector_flow_data.
        num_detectors: Number of detectors in dataset.
    """
    dataset: Dict[flow_processing_input.DetectorId,
                  Tuple[flow_processing_input.Direction,
                        flow_processing_input.Point]]
    num_locations: int

    def __init__(self, num_locations):
        """Create dataset of size num_locations"""
        self.dataset = {}
        self.num_locations = num_locations
        self.add_locations()

    def add_locations(self):
        """Add detectors and their locations to dataset"""
        for _ in range(0, self.num_locations):
            detector_id = self.generate_id()
            detector_direction = self.generate_direction()
            detector_point = self.generate_point()
            self.dataset[detector_id] = (detector_direction, detector_point)
        assert len(self.dataset) == self.num_locations

    def generate_id(self):
        """Generate a random ID for a detector"""
        random_Id = flow_processing_input.DetectorId(random.randint(0, 9999))
        assert isinstance(random_Id, flow_processing_input.DetectorId(int))
        return random_Id

    def generate_direction(self):
        """Generate a random direction for a detector."""
        random_enum = random.randint(1, 4)
        random_direction = flow_processing_input.Direction(random_enum)
        assert isinstance(random_direction, flow_processing_input.Direction)
        return random_direction

    def generate_point(self):
        """Generate a random point for a detector."""
        x = random.uniform(0.0, 9999.9)
        y = random.uniform(0.0, 9999.9)
        random_point = Point(x, y)
        assert isinstance(random_point, Point)
        return random_point


class createGFDDataset:
    """Generator class for GroundFlowData's detector_flow_data.

    This class creates detector_flow_data for the GroundFlowData
    class to be used for various test cases.

    To create a dataset, use the following command:
        >>> gfd = flow_processing_input.GroundFlowData()
        >>> gfd.detector_flow_data = createGFDDataset(datasize).dataset

    Attributes:
        dataset: Ramdomly generated detector_flow_data.
        num_detectors: Number of detectors in dataset.
    """
    dataset: List[flow_processing_input.DetectorFlowData]
    num_detectors: int

    def __init__(self, num_detectors):
        """Create dataset of size num_detectors"""
        self.dataset = []
        self.num_detectors = num_detectors
        self.add_detectors()

    def add_detectors(self):
        """Add detectors and their attributes to dataset"""
        for _ in range(self.num_detectors):
            detector = flow_processing_input.DetectorFlowData()
            detector.detector_id = self.generate_id()
            detector.direction = self.generate_direction()
            detector.name = self.generate_name()
            detector.flow_data = self.generate_flowdata()
            detector.year = 2021
            self.dataset += [detector]
        assert len(self.dataset) == self.num_detectors

    def generate_id(self):
        """Generate a random ID for a detector"""
        random_Id = flow_processing_input.DetectorId(random.randint(0, 9999))
        assert isinstance(random_Id, flow_processing_input.DetectorId(int))
        return random_Id

    def generate_direction(self):
        """Generate a random direction for a detector."""
        random_enum = random.randint(1, 4)
        random_direction = flow_processing_input.Direction(random_enum)
        assert isinstance(random_direction, flow_processing_input.Direction)
        return random_direction

    def generate_name(self):
        """Generate a random name for a detector."""
        letters = string.ascii_letters
        random_name = ''.join(random.choice(letters) for _ in range(10))
        assert isinstance(random_name, str)
        return random_name

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
