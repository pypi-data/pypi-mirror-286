import typing as t
from datetime import datetime
from pydantic import (BaseModel, HttpUrl, field_validator,
                      IPvAnyAddress, Field, ValidationError,
                      ConfigDict)


class Event(BaseModel):
    name: str = Field(max_length=32)
    siteId: str = Field(max_length=16)
    sourceIp: IPvAnyAddress
    time: str

    @field_validator('time')
    @classmethod
    def validate_time(cls, time: str):
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return time

    @property
    def py_time(self):
        return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%SZ")


class UserGeneratedEvent(Event):
    model_config = ConfigDict(extra="allow")

    # all fields not associated with
    name: str = Field(max_length=32)

    @field_validator('name')
    @classmethod
    def validate_name(cls, name: str):
        if not name.startswith("u-"):
            raise ValidationError
        return name


class PageViewEvent(Event):
    name: t.Literal['PageView']
    pageUrl: HttpUrl
    referrer: str = ""
    prevUrl: str = ""


def test_user_generated_event():
    m = UserGeneratedEvent.model_validate(
        {'name': 'u-hello',
         'siteId': "123",
         "sourceIp": "192.168.1.2",
         "time": "2004-04-02T10:10:10Z",
         "hello": "world"})
    assert "hello" in m.model_dump(mode='json'), "hello not in model"
