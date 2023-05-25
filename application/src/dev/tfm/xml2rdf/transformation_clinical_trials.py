import xml.etree.ElementTree as Et

from config import xml_paths
from tfm.data_type.clinical_trial_intervention_structure import ClinicalTrialInterventionStructure
from tfm.data_type.clinical_trial_location_structure import ClinicalTrialLocationStructure
from tfm.data_type.clinical_trial_outcome_structure import ClinicalTrialOutcomeStructure
from tfm.data_type.clinical_trial_person_structure import ClinicalTrialPersonStructure
from tfm.data_type.clinical_trial_structure import ClinicalTrialStructure
from tfm.data_type.ct_study_type import StudyType
from utils.utils import Utils


class TransformationClinicalTrials:

    @staticmethod
    def xml2clinical_trials(xml_path: str):
        """
            Save the XML data into the ClinicalTrialsStructure.

            Parameters:
                xml_path (str): Path to a specific XML.

            Returns:
                ClinicalTrialStructure
        """

        clinical_trial = ClinicalTrialStructure()
        tree = Et.parse(xml_path)
        root = tree.getroot()

        TransformationClinicalTrials.xml2description(root, clinical_trial)

        TransformationClinicalTrials.xml2study_type(root, clinical_trial)

        TransformationClinicalTrials.xml2conditions(root, clinical_trial)

        TransformationClinicalTrials.xml2interventions(root, clinical_trial)

        TransformationClinicalTrials.xml2status(root, clinical_trial)

        TransformationClinicalTrials.xml2participants(root, clinical_trial)

        TransformationClinicalTrials.xml2collaborators(root, clinical_trial)

        return clinical_trial

    @staticmethod
    def xml2description(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to identified and description into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        # Identifier
        clinical_trial.identifier = Utils.get_text(root.find(xml_paths.IDENTIFIER))

        # Description
        clinical_trial.brief_title = Utils.get_text(root.find(xml_paths.BRIEF_TITLE))
        clinical_trial.official_title = Utils.get_text(root.find(xml_paths.OFFICIAL_TITLE))
        clinical_trial.brief_summary = Utils.get_text(root.find(xml_paths.BRIEF_SUMMARY))
        clinical_trial.summary = Utils.get_text(root.find(xml_paths.SUMMARY))

    @staticmethod
    def xml2study_type(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to study type into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        # Design
        clinical_trial.study_type = Utils.get_enum(root.find(xml_paths.STUDY_TYPE), "STUDY")

        if clinical_trial.study_type.name == StudyType.OBSERVATIONAL.name:
            for attr in root.findall(xml_paths.OBSERVATIONAL_MODE):
                obj = Utils.get_enum(attr, "OBS_MODE")

                if obj is not None:
                    clinical_trial.objective.append(obj)

        if clinical_trial.study_type.name == StudyType.INTERVENTIONAL.name:
            obj = Utils.get_enum(root.find(xml_paths.OBJECTIVE), "INT_MODE")

            if obj is not None:
                clinical_trial.objective.append(obj)

    @staticmethod
    def xml2conditions(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to conditions into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        for attr in root.findall(xml_paths.CONDITIONS):
            clinical_trial.conditions.append(attr.text)

        if len(clinical_trial.conditions) > 0:
            clinical_trial.conditions = list(set(clinical_trial.conditions))

        relevance_high = []
        for attr in root.findall(xml_paths.KEYWORDS_RELEVANCE):
            relevance = Utils.get_text(attr)

            if relevance is not None and relevance == 'high':
                relevance_high.append(True)
            else:
                relevance_high.append(False)

        i = 0
        for attr in root.findall(xml_paths.KEYWORDS):
            kw = Utils.split_and_normalise_text(attr)
            if relevance_high[i] is True:
                clinical_trial.keywords += kw
            else:
                clinical_trial.keywords_low += kw
            i += 1

    @staticmethod
    def xml2interventions(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to interventions into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        relevance_high = []
        for attr in root.findall(xml_paths.KEYWORDS_INTERVENTION_RELEVANCE):
            relevance = Utils.get_text(attr)

            if relevance is not None and relevance == 'high':
                relevance_high.append(True)
            else:
                relevance_high.append(False)

        i = 0
        for attr in root.findall(xml_paths.KEYWORDS_INTERVENTION):
            kw = Utils.split_and_normalise_text(attr)
            if relevance_high[i] is True:
                clinical_trial.keywords_intervention += kw
            else:
                clinical_trial.keywords_intervention_low += kw
            i += 1

        if len(clinical_trial.keywords) > 0:
            clinical_trial.keywords = list(set(clinical_trial.keywords))

    @staticmethod
    def xml2status(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to status into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        for attr in root.findall(xml_paths.STUDY_PHASE):
            clinical_trial.phases.append(Utils.get_enum(attr, "PHASE"))

        if len(clinical_trial.phases) > 0:
            clinical_trial.phases = list(set(clinical_trial.phases))

        # Status
        clinical_trial.recruiting_status = Utils.get_enum(root.find(xml_paths.RECRUITING_STATUS), "RECRUITING")
        clinical_trial.start_date = Utils.get_date(root.find(xml_paths.START_DATE))
        clinical_trial.end_date = Utils.get_date(root.find(xml_paths.END_DATE))
        clinical_trial.primary_end_date = Utils.get_date(root.find(xml_paths.PRIMARY_END_DATE))

    @staticmethod
    def xml2participants(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to status into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        # Participants
        clinical_trial.number_participants = Utils.get_int(root.find(xml_paths.NUM_PARTICIPANTS))
        for attr in root.findall(xml_paths.INTERVENTIONS):
            ct_intervention = ClinicalTrialInterventionStructure()

            ct_intervention.name = Utils.split_and_normalise_text(attr.find(xml_paths.INTERVENTION_NAME))
            ct_intervention.description = Utils.get_text(attr.find(xml_paths.INTERVENTION_DESCR))
            ct_intervention.type = Utils.get_enum(attr.find(xml_paths.INTERVENTION_TYPE), "INTERVENTION")
            clinical_trial.interventions.append(ct_intervention)

        for attr in root.findall(xml_paths.OUTCOMES):
            ct_outcome = ClinicalTrialOutcomeStructure()
            ct_outcome.name = Utils.get_text(attr.find(xml_paths.OUTCOME_NAME))
            ct_outcome.description = Utils.get_text(attr.find(xml_paths.OUTCOME_DESCR))
            ct_outcome.time = Utils.get_text(attr.find(xml_paths.OUTCOME_TIME))

            clinical_trial.outcomes.append(ct_outcome)

        # Eligibility criteria
        clinical_trial.eligibility_criteria = Utils.get_text(root.find(xml_paths.CRITERIA))
        clinical_trial.gender = Utils.get_enum(root.find(xml_paths.GENDER), "GENDER")
        clinical_trial.maximum_age = Utils.get_text(root.find(xml_paths.MAX_AGE))
        clinical_trial.minimum_age = Utils.get_text(root.find(xml_paths.MIN_AGE))

    @staticmethod
    def xml2collaborators(root: Et.ElementTree, clinical_trial: ClinicalTrialStructure):
        """
            Save the XML data related to status into the ClinicalTrialsStructure.

            Parameters:
                root (xml.etree.ElementTree.ElementTree): Root element of the XML.
                clinical_trial (ClinicalTrialStructure): Clinical Trial Structure to store the XML data.

            Returns:
                None
        """
        # Sponsors
        clinical_trial.sponsor_name = Utils.get_text(root.find(xml_paths.SPONSOR_NAME))
        clinical_trial.sponsor_class = Utils.get_enum(root.find(xml_paths.SPONSOR_CLASS), "SPONSOR")

        # INVESTIGATORS
        for attr in root.findall(xml_paths.CONTACT_PERSONS):
            ct_person = ClinicalTrialPersonStructure()
            ct_person.name = Utils.get_text(attr.find(xml_paths.CONTACT_NAME))
            ct_person.role = Utils.get_text(attr.find(xml_paths.CONTACT_ROLE))
            ct_person.email = Utils.get_text(attr.find(xml_paths.CONTACT_EMAIL))
            ct_person.telephone = Utils.get_text(attr.find(xml_paths.CONTACT_PHONE))
            clinical_trial.contact_persons.append(ct_person)

        ct_inv = ClinicalTrialPersonStructure()
        ct_inv.name = Utils.get_text(root.find(xml_paths.RESPONSIBLE_NAME))
        ct_inv.affiliation = Utils.get_text(root.find(xml_paths.RESPONSIBLE_ORG))
        ct_inv.role = Utils.get_text(root.find(xml_paths.RESPONSIBLE_TYPE))
        clinical_trial.principal_investigator.append(ct_inv)

        investigator_names = [ct_inv.name]

        for attr in root.findall(xml_paths.PRINCIPAL_INVESTIGATORS):
            ct_inv = ClinicalTrialPersonStructure()
            investigator_name = Utils.get_text(attr.find(xml_paths.INVESTIGATOR_NAME))

            if investigator_name not in investigator_names:
                ct_inv.name = Utils.get_text(attr.find(xml_paths.INVESTIGATOR_NAME))
                ct_inv.role = Utils.get_text(attr.find(xml_paths.INVESTIGATOR_ROLE))
                ct_inv.affiliation = Utils.get_text(attr.find(xml_paths.INVESTIGATOR_AFFILIATION))
                clinical_trial.principal_investigator.append(ct_inv)

        for attr in root.findall(xml_paths.LOCATIONS):
            ct_location = ClinicalTrialLocationStructure()
            ct_location.city = Utils.get_text(attr.find(xml_paths.LOCATION_CITY))
            ct_location.country = Utils.get_text(attr.find(xml_paths.LOCATION_COUNTRY))
            ct_location.facility = Utils.get_text(attr.find(xml_paths.LOCATION_FACILITY))
            ct_location.postcode = Utils.get_text(attr.find(xml_paths.LOCATION_POSTCODE))
            ct_location.collaborators = []

            for attr2 in attr.findall(xml_paths.LOCATION_COLLABORATORS):
                ct_person = ClinicalTrialPersonStructure()
                ct_person.name = Utils.get_text(attr2.find(xml_paths.LOCATION_COLLAB_NAME))
                ct_person.role = Utils.get_text(attr2.find(xml_paths.LOCATION_COLLAB_ROLE))
                ct_person.email = Utils.get_text(attr2.find(xml_paths.LOCATION_COLLAB_EMAIL))
                ct_person.telephone = Utils.get_text(attr2.find(xml_paths.LOCATION_COLLAB_PHONE))
                ct_location.collaborators.append(ct_person)
            clinical_trial.locations.append(ct_location)
