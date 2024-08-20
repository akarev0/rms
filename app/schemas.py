from pydantic import BaseModel, ConfigDict, Field


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseSchemaModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponseModel(UserBase):
    id: int


class EmployeeResponseMode(BaseSchemaModel):
    id: int
    name: str
    email: str
    position: str
    level: str
    english_level: str
    sales_campaign: str
    other_skills: list[str]
    team: str
    attendance_link: str
    last_interview: str
    skills: list[str]


class ResourceBase(BaseSchemaModel):
    name: str
    description: str


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int
    owner_id: int


class TeamResponseModel(BaseSchemaModel):
    id: int
    name: str
    leader_id: int
    employees: list[EmployeeResponseMode] | None = Field(default_factory=list)


class TeamCreate(BaseSchemaModel):
    name: str
    leader_id: int
    employees: list[int] = Field(default_factory=list)
