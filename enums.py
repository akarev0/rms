from enum import IntEnum, StrEnum


class EmployeeLevel(IntEnum):
    JUNIOR = 1
    MIDDLE = 2
    SENIOR = 3

    def __str__(self):
        return self.name


class EmployeeEnglishLevel(StrEnum):
    ELEMENTARY = "Elementary"
    PRE_INTERMEDIATE = "Pre-Intermediate"
    INTERMEDIATE = "Intermediate"
    UPPER_INTERMEDIATE = "Upper-Intermediate"
    ADVANCED = "Advanced"
    PROFICIENT = "Proficient"

    def __str__(self):
        return self.name


class Position(StrEnum):
    MANAGER = "Manager"
    DEVELOPER = "Developer"
    DESIGNER = "Designer"
    QA = "QA"
    HR = "HR"
