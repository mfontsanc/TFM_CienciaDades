import os

# -------------------------------------------- PROJECT CONFIGURATION -------------------------------------------------
PROJECT_NAME = 'tfm-collaboration-network'
VERSION = 'v1.0'
PROJECT_NAME_FOLDER = 'dev'
BASE_PATH_EXECUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(BASE_PATH_EXECUTE)
HOME_PATH_LOG = os.path.join(BASE_PATH, PROJECT_NAME_FOLDER, 'logs')

# ---------------------------------------------- RESULTS FOLDERS -----------------------------------------------------
TEMP_TTL_FOLDER = os.path.join(BASE_PATH, "dev", "resources", "tmp")
ONTOLOGY_TTL_FOLDER = os.path.join(BASE_PATH, "dev", "resources", "ocre")
TSV_FILE = "clinical_trials.tsv"
RDF_FOLDER = "/rdf"
JSON_COORDINATES = os.path.join(BASE_PATH, "dev", "resources", "coordinates.json")

# ----------------------------------------------- API CONFIGURATION --------------------------------------------------
API_PORT = os.environ.get('API_PORT', 5000)
API_DEBUG = False

# API GENERIC URL
END_POINT_API = f'/{PROJECT_NAME}/{VERSION[:2]}'
END_POINT_SWAGGER = f'{END_POINT_API}/swagger'
END_POINT_SWAGGER_JSON = f'{END_POINT_API}/swagger.json'

# API KEYS
KEY_TITLE = 'title'
KEY_TITLE_END_POINT = 'end_point'
KEY_TITLE_DIRECTORIES = 'directories'
KEY_DESCRIPTION = 'description'
KEY_DOC = 'documentation'

# API KEYS ENDPOINTS
KEY_NETWORK = 'uoc_tfm_network_collaboration'
KEY_NETWORK_COMMUNITIES = 'uoc_tfm_network_communities'
KEY_NETWORK_GET_COMMUNITIES = 'uoc_tfm_network_get_communities'
KEY_NETWORK_GET_COMMUNITIES_CT = 'uoc_tfm_network_get_communities_clinical_trials'
KEY_NETWORK_GET_COMMUNITIES_DETAIL = 'uoc_tfm_network_get_communities_detail'
KEY_NETWORK_GET_COLLABORATORS = 'uoc_tfm_network_get_collaborators'
KEY_NETWORK_GET_CLINICAL_TRIAL = 'uoc_tfm_network_get_clinical_trial'

# API DESCRIPTION
NAME_API = 'networkCollaboration'
TITLE_API = 'UOC - TFM - Network collaboration'
DESCRIPTION_API = 'UOC - TFM - Network collaboration related to breast cancer clinical trials'
NAME_BLUEPRINT = 'tfm_network'

# API ENDPOINTS
# TITLES
TITLE_NETWORK = 'NetworkCollaboration'

# DESCRIPTIONS
DESCRIPTION_NETWORK = 'API namespace for Network collaboration'
DESCRIPTION_NETWORK_MODEL_INPUT = 'Input'
DESCRIPTION_NETWORK_MODEL_INPUT_FOLDER = 'String input with the path including all XML to be processed'
DESCRIPTION_NETWORK_MODEL_INPUT_RESULT = 'String input with the path where the output will be stored'
DESCRIPTION_NETWORK_MODEL_INPUT_DB = 'Boolean if the RDF will be stored in the database (default: True)'
DESCRIPTION_NETWORK_MODEL_OUTPUT_RESULT = 'String output resulting of the process'
DESCRIPTION_NETWORK_MODEL_OUTPUT_MESSAGE = 'String output with the messages according with the process'
DESCRIPTION_NETWORK_MODEL_OUTPUT_RESPONSE = 'Boolean output according with the process result'
DESCRIPTION_NETWORK_MODEL_OUTPUT_RESULT = 'String output with the path where the output is stored'

DESCRIPTION_NETWORK_MODEL_OUTPUT_DATA = 'List output with the data get from the database'
DESCRIPTION_NETWORK_MODEL_OUTPUT_SPONSORS = 'List output with the sponsors get from the database'
DESCRIPTION_NETWORK_MODEL_OUTPUT_PRINCIPAL_INVESTIGATORS = 'List output with the principal inviestigators' \
                                                           ' get from the database'
DESCRIPTION_NETWORK_MODEL_OUTPUT_LOCATIONS = 'List output with the locations get from the database'

DESCRIPTION_NETWORK_MODEL_INPUT_COMMUNITY = 'String input with the path including all community txt files.'
DESCRIPTION_NETWORK_MODEL_INPUT_COMMUNITY_ID = 'String input with the community identifier.'
DESCRIPTION_NETWORK_MODEL_INPUT_CT_ID = 'String input with the clinical trial identifier.'

DESCRIPTION_NETWORK_TYPE = 'Int indicating the type of request.'
DESCRIPTION_NETWORK_MESSAGE = 'String indicating the result in text.'

# DOCUMENTATION
DOCUMENTATION_NETWORK = 'Class to execute the transformation process from XML to RDF, and the insertion to GraphDB.'
DOCUMENTATION_NETWORK_COMMUNITIES = 'Class to insert the relations between the different clinical trials.'
DOCUMENTATION_NETWORK_GET_COMMUNITIES = 'Class to get the communities.'
DOCUMENTATION_NETWORK_GET_COMMUNITIES_CT = 'Class to get the clinical trials and community data.'
DOCUMENTATION_NETWORK_GET_COMMUNITIES_DETAILS = 'Class to get the clinical trials and its properties of ' \
                                                'one specific community.'
DOCUMENTATION_NETWORK_GET_COLLABORATORS = 'Class to get the sponsors and collaborators of one specific community.'
DOCUMENTATION_NETWORK_GET_CLINICAL_TRIAL = 'Class to get all data of one clinical trial.'

# ENDPOINTS
END_POINT_NETWORK = "/insert"
END_POINT_NETWORK_COMMUNITIES = "/insert_communities"
END_POINT_NETWORK_GET_COMMUNITIES = "/get_communities"
END_POINT_NETWORK_GET_COMMUNITIES_CT = "/get_communities_clinical_trials"
END_POINT_NETWORK_GET_COMMUNITIES_DETAIL = "/get_communities_detail"
END_POINT_NETWORK_GET_COLLABORATORS = "/get_collaborators"
END_POINT_NETWORK_GET_CLINICAL_TRIAL = "/get_clinical_trial"

# KEY ARGUMENTS
KEY_NAME_PATH = 'folder_xml_path'
KEY_NAME_COMMUNITY_PATH = 'folder_path'
KEY_NAME_REQUEST_DB_INSERT = 'insert_database'
KEY_NAME_REQUEST_COMMUNITY_ID = 'community_id'
KEY_NAME_REQUEST_CT_ID = 'id'
KEY_NAME_OUTPUT = 'folder_results'
KEY_NAME_RESPONSE_MESSAGE = 'message'
KEY_NAME_RESPONSE_RESULT = 'result'
KEY_NAME_RESPONSE = 'response'

KEY_NAME_RESPONSE_DATA = 'data'
KEY_NAME_RESPONSE_SPONSORS = 'sponsors'
KEY_NAME_RESPONSE_PRINCIPAL_INVESTIGATORS = 'principal_investigator'
KEY_NAME_RESPONSE_COLLABORATORS = 'collaborators'
KEY_NAME_RESPONSE_COMMUNITIES = 'communities'

# -------------------------------------------- FUNCTIONALITIES -------------------------------------------------------

FUNCTIONALITIES = {
    KEY_NETWORK: {KEY_TITLE: TITLE_NETWORK, KEY_TITLE_END_POINT: END_POINT_NETWORK, KEY_TITLE_DIRECTORIES: [],
                  KEY_DESCRIPTION: DESCRIPTION_NETWORK, KEY_DOC: DOCUMENTATION_NETWORK},
    KEY_NETWORK_COMMUNITIES: {KEY_TITLE: TITLE_NETWORK, KEY_TITLE_END_POINT: END_POINT_NETWORK_COMMUNITIES,
                              KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                              KEY_DOC: DOCUMENTATION_NETWORK_COMMUNITIES},
    KEY_NETWORK_GET_COMMUNITIES: {KEY_TITLE: TITLE_NETWORK, KEY_TITLE_END_POINT: END_POINT_NETWORK_GET_COMMUNITIES,
                                  KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                                  KEY_DOC: DOCUMENTATION_NETWORK_GET_COMMUNITIES},
    KEY_NETWORK_GET_COMMUNITIES_CT: {KEY_TITLE: TITLE_NETWORK,
                                     KEY_TITLE_END_POINT: END_POINT_NETWORK_GET_COMMUNITIES_CT,
                                     KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                                     KEY_DOC: DOCUMENTATION_NETWORK_GET_COMMUNITIES_CT},
    KEY_NETWORK_GET_COMMUNITIES_DETAIL: {KEY_TITLE: TITLE_NETWORK,
                                         KEY_TITLE_END_POINT: END_POINT_NETWORK_GET_COMMUNITIES_DETAIL,
                                         KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                                         KEY_DOC: DOCUMENTATION_NETWORK_GET_COMMUNITIES_DETAILS},
    KEY_NETWORK_GET_COLLABORATORS: {KEY_TITLE: TITLE_NETWORK,
                                    KEY_TITLE_END_POINT: END_POINT_NETWORK_GET_COLLABORATORS,
                                    KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                                    KEY_DOC: DOCUMENTATION_NETWORK_GET_COLLABORATORS},
    KEY_NETWORK_GET_CLINICAL_TRIAL: {KEY_TITLE: TITLE_NETWORK,
                                     KEY_TITLE_END_POINT: END_POINT_NETWORK_GET_CLINICAL_TRIAL,
                                     KEY_TITLE_DIRECTORIES: [], KEY_DESCRIPTION: DESCRIPTION_NETWORK,
                                     KEY_DOC: DOCUMENTATION_NETWORK_GET_CLINICAL_TRIAL},
}

# ---------------------------------------- DATABASE CONFIGURATION ----------------------------------------------------
GRAPHDB_REPOSITORY = "clinical_trials"
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/" + GRAPHDB_REPOSITORY
GRAPHDB_STATEMENTS = "http://localhost:7200/repositories/" + GRAPHDB_REPOSITORY + "/statements"
GRAPHDB_ONTOLOGY_NG = "http://localhost:7200/repositories/" + GRAPHDB_REPOSITORY + "/rdf-graphs/" \
                      "service?graph=http%3A%2F%2Fpurl.org%2Fnet%2FOCRe%2FOCRe.owl%23"

# ---------------------------------------- RDF NAMESPACES ------------------------------------------------------------
OCRE_NAMESPACE = "http://purl.org/net/OCRe/OCRe.owl#"
OCRE_PROTOCOL_NAMESPACE = "http://purl.org/net/OCRe/study_protocol.owl#"
OCRE_DESIGN_NAMESPACE = "http://purl.org/net/OCRe/study_design.owl#"
TFM_NAMESPACE = "http://purl.org/net/TFM/communities#"
