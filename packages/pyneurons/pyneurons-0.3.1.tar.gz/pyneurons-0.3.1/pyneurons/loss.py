from .mae import mae


def loss(model, x, y):
    yhat = model(x)
    return mae(y, yhat)
