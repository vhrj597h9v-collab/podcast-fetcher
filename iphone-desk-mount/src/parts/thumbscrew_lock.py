"""Tr8x2 thumbscrew (lock)."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_LOCK, None)
