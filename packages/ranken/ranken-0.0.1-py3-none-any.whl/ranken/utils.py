from scipy.optimize import minimize
import numpy as np

dagger = lambda x: np.conj(x).T

ROUNDOFF_TOL = 1e-6

def Loss(phi_rx, projector):
  left = dagger(phi_rx)
  right = phi_rx

  prod = np.dot(np.dot(left, projector), right)

  return np.real_if_close(prod, tol=ROUNDOFF_TOL)

def rand(max_val, size):
  return np.random.randint(-max_val, max_val, size=size)

def urand(max_val, size):
  return np.random.randint(0, max_val, size=size)

def minima(f, x0, **kwargs):
  if 'method' not in kwargs:
    kwargs['method'] = 'L-BFGS-B'

  if 'tol' not in kwargs:
    kwargs['tol'] = ROUNDOFF_TOL

  return minimize(f, x0=x0, **kwargs)