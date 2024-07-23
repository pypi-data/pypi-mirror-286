# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from themoviedb.schemas._enums import MediaType, SizeType


@dataclass
class PartialCompany:
    id: Optional[int] = None
    logo_path: Optional[str] = None
    name: Optional[str] = None

    def __str__(self) -> str:
        return self.name or ""

    def logo_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.logo_path}" if self.logo_path else None


@dataclass
class PartialCollection:
    id: Optional[int] = None
    backdrop_path: Optional[str] = None
    name: Optional[str] = None
    poster_path: Optional[str] = None

    def __str__(self) -> str:
        return self.name or ""

    def backdrop_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.backdrop_path}" if self.backdrop_path else None

    def poster_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.poster_path}" if self.poster_path else None


@dataclass
class PartialKeyword:
    id: Optional[int] = None
    name: Optional[str] = None

    def __str__(self) -> str:
        return self.name or ""


@dataclass
class PartialMovie:
    id: Optional[int] = None
    poster_path: Optional[str] = None
    adult: Optional[bool] = None
    overview: Optional[str] = None
    release_date: Optional[date] = None
    genre_ids: Optional[List[int]] = None
    original_title: Optional[str] = None
    original_language: Optional[str] = None
    title: Optional[str] = None
    backdrop_path: Optional[str] = None
    popularity: Optional[float] = None
    vote_count: Optional[int] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    media_type: MediaType = MediaType.movie

    def __str__(self) -> str:
        return self.title or self.original_title or ""

    @property
    def year(self) -> Optional[int]:
        return self.release_date.year if self.release_date else None

    def backdrop_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.backdrop_path}" if self.backdrop_path else None

    def poster_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.poster_path}" if self.poster_path else None


@dataclass
class PartialNetwork:
    id: Optional[int] = None
    logo_path: Optional[str] = None
    name: Optional[str] = None
    origin_country: Optional[str] = None

    def __str__(self) -> str:
        return self.name or ""

    def logo_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.logo_path}" if self.logo_path else None


@dataclass
class PartialTV:
    id: Optional[int] = None
    poster_path: Optional[str] = None
    adult: Optional[bool] = None
    popularity: Optional[float] = None
    backdrop_path: Optional[str] = None
    vote_average: Optional[float] = None
    overview: Optional[str] = None
    first_air_date: Optional[date] = None
    origin_country: Optional[List[str]] = None
    genre_ids: Optional[List[int]] = None
    original_language: Optional[str] = None
    vote_count: Optional[int] = None
    name: Optional[str] = None
    original_name: Optional[str] = None
    media_type: MediaType = MediaType.tv

    def __str__(self) -> str:
        return self.name or self.original_name or ""

    @property
    def year(self) -> Optional[int]:
        return self.first_air_date.year if self.first_air_date else None

    def backdrop_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.backdrop_path}" if self.backdrop_path else None

    def poster_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.poster_path}" if self.poster_path else None


@dataclass
class PartialSeason:
    id: Optional[int] = None
    air_date: Optional[date] = None
    episode_count: Optional[int] = None
    name: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    season_number: Optional[int] = None

    def __str__(self) -> str:
        return self.name or ""

    def poster_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.poster_path}" if self.poster_path else None


@dataclass
class PartialEpisode:
    id: Optional[int] = None
    air_date: Optional[date] = None
    episode_number: Optional[int] = None
    name: Optional[str] = None
    overview: Optional[str] = None
    production_code: Optional[str] = None
    season_number: Optional[int] = None
    still_path: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    show_id: Optional[int] = None
    order: Optional[int] = None
    runtime: Optional[int] = None

    def __str__(self) -> str:
        return self.name or ""

    def still_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.still_path}" if self.still_path else None


@dataclass
class PartialMedia(PartialMovie, PartialTV):
    _id: Optional[str] = None


@dataclass
class PartialPerson:
    id: Optional[int] = None
    profile_path: Optional[str] = None
    adult: Optional[bool] = None
    known_for: Optional[List[PartialMedia]] = None
    known_for_department: Optional[str] = None
    gender: Optional[int] = None
    name: Optional[str] = None
    original_name: Optional[str] = None
    popularity: Optional[float] = None
    media_type: MediaType = MediaType.person

    def __str__(self) -> str:
        return self.name or self.original_name or ""

    def profile_url(self, size: SizeType = SizeType.original) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/{size.value}{self.profile_path}" if self.profile_path else None
