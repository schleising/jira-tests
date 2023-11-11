from enum import Enum

from pydantic import BaseModel, Field

class IssueType(str, Enum):
    bug = 'Bug'
    epic = 'Epic'
    story = 'Story'

    def __str__(self) -> str:
        return self.value

class Session(BaseModel):
    name: str
    value: str

class SessionResponse(BaseModel):
    session: Session

class CreateIssueResponse(BaseModel):
    id: str
    key: str
    self: str

class CreateIssueErrorResponse(BaseModel):
    errorMessages: list[str]
    errors: dict[str, str]

class IdField(BaseModel):
    id: str

class NameField(BaseModel):
    name: str

class ValueField(BaseModel):
    value: str

class KeyField(BaseModel):
    key: str

class StatusType(str, Enum):
    backlog = 'Backlog'
    selected_for_development = 'Selected for Development'
    in_progress = 'In Progress'
    done = 'Done'

    def __str__(self) -> str:
        return self.value

class StatusField(BaseModel):
    name: StatusType

class Fields(BaseModel):
    project: IdField
    issue_type: NameField = Field(..., alias='issuetype')
    summary: str
    description: str
    status: StatusField | None = None
    epic_name: str | None = Field(default=None, serialization_alias='customfield_10103')

class IssueLinks(BaseModel):
    inwardIssue: KeyField
    outwardIssue: KeyField
    type: NameField = NameField(name='Relates')

class Issue(BaseModel):
    key: str | None = None
    fields: Fields

    def __str__(self):
        return f'{self.key} - {self.fields.summary} - {self.fields.status.name if self.fields.status is not None else None}'

    @property
    def issue_key(self) -> str | None:
        return self.key

    @property
    def project(self) -> str:
        return self.fields.project.id
    
    @property
    def issue_type(self) -> str:
        return self.fields.issue_type.name

    @property
    def summary(self) -> str:
        return self.fields.summary
    
    @property
    def description(self) -> str:
        return self.fields.description
    
    @property
    def status(self) -> str | None:
        return self.fields.status.name if self.fields.status is not None else None
