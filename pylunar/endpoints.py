from typing import Literal, Optional

from . import models
from .api import Endpoint, ep

@ep("gen/welcome", models.Image)
def generate_welcome(avatar: str, username: str):
    ...

@ep("gen/achievement", models.Image)
def generate_achievement(text: str, icon: Optional[int] = None):
    ...


@ep("gen/challenge", models.Image)
def generate_challenge(text: str, icon: Optional[int] = None):
    ...


@ep("gen/amiajoke", models.Image)
def generate_amiajoke(image: str):
    ...


@ep("gen/bad", models.Image)
def generate_bad(image: str):
    ...


@ep("gen/calling", models.Image)
def generate_calling(text: str):
    ...


__valid = Literal[
    "ahegao",
    "ass",
    "boobs",
    "cum",
    "gif",
    "hololive",
    "jpg",
    "neko",
    "panties",
    "thighs",
    "yuri",
]

__sfw_valid = Literal[
    "hug"
]


def nsfw(__name: __valid):
    return Endpoint(f"nsfw/{__name}", model=models.JSON, fn=lambda: None)

def sfw(__name: __sfw_valid):
    return Endpoint(f"sfw/{__name}", model=models.JSON, fn=lambda: None)