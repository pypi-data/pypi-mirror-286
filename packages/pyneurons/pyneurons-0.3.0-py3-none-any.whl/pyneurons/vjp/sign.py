from jax.numpy import sign as sign_function
from jax import custom_vjp


def sign(function):
    wrapper = custom_vjp(function)

    def forward(x):
        return function(x), x

    def backward(x, gradient):
        return (gradient * sign_function(x),)

    wrapper.defvjp(forward, backward)
    return wrapper
