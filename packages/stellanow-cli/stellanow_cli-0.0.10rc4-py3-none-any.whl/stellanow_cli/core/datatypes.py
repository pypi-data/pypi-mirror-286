"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class StellaFormattedDateTime:
    createdAt: str
    updatedAt: str

    def __post_init__(self):
        self.createdAt = self.format_date(self.createdAt)
        self.updatedAt = self.format_date(self.updatedAt)

    @staticmethod
    def format_date(date_str: str) -> str:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class StellaEntity:
    id: str
    name: str


@dataclass
class StellaBaseFieldType:
    value: str


@dataclass
class StellaFieldType(StellaBaseFieldType):
    modelRef: Optional[str] = None


@dataclass
class StellaSubField:
    id: str
    name: str
    fieldType: StellaFieldType
    required: bool
    path: str


@dataclass
class StellaField:
    id: str
    name: str
    fieldType: StellaFieldType
    required: bool
    subfields: Optional[List[StellaSubField]] = None


@dataclass
class StellaModelField:
    id: str
    modelId: str
    name: str
    fieldType: StellaFieldType


@dataclass
class StellaEvent(StellaFormattedDateTime):
    id: str
    name: str
    isActive: bool


@dataclass
class StellaEventDetailed(StellaEvent):
    description: str
    fields: List[StellaField]
    entities: List[StellaEntity]


@dataclass
class StellaModel(StellaFormattedDateTime):
    id: str
    name: str


@dataclass
class StellaModelDetailed(StellaModel):
    description: str
    fields: List[StellaModelField]
