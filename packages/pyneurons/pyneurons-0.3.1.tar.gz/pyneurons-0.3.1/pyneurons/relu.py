from jax.numpy import maximum
from .vjp.identity import identity


@identity
def relu(x):
    return maximum(x, 0)
