"""Tr10x2.5 cradle-retaining thumbscrew (40 x 12 T-bar), 66 mm thread: through the carrier and boss into the cradle thread."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_RETAIN, None, None, None, P.RETAIN_D, P.RETAIN_P)
