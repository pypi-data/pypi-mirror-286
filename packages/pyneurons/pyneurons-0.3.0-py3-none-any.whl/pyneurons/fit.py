from functools import partial
from jax.tree_util import tree_map
from jax import grad
from .loss import loss
from .gd import gd


def fit(learning_rate, model, x, y):
    gradients = grad(loss)(model, x, y)
    return tree_map(partial(gd, learning_rate), model, gradients)
