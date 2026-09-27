"""Tr10x2.5 tilt thumbscrew with a 50 x 14 T-bar, 42 mm thread (through the near ear, the tongue nut and the far ear)."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_TILT, P.TS_TBAR_L_TILT, P.TS_TBAR_W_TILT, P.TS_TBAR_H_TILT, P.TILT_D, P.TILT_P)
