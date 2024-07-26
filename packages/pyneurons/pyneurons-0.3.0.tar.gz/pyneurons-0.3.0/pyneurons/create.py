from jax.numpy import ndarray
from multipledispatch import dispatch
from .random.key import key as random_key
from .random.weight import weight
from .random.bias import bias


@dispatch(ndarray, int)
def create(key, n):
    return (weight(key, (n, 1)), bias(key, (1, 1)))


@dispatch(int)
def create(n):
    return create(random_key(), n)
