import os

from config import messages
from tfm.data_type.clinical_trial_structure import ClinicalTrialStructure
from tfm.similarity.transformation_tsv import TransformationTSV
from tfm.validate.file_manager import FileManager
from tfm.xml2rdf import logger
from tfm.xml2rdf.transformation_clinical_trials import TransformationClinicalTrials
from tfm.xml2rdf.transformation_rdf import TransformationRDF
from utils.database_manager import DatabaseManager


class TransformationXML2RDF:
    xml_folder_path: str
    store_db: bool
    output_path: str
    clinical_trials: list[ClinicalTrialStructure]

    def __init__(self, folder_path: str, store_db: bool, output_path: str):
        self.xml_folder_path = folder_path
        self.store_db = store_db
        self.output_path = output_path
        self.clinical_trials = []

    def __process_save_data__(self, xml_path: str):
        """ Method to execute TransformationClinicalTrials, and controls the occurred exception, if any.

            Parameters:
                xml_path (str): Path to a specific XML.

            Returns:
                None
        """
        try:
            self.clinical_trials.append(TransformationClinicalTrials.xml2clinical_trials(xml_path))
        except Exception as ex:
            message = messages.MESSAGE_SAVE_XML_ERROR.format(xml_path, ex.__str__())
            logger.error(message)

    def start_process(self):
        """
            Start the transformation process.
            1. Validation that the input folder path exists.
            2. Initialize the loop per each XML.

            Parameters:

            Returns:
                Bool: whether the process has ended successfully or not.
                str: message of the status of the process.
        """
        result_messages = []
        logger.info(messages.MESSAGE_PROCESS_STARTED)

        # 1. Validates that the input path exists, and it is a folder.
        if not FileManager.validate_folder_path(self.xml_folder_path):
            return False, messages.MESSAGE_VALIDATION_KO

        # 2. Loop to store the XML data into the clinical_trials dataset
        dir_list = os.listdir(self.xml_folder_path)

        for file in dir_list:
            file_path = self.xml_folder_path + "/" + file
            if os.path.isfile(file_path):
                self.__process_save_data__(file_path)

        if len(self.clinical_trials) == 0:
            return False, messages.MESSAGE_SAVE_XML_KO

        logger.info(messages.MESSAGE_SAVE_XML_OK)
        result_messages.append(messages.MESSAGE_SAVE_XML_OK)

        # 3. Transform to RDF and save it into GraphDB
        for ct in self.clinical_trials:
            transformation_status, message = TransformationRDF.process_to_rdf(ct, self.output_path)

            if not transformation_status:
                return False, message

        logger.info(messages.MESSAGE_PROCESS_TRANSFORMATION_RDF_ENDED)
        result_messages.append(messages.MESSAGE_PROCESS_TRANSFORMATION_RDF_ENDED)

        # 4. Store it into GraphDB
        if self.store_db:
            db_manager = DatabaseManager()
            clinical_trials_in_db = 0
            if db_manager.ping():
                db_manager.insert_ontology_rdf()
                for ct in self.clinical_trials:
                    result = db_manager.run_insert_rdf(ct.filename)

                    if result:
                        clinical_trials_in_db += 1

            logger.info(messages.MESSAGE_PROCESS_STORE_DATABASE_ENDED)

            message = messages.MESSAGE_STATUS_DATABASE_INSERT.format(str(clinical_trials_in_db),
                                                                     str(len(self.clinical_trials)))
            logger.info(message)
            result_messages.append(message)

        # 5. Generate TSV
        transformation_tsv = TransformationTSV(clinical_trials=self.clinical_trials, result_path=self.output_path)
        status, message = transformation_tsv.process_to_tsv()

        if not status:
            return False, message

        logger.info(message)
        result_messages.append(message)

        result_messages.append(messages.MESSAGE_TRANSFORMATION_OK)
        logger.info(messages.MESSAGE_PROCESS_ENDED)

        return True, str(result_messages)
