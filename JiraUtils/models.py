from pydantic import BaseModel, Field

class Session(BaseModel):
    name: str
    value: str

class SessionResponse(BaseModel):
    session: Session

class NameField(BaseModel):
    name: str

class ValueField(BaseModel):
    value: str

class Fields(BaseModel):
    project: NameField
    issue_type: NameField = Field(..., alias='issuetype')
    summary: str
    description: str

class Issue(BaseModel):
    key: str
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
