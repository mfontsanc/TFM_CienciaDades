# EXAMPLES
import os

from config import constants

EXAMPLE_XML_PATH_INPUT = os.path.join(constants.BASE_PATH, "test", "resources")
EXAMPLE_XML_PATH_INPUT_RESULT = os.path.join(constants.BASE_PATH, "resources", 'tmp')
EXAMPLE_COMMUNITY_ID = 2
EXAMPLE_CT_ID = "NCT00002528"
EXAMPLE_INSERT_MODEL_OUTPUT_MESSAGE = 'Process ended.'
EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE = True
EXAMPLE_GET_COMMUNITIES_OUTPUT_DATA = [['NCT00001378', 1]]
EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_DATA = [['NCT00001378', "has study objective", "InterventionModel.TREATMENT"]]
EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_SPONSORS = [['NCT00001378', "Genentech, Inc."]]
EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_PRINCIPAL_INVESTIGATOR = [['NCT00001378', "Ospedale Civile Rimini", "Rimini",
                                                                 "Italy", "40009"]]
EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_LOCATION = [['NCT00001378', "James N", "Study Chair", "Mayo Clinic"]]
