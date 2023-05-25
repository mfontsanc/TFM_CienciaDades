from enum import Enum


class ObservationalModel(Enum):
    COHORT = 1
    CASE_CONTROL = 2
    CASE_ONLY = 3
    CASE_CROSSOVER = 4
    ECOLOGIC_OR_COMMUNITY = 5
    COMMUNITY_STUDIES = 6
    FAMILY_BASED = 7
    DEFINED_POPULATION = 8
    OTHER = 9
