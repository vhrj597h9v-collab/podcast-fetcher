"""Tr8x2.5 cradle-retaining thumbscrew (T-bar), 60 mm thread: through the carrier and boss into the cradle thread."""
import params as P
from parts._thumbscrew import thumbscrew


def build():
    return thumbscrew(P.TS_LEN_RETAIN)
