from pydantic import BaseModel, Field

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

class Fields(BaseModel):
    project: IdField
    issue_type: NameField = Field(..., alias='issuetype')
    summary: str
    description: str

class Issue(BaseModel):
    key: str | None = None
    fields: Fields

    def __str__(self):
        return f'{self.key}: {self.fields.summary}'

    @property
    def issue_key(self):
        return self.key

    @property
    def project(self):
        return self.fields.project
    
    @property
    def issue_type(self):
        return self.fields.issue_type

    @property
    def summary(self):
        return self.fields.summary
    
    @property
    def description(self):
        return self.fields.description
