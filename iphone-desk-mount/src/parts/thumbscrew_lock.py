"""Tr8x2.5 slider-lock thumbscrew (T-bar), 26 mm thread."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_LOCK)
