from jax.numpy import abs as function
from .vjp.sign import sign

abs = sign(function)
