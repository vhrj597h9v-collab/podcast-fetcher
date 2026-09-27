"""Tr8x2 thumbscrew (tilt)."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_TILT, P.TS_KNOB_D_TILT)
