# -*- coding: utf-8 -*-
from themoviedb import schemas, utils
from themoviedb.routes_sync._base import Base


class Certifications(Base):
    def movie(self) -> schemas.Certifications:
        """Get an up to date list of the officially supported movie certifications on TMDB.

        See more: https://developers.themoviedb.org/3/certifications/get-movie-certifications
        """
        data = self.request("certification/movie/list")
        return utils.as_dataclass(schemas.Certifications, data)

    def tv(self) -> schemas.Certifications:
        """Get an up to date list of the officially supported TV show certifications on TMDB.

        See more: https://developers.themoviedb.org/3/certifications/get-tv-certifications
        """
        data = self.request("certification/tv/list")
        return utils.as_dataclass(schemas.Certifications, data)
