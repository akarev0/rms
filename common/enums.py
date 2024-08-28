from enum import IntEnum, StrEnum


class EmployeeLevel(StrEnum):
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    ARCHITECT = "Architect"

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
    BA = "BA"
    BE_DOT_NET = "BE .Net"
    BE_HYBRIS = "BE Hybris"
    BE_JAVA = "BE Java"
    BE_NODE = "BE Node"
    BE_PYTHON = "BE Python"
    BE_SCALA = "BE Scala"
    DATA_SCIENTIST = "Data Scientist"
    DEVOPS = "DevOps"
    FE = "FE"
    FE_HYBRIS = "FE Hybris"
    PE_PLATFORMS = "PE Platforms"
    FS_DOT_NET = "FS .Net"
    FS_JAVA = "FS Java"
    FS_NODE = "FS Node"
    FS_PHP = "FS PHP"
    FS_PYTHON = "FS Python"
    MOBILE_HYBRID = "Mobile Hybrid"
    MOBILE_NATIVE = "Mobile Native"
    PM = "PM"
    QA = "QA"
    UI_UX_DESIGNER = "UI\\UX Designer"
    MANAGER = "Manager"
    DEVELOPER = "Developer"
    DESIGNER = "Designer"
    HR = "HR"
    UNKNOWN = "Unknown"

    def _missing_(self, value):
        return Position.UNKNOWN
