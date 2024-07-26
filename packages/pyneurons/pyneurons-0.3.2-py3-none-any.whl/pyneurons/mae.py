from jax.numpy import mean
from .abs import abs


def mae(y, yhat):
    return mean(abs(y - yhat))
