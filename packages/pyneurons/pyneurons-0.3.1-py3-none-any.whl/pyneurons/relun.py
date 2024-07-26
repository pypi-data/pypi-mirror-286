from jax.numpy import minimum
from .vjp.identity import identity
from .relu import relu


def relun(n):
    @identity
    def function(x):
        return minimum(relu(x), n)

    return function
