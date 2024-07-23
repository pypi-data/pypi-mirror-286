# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from themoviedb.schemas._result import Result


@dataclass
class Certification:
    certification: Optional[str] = None
    meaning: Optional[str] = None
    order: Optional[int] = None


@dataclass
class Certifications(Result[Optional[Dict[str, List[Certification]]]]):
    certifications: Optional[Dict[str, List[Certification]]] = field(default=None)

    def __post_init__(self) -> None:
        self.results = self.certifications

    def __bool__(self) -> bool:
        return bool(self.results)

    def __getitem__(self, region: str) -> List[Certification]:
        if self.results is None:
            raise KeyError(f"Region {region} not found")
        return self.results[region]

    @property
    def regions(self) -> List[str]:
        if self.results is None:
            return []
        return list(self.results.keys())
