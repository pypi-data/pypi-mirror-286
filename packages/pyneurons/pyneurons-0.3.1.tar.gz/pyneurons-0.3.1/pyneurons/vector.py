from .vjp.identity import identity
from .binary import binary
from .relu1 import relu1


@identity
def vector(x):
    return binary(x) + relu1(x)
