"""Contains DetectorsLocation and GroundFlowData class, as well as its
data classes for its attributes.

Classes:
    Direction: Data class for the direction of flow.
    DetectorsLocation: Data class for the location of multiple traffic flow
        detectors.
    DetectorFlowData: Data class for data from one traffic flow detector.
    GroundFlowData: Data class for data from multiple traffic flow detectors.
"""

import datetime
import pickle
import warnings

from enum import Enum
from os import path
from shapely.geometry import Point
from typing import Dict, NewType, Tuple, List

DetectorId = NewType('DetectorId', int)
SectionId = NewType('SectionId', int)


class Direction(Enum):
    """Possible direction of the flow going through a detector."""
    north_bound = 1
    east_bound = 2
    south_bound = 3
    west_bound = 4


class DetectorsLocation:
    """Detectors location data class.

    Contains a dictionary of detector locations and the year corresponding
    to the year data was collected.

    To export the DetectorsLocation, use the following command:
        >>> dl = DetectorsLocation(year)
        >>> dl.export_to_file(filepath)

    To import the DetectorsLocation, use the following command:
        >>> dl = DetectorsLocation(year, filepath)

    Attributes:
        detectors_location_dict: Dictionary of the detector locations.
        year: Year data was collected.
    """
    detectors_location_dict: Dict[DetectorId, Tuple[Direction, Point]]
    year: int

    def __init__(self, year: int, filepath: str = ""):
        self.year = year
        if filepath != "":
            self._import_from_file(filepath)

    def export_to_file(self, filepath: str):
        """Export DetectorsLocation to file by serializing
        `detectors_location_dict` and `year`.

        Raises exception if the detectors_location_dict is empty. Warns the
        user if a file already exists at filepath and overwrites it.
        """
        # Check if detectors_location_dict is empty
        if len(self.detectors_location_dict) == 0:
            raise Exception('DetectorsLocation has no data. Export aborted.')
        # Check if file exists at given filepath
        if path.exists(filepath):
            warnings.warn('File already exists at filepath. Overwriting file.')
        # Serialize detectors_location_dict and write to filepath
        with open(filepath, 'wb') as file:
            pickle.dump(self.detectors_location_dict, file)
            pickle.dump(self.year, file)

    def _import_from_file(self, filepath: str):
        """Import DetectorsLocation from file by deserializing
        `detectors_location_dict` and `year`.

        Raises exception if the given file does not match the data type of
        detector_flow_data (Dict) and year (int).
        """
        # Deserialize detectors_location_dict from filepath
        with open(filepath, 'rb') as file:
            imported_location_dict = pickle.load(file)
            imported_year = pickle.load(file)
        # Check if imported data matches data type of detectors_location_dict
        if (isinstance(imported_location_dict, dict) and
                isinstance(imported_year, int)):
            self.detectors_location_dict = imported_location_dict
            self.year = imported_year
        else:
            raise Exception("File has incorrect data type. Import aborted.")

    def __eq__(self, other):
        """Evaluates object equality based on attributes."""
        # Return False if year is different
        if self.year != other.year:
            return False
        for key in self.detectors_location_dict:
            if key in other.detectors_location_dict:
                selfVal = self.detectors_location_dict[key]
                selfDirection = selfVal[0]
                selfPoint = selfVal[1]
                otherVal = other.detectors_location_dict[key]
                otherDirection = otherVal[0]
                otherPoint = otherVal[1]
                if not (selfDirection == otherDirection
                        and selfPoint.x == otherPoint.x
                        and selfPoint.y == otherPoint.y):
                    return False
            else:
                return False
        return True


class DetectorFlowData:
    """Detector flow data class.

    The object corresponds to data from one traffic flow detector.

    Attributes:
        detector_id: ID of the detector.
        direction: Direction of the detected flow.
        flow_data: Timestamps and sizes of detected flows.
        name: Name of the detector.
        year: Year data was collected.
    """
    detector_id: DetectorId
    direction: Direction
    flow_data: Dict[datetime.datetime, float]
    name: str
    year: int


class GroundFlowData:
    """Ground flow data class.

    Contains a list of detector flow data. There is a corresponding
    `DetectorFlowData` for each element in the list.

    To export the GroundFlowData, use the following command:
        >>> gfd = GroundFlowData()
        >>> gfd.export_to_file(filepath)

    To import the GroundFlowData, use the following command:
        >>> gfd = GroundFlowData(filepath)

    Attributes:
        detector_flow_data: List of flow data from multiple detectors.
    """
    detector_flow_data: List[DetectorFlowData]

    def __init__(self, filepath: str = ""):
        if filepath != "":
            self._import_from_file(filepath)

    def export_to_file(self, filepath: str):
        """Export GroundFlowData to file by serializing detector_flow_data.

        Raises exception if the detector_flow_data is empty. Warns the user
        if a file already exists at filepath and overwrites it.
        """
        # Check if detector_flow_data is empty
        if len(self.detector_flow_data) == 0:
            raise Exception('GroundFlowData has no data. Export aborted.')
        # Check if file exists at given filepath
        if path.exists(filepath):
            warnings.warn('File already exists at filepath. Overwriting file.')
        # Serialize detector_flow_data and write to filepath
        with open(filepath, 'wb') as file:
            pickle.dump(self.detector_flow_data, file)

    def _import_from_file(self, filepath: str):
        """Import GroundFlowData from file by deserializing detector_flow_data.

        Raises exception if the given file does not match the data type of
        detector_flow_data (List[DetectorFlowData]).
        """
        # Deserialize detector_flow_data from filepath
        with open(filepath, 'rb') as file:
            imported_data = pickle.load(file)
        # Check if imported data matches data type of detector_flow_data
        if (isinstance(imported_data, list)
                and isinstance(imported_data[0], DetectorFlowData)):
            self.detector_flow_data = imported_data
        else:
            raise Exception("File has incorrect data type. Import aborted.")

    def __eq__(self, other):
        """Evaluates object equality based on attributes."""
        # Return False if detector_flow_data size is different
        if len(self.detector_flow_data) != len(other.detector_flow_data):
            return False
        # Check all attributes of detector_flow_data against each other
        equality = True
        for i in range(len(self.detector_flow_data)):
            this_detector = self.detector_flow_data[i]
            other_detector = other.detector_flow_data[i]
            if (this_detector.detector_id != other_detector.detector_id
                    or this_detector.direction != other_detector.direction
                    or this_detector.flow_data != other_detector.flow_data
                    or this_detector.name != other_detector.name
                    or this_detector.year != other_detector.year):
                equality = False
        return equality
