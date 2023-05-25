import os

from config import constants, messages
from tfm.data_type.clinical_trial_structure import ClinicalTrialStructure
from tfm.similarity import logger
from tfm.validate.file_manager import FileManager
from utils.utils import Utils

import pandas as pd


class TransformationTSV:
    clinical_trials: list[ClinicalTrialStructure]
    output_file: str
    output_folder: str
    output_tsv_data = dict
    conditions_not_processed = []

    def __init__(self, clinical_trials: list, result_path: str):
        self.clinical_trials = clinical_trials
        self.output_file = os.path.join(result_path, constants.TSV_FILE)
        self.output_folder = result_path
        self.output_tsv_data = {'target': [], 'source': [], 'weight': []}
        self.conditions_not_processed = ["BreastCancer", "BreastNeoplasms", "SkinDiseases", "BreastDiseases"]

    def process_to_tsv(self):
        """
            Method to create a TSV with all data from the clinical trials.

            Parameters:

            Returns:
                bool: Whether the TSV file has been generated correctly or not.
                str: Message with the status of the process.
        """
        try:
            for clinical_trial in self.clinical_trials:
                self.transformation_rdf2triples(clinical_trial)

            FileManager.create_folder(self.output_folder)
            FileManager.remove_file(self.output_file)
            df = pd.DataFrame(self.output_tsv_data)
            df.to_csv(self.output_file, sep="\t", index=False)

        except Exception as ex:
            message = messages.MESSAGE_TSV_KO
            logger.error(messages.MESSAGE_TSV_KO + ex.__str__())
            return False, message

        return True, messages.MESSAGE_TSV_OK

    def transformation_rdf2triples(self, clinical_trial: ClinicalTrialStructure):
        """
            Method to create the triples from a clinical trial.

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.

            Returns:
                None
        """
        ct_identifier = "ClinicalTrial::" + clinical_trial.identifier

        # Objective
        for objective in clinical_trial.objective:
            self.output_tsv_data['target'].append(ct_identifier)
            self.output_tsv_data['source'].append(Utils.normalise_text(objective.name))
            self.output_tsv_data['weight'].append(0.2)

        # Intervention
        interventions = [x.name for x in clinical_trial.interventions]
        interventions = sum(interventions, [])
        interventions = [Utils.normalise_text(x) for x in list(set(interventions))]
        for intervention in interventions:
            self.output_tsv_data['target'].append(ct_identifier)
            self.output_tsv_data['source'].append(intervention)
            self.output_tsv_data['weight'].append(1)

        # Health Condition
        conditions = [Utils.normalise_text(x) for x in list(set(clinical_trial.conditions))]
        for condition in conditions:
            if condition not in self.conditions_not_processed and condition not in interventions:
                self.output_tsv_data['target'].append(ct_identifier)
                self.output_tsv_data['source'].append(condition)
                self.output_tsv_data['weight'].append(0.5)

        # Keywords condition - high relevance
        keywords = [Utils.normalise_text(x) for x in list(set(clinical_trial.keywords))]
        for keyword in keywords:
            if keyword not in conditions and keyword not in self.conditions_not_processed:
                self.output_tsv_data['target'].append(ct_identifier)
                self.output_tsv_data['source'].append(keyword)
                self.output_tsv_data['weight'].append(0.5)

        keywords_low = [Utils.normalise_text(x) for x in list(set(clinical_trial.keywords_low))]
        for keyword in keywords_low:
            if keyword not in conditions and keyword not in self.conditions_not_processed:
                self.output_tsv_data['target'].append(ct_identifier)
                self.output_tsv_data['source'].append(keyword)
                self.output_tsv_data['weight'].append(0.2)

        # Keywords intervention - high relevance
        keywords = [Utils.normalise_text(x) for x in list(set(clinical_trial.keywords_intervention))]
        for keyword in keywords:
            if keyword not in interventions:
                self.output_tsv_data['target'].append(ct_identifier)
                self.output_tsv_data['source'].append(keyword)
                self.output_tsv_data['weight'].append(0.7)

        keywords_low = [Utils.normalise_text(x) for x in list(set(clinical_trial.keywords_intervention_low))]
        for keyword in keywords_low:
            if keyword not in interventions:
                self.output_tsv_data['target'].append(ct_identifier)
                self.output_tsv_data['source'].append(keyword)
                self.output_tsv_data['weight'].append(0.3)

