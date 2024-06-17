from enum import Enum


# TODO CHECK IF ALL OF THE STRINGS ARE WRITTEN THIS WAY
class Classifications(Enum):
    RIGID = ("kind", "subkind", "category")
    ANTIRIGID = ("phase", "role", "phasemixin", "rolemixin")
    SEMIRIGID = ("mixin")
    SORTAL = ("kind", "subkind", "phase", "role")
    NONSORTAL = ("category", "phasemixin", "rolemixin", "mixin")
