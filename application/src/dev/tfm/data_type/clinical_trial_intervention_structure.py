from tfm.data_type.ct_intervention_type import InterventionType


class ClinicalTrialInterventionStructure:
    name: list
    type: InterventionType
    description: str

    def __init__(self):
        self.name = []

