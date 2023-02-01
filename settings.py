import os
import sys
from dataclasses import dataclass

from environs import Env

os.chdir(sys.path[0])


@dataclass()
class Db:
    user: str
    password: str
    database: str
    host: str


@dataclass()
class Link:
    link_to_pars: str


@dataclass()
class Settings:
    db: Db
    link: Link


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return (Settings(
        db=Db(
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_DATABASE"),
            host=env.str("DB_HOST")
        ),
        link=Link(
            link_to_pars=env.str("LINK_TO_PARSING")
        )
    ))


settings = get_settings('inp_sett')
