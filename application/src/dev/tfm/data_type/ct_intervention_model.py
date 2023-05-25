from enum import Enum


class InterventionModel(Enum):
    TREATMENT = 1
    PREVENTION = 2
    DIAGNOSTIC = 3
    SUPPORTIVE_CARE = 4
    SCREENING = 5
    HEALTH_SERVICES_RESEARCH = 6
    BASIC_SCIENCE = 7
    DEVICE_FEASIBILITY = 8
    OTHER = 9
