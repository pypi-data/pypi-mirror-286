# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, List, Optional

from themoviedb.schemas._enums import SizeType
from themoviedb.schemas._result import Result, ResultWithID


@dataclass
class WatchProviderData:
    display_priority: Optional[int] = None
    logo_path: Optional[str] = None
    provider_name: Optional[str] = None
    provider_id: Optional[int] = None

    def __str__(self) -> str:
        return self.provider_name or ""

    def logo_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.logo_path}" if self.logo_path else None


@dataclass
class WatchProvidersData(Result[WatchProviderData]):
    results: Optional[List[WatchProviderData]] = None  # type: ignore


@dataclass
class WatchProvider:
    link: Optional[str] = None
    ads: Optional[List[WatchProviderData]] = None
    buy: Optional[List[WatchProviderData]] = None
    flatrate: Optional[List[WatchProviderData]] = None
    free: Optional[List[WatchProviderData]] = None
    rent: Optional[List[WatchProviderData]] = None

    def __bool__(self) -> bool:
        return bool(self.buy or self.flatrate or self.free)


@dataclass
class WatchProviders(ResultWithID):
    results: Optional[Dict[str, WatchProvider]] = None

    def __bool__(self) -> bool:
        return bool(self.results)

    def __getitem__(self, region: str) -> WatchProvider:
        if self.results is None:
            raise KeyError(f"Region {region} not found")
        return self.results[region]

    @property
    def regions(self) -> List[str]:
        if self.results is None:
            return []
        return list(self.results.keys())
