from datetime import date

from tfm.data_type.clinical_trial_intervention_structure import ClinicalTrialInterventionStructure
from tfm.data_type.clinical_trial_location_structure import ClinicalTrialLocationStructure
from tfm.data_type.clinical_trial_outcome_structure import ClinicalTrialOutcomeStructure
from tfm.data_type.clinical_trial_person_structure import ClinicalTrialPersonStructure
from tfm.data_type.ct_gender import GenderType
from tfm.data_type.ct_phases import PhasesType
from tfm.data_type.ct_recruiting_status import RecruitingStatus
from tfm.data_type.ct_sponsor import SponsorClass
from tfm.data_type.ct_study_type import StudyType


class ClinicalTrialStructure:
    filename: str

    identifier: str

    brief_title: str
    official_title: str
    brief_summary: str
    summary: str

    conditions: list[str]
    keywords: list[str]
    keywords_low: list[str]
    keywords_intervention: list[str]
    keywords_intervention_low: list[str]
    study_type: StudyType
    phases: list[PhasesType]
    objective: list[str]

    recruiting_status: RecruitingStatus
    start_date: date
    end_date: date
    primary_end_date: date

    sponsor_name: str
    sponsor_class: SponsorClass     # Discarded

    number_participants: int
    interventions: list[ClinicalTrialInterventionStructure]
    outcomes: list[ClinicalTrialOutcomeStructure]

    eligibility_criteria: str
    gender: GenderType
    maximum_age: int
    minimum_age: int

    contact_persons: list[ClinicalTrialPersonStructure]
    principal_investigator: list[ClinicalTrialPersonStructure]
    locations: list[ClinicalTrialLocationStructure]

    def __init__(self):
        self.conditions = []
        self.keywords = []
        self.keywords_low = []
        self.keywords_intervention = []
        self.keywords_intervention_low = []
        self.phases = []
        self.interventions = []
        self.outcomes = []
        self.contact_persons = []
        self.principal_investigator = []
        self.locations = []
        self.objective = []
