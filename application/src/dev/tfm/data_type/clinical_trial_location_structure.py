from tfm.data_type.clinical_trial_person_structure import ClinicalTrialPersonStructure


class ClinicalTrialLocationStructure:
    facility: str
    city: str
    country: str
    postcode: str
    collaborators: list[ClinicalTrialPersonStructure]

    def __init__(self):
        self.collaborators = []

