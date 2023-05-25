import os

from config import messages
from tfm.similarity import logger
from tfm.similarity.transformation_communities2rdf import TransformationCommunity2RDF
from tfm.validate.file_manager import FileManager
from utils.database_manager import DatabaseManager


class CommunityRelationship:
    clinical_trials_relationship: list
    folder_path: str

    def __init__(self, path: str):
        self.clinical_trials_relationship = []
        self.folder_path = path

    def __process_save_data__(self, file_path: str):
        """ Method to execute the storage of the community data, and controls the occurred exception, if any.

            Parameters:
                file_path (str): Path to a specific TXT file.

            Returns:
                None
        """
        try:
            clinical_trials = []
            f = open(file_path, 'r')
            lines = f.readlines()

            for line in lines:
                line = line.strip()
                line = line.replace("ClinicalTrial::", "")
                clinical_trials.append(line)

            self.clinical_trials_relationship.append(clinical_trials)

        except Exception as ex:
            message = messages.MESSAGE_SAVE_XML_ERROR.format(file_path, ex.__str__())
            logger.error(message)

    def start_process(self):
        """
            Start the insertion of community relationship process.

            Parameters:

            Returns:
                Bool: whether the process has ended successfully or not.
                str: message of the status of the process.
        """
        result_messages = []
        logger.info(messages.MESSAGE_PROCESS_STARTED)

        # 1. Validates that the input path exists, and it is a folder.
        if not FileManager.validate_folder_path(self.folder_path):
            return False, messages.MESSAGE_VALIDATION_KO

        # 2. Loop to store the TXT data into a list
        dir_list = os.listdir(self.folder_path)

        for file in dir_list:
            file_path = self.folder_path + "/" + file
            if os.path.isfile(file_path):
                self.__process_save_data__(file_path)

        if len(self.clinical_trials_relationship) != len(dir_list):
            message = messages.MESSAGE_SAVE_COMMUNITIES_TXT.format(str(len(self.clinical_trials_relationship)),
                                                                   str(len(dir_list)))
            return False, message

        logger.info(messages.MESSAGE_SAVE_COMMUNITIES_TXT_OK)
        result_messages.append(messages.MESSAGE_SAVE_COMMUNITIES_TXT_OK)

        # 3. Generate triples
        list_triples = TransformationCommunity2RDF(clinical_trials_relationship=self.clinical_trials_relationship)\
            .generate_triples()

        if len(list_triples) == 0:
            return False, messages.MESSAGE_GENERATION_TRIPLES_KO

        logger.info(messages.MESSAGE_GENERATION_TRIPLES_OK)
        result_messages.append(messages.MESSAGE_GENERATION_TRIPLES_OK)

        # 4. Insert to database
        db_manager = DatabaseManager()
        if not db_manager.ping():
            return False, messages.MESSAGE_DATABASE_KO
        else:
            status, num_processed = db_manager.run_insert_triples(list_triples)

            if not status:
                message = messages.MESSAGE_INSERT_TRIPLES_KO.format(str(num_processed), str(len(list_triples)))
                return False, message

        logger.info(messages.MESSAGE_INSERT_TRIPLES_OK)
        result_messages.append(messages.MESSAGE_INSERT_TRIPLES_OK)

        logger.info(messages.MESSAGE_PROCESS_ENDED)
        result_messages.append(messages.MESSAGE_PROCESS_ENDED)

        return True, str(result_messages)
