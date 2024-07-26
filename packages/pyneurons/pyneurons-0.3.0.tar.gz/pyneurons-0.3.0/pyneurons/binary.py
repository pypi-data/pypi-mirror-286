from jax.numpy import heaviside
from .vjp.identity import identity


@identity
def binary(x):
    return heaviside(x, 1)
