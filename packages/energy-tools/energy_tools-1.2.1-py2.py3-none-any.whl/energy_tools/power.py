from math import sqrt


def q(s=None, p=None, pf=None):
    """Calculates the reactive power `p` (unitless) from the apparent power `s`,
    the active power `p`, or the power factor `pf` (2 values required).
    """

    if pf is not None:
        if not -1 <= pf <= 1:
            raise ValueError("PF must be between -1 and 1.")

    if p is not None and pf is not None:
        return sqrt(p**2 * ((1 / pf**2) - 1))

    if s is not None and pf is not None:
        return sqrt(s**2 - (s * pf) ** 2)

    if p is not None and s is not None:
        return sqrt(s**2 - p**2)

    raise ValueError("You must provide at least two arguments.")


def p(s=None, q=None, pf=None):
    """Calculates the active power `p` (unitless) from the apparent power `s`,
    the reactive power `q`, or the power factor `pf` (2 values required).
    """

    if pf is not None:
        if not -1 <= pf <= 1:
            raise ValueError("PF must be between -1 and 1.")

    if q is not None and pf is not None:
        return sqrt(q**2 / ((1 / pf**2) - 1))

    if s is not None and pf is not None:
        return s * pf

    if q is not None and s is not None:
        return sqrt(s**2 - q**2)

    raise ValueError("You must provide at least two arguments.")
