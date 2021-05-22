"""Contains DetectorIdToRoadSections and OutputFlowDataSet class, as well
as its data classes for its attributes.

Classes:
    DetectorIdToRoadSection: Data class for detector and section IDs.
    DetectorIdToRoadSections: Data class for multiple DetectorIdToRoadSection.
    OutputFlowData: Data class for output flow data from one detector.
    OutputFlowDataSet: Data class for output flow data from multiple detectors.
"""
#modify asdfasdgaasdgdd 12 adsf dsakkadsk af sdijfak 23i32n
#wootas
#yeet

import datetime
from flow_processing_input import DetectorId, SectionId
from os import path
import pickle
from typing import Dict, List
import warnings


class DetectorIdToRoadSection:
    """Data class for one DetectorId to SectionId.

    The object corresponds to data of the detectorID and sectionID
    from one detector.

    Attributes:
        detector_id: ID of the detector.
        section_id: ID of the detector's section.
    """
    detector_id: DetectorId
    section_id: SectionId


class DetectorIdToRoadSections:
    """Data class for multiple DetectorId to SectionId pairs.

    The object corresponds to a list of DetectorIdToRoadSection
    from multiple detectors.

    To export the DetectorIdToRoadSection, use the following command:
        >>> ditrs = DetectorIdToRoadSections()
        >>> ditrs.export_to_file(filepath)

    To import the DetectorIdToRoadSection, use the following command:
        >>> ditrs = DetectorIdToRoadSections(filepath)

    Attributes:
        aimsun_detector_locations: List of DetectorIdToRoadSection
            from multiple detectors.
    """
    aimsun_detector_locations: List[DetectorIdToRoadSection]

    def __init__(self, filepath: str = ""):
        if filepath:
            self._import_from_file(filepath)

    def export_to_file(self, filepath: str):
        """Export DetectorIdToRoadSections to file by serializing
        `aimsun_detector_locations`.

        Raises exception if the aimsun_detector_locations is empty. Warns
        the user if a file already exists at filepath and overwrites it.

        Args:
            filepath: Location to export object attributes.
        """
        # Check if aimsun_detector_locations is empty
        if len(self.aimsun_detector_locations) == 0:
            raise Exception('DetectorIdToRoadSections has no data.'
                            + 'Export aborted.')
        # Check if file exists at given filepath
        if path.exists(filepath):
            warnings.warn('File already exists at filepath. Overwriting file.')
        # Serialize aimsun_detector_locations and write to filepath
        with open(filepath, 'wb') as file:
            pickle.dump(self.aimsun_detector_locations, file)

    def _import_from_file(self, filepath: str):
        """Import DetectorIdToRoadSections from file by deserializing
        `aimsun_detector_locations`.

        Raises exception if the given file does not match the data type of
        aimsun_detector_locations (List[DetectorIdToRoadSection]).

        Args:
            filepath: Location to import object attributes from.
        """
        # Deserialize aimsun_detector_locations from filepath
        with open(filepath, 'rb') as file:
            imported_aimsun_detector_locations = pickle.load(file)
        # Check if imported data matches data type of flow_data_set
        if (isinstance(imported_aimsun_detector_locations, list)
                and isinstance(imported_aimsun_detector_locations[0],
                               DetectorIdToRoadSection)):
            self.aimsun_detector_locations = imported_aimsun_detector_locations
        else:
            raise Exception("File has incorrect data type. Import aborted.")

    def __eq__(self, other):
        """Evaluates object equality based on attributes."""
        # Check if length of aimsun_detector_locations equals each other
        if (len(self.aimsun_detector_locations)
                != len(other.aimsun_detector_locations)):
            return False
        # Check all attributes of aimsun_detector_locations against each other
        for i in range(len(self.aimsun_detector_locations)):
            selfVals = self.aimsun_detector_locations[i]
            otherVals = other.aimsun_detector_locations[i]
            if (selfVals.detector_id != otherVals.detector_id
                    or selfVals.section_id != otherVals.section_id):
                return False
        return True


class OutputFlowData:
    """Data class for output flow data from one detector.

    Attributes:
        detector_id: ID of the detector.
        flow_data: Flow data of the detector.
        section_id: ID of the detector's section.
    """
    detector_id: DetectorId
    flow_data: Dict[datetime.time, float]
    section_id: SectionId


# TODO(Theo): check if we need the year attribute
class OutputFlowDataSet:
    """Data class for output flow data from multiple detectors.

    The object corresponds to a list of OutputFlowData from
    multiple detectors.

    To export the DetectorIdToRoadSection, use the following command:
        >>> ofds = OutputFlowDataSet()
        >>> ofds.export_to_file(filepath)

    To import the DetectorIdToRoadSection, use the following command:
        >>> ofds = OutputFlowDataSet(filepath)

    Attributes:
        flow_data_set: List of OutputFlowData.
        year: Year data was collected.
    """
    flow_data_set: List[OutputFlowData]
    year: int

    def __init__(self, filepath: str = ""):
        if filepath:
            self._import_from_file(filepath)

    def export_to_file(self, filepath: str):
        """Export OutputFlowDataSet to file by serializing `flow_data_set`
        and `year`.

        Raises exception if the detectors_location_dict is empty. Warns the
        user if a file already exists at filepath and overwrites it.

        Args:
            filepath: Location to export object attributes.
        """
        # Check if flow_data_set is empty
        if len(self.flow_data_set) == 0:
            raise Exception('OutputFlowDataSet has no data. Export aborted.')
        # Check if file exists at given filepath
        if path.exists(filepath):
            warnings.warn('File already exists at filepath. Overwriting file.')
        # Serialize flow_data_set and write to filepath
        with open(filepath, 'wb') as file:
            pickle.dump(self.flow_data_set, file)

    def _import_from_file(self, filepath: str):
        """Import OutputFlowDataSet from file by deserializing `flow_data_set`
        and `year`.

        Raises exception if the given file does not match the data type of
        flow_data_set (List[OutputFlowData]) and year (int).

        Args:
            filepath: Location to import object attributes from.
        """
        # Deserialize flow_data_set from filepath
        with open(filepath, 'rb') as file:
            imported_flow_data_set = pickle.load(file)
        # Check if imported data matches data type of flow_data_set
        if (isinstance(imported_flow_data_set, list)
                and isinstance(imported_flow_data_set[0], OutputFlowData)):
            self.flow_data_set = imported_flow_data_set
        else:
            raise Exception("File has incorrect data type. Import aborted.")

    # TODO: write the docstring and the function
    def export_to_aimsun_real_data_set_csv(self, filepath: str):
        """Function docstring.

        Args:
            filepath:
        """
        # Should be consistent with T1.
        # CSV with lines being detector_id, time, count.
        pass

    def __eq__(self, other):
        """Evaluates object equality based on attributes."""
        # Check if length of flow_data_set equals each other
        if len(self.flow_data_set) != len(other.flow_data_set):
            return False
        # Check all attributes of flow_data_set against each other
        for i in range(len(self.flow_data_set)):
            selfVals = self.flow_data_set[i]
            otherVals = other.flow_data_set[i]
            if (selfVals.detector_id != otherVals.detector_id
                    or selfVals.flow_data != otherVals.flow_data
                    or selfVals.section_id != otherVals.section_id):
                return False
        return True
