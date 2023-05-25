from enum import Enum


class RecruitingStatus(Enum):
    NOT_YET_RECRUITING = 1
    RECRUITING = 2
    ENROLLING_BY_INVITATION = 3
    ACTIVE_NOT_RECRUITING = 4
    COMPLETED = 5
    SUSPENDED = 6
    TERMINATED = 7
    WITHDRAWN = 8
