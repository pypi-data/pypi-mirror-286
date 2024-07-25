import numpy as np

normalise = lambda phi: phi / np.linalg.norm(phi)
dagger = lambda x: np.conj(x).T

def Qdit(order, coeffs):
  if len(coeffs) == order*2:
    # for [a,b,a,b] case
    psis = [coeffs[i] + 1j*coeffs[i+1] for i in range(0, len(coeffs), 2)]
  else:
    # for [[a,b][a,b]] case
    psis = [c[0] + 1j*c[1] for c in coeffs]

  return normalise(np.array(psis))



def Projector(basis):
  projector = np.array([
    np.outer(basis[i], dagger(basis[i]))
      for i in range(len(basis))
  ])

  perp = np.eye(len(basis[0])) - sum(projector)
  return projector, perp


class State:
  Ket_0 = np.array([1, 0])
  Ket_1 = np.array([0, 1])
  Ket_p = normalise(np.array([1, 1]))
  Ket_m = normalise(np.array([1, -1]))
  Ket_i = normalise(np.array([1, 1j]))
  Ket_mi = normalise(np.array([1, -1j]))

  def create(state, basis_vec):
    return np.kron(state, basis_vec)

  def combine(states, coeffs):
    if len(states) != len(coeffs):
      raise ValueError("states and coeffs must have the same length")
    return normalise(sum([coeffs[i]*states[i] for i in range(len(states))]))

def gs_cofficient(v1, v2):
  return np.dot(v2, v1) / np.dot(v1, v1)

def multiply(cofficient, v):
  return list(map((lambda x : x * cofficient), v))

def proj(v1, v2):
  return multiply(gs_cofficient(v1, v2) , v1)

# usage:
# subspace_basis = np.array([PSI(i) for i in range(2)])
# subspace_basis = gs(subspace_basis)
def GramSchmidt(X):
  Y = []
  for i in range(len(X)):
    temp_vec = X[i]
    for inY in Y :
      proj_vec = proj(inY, X[i])
      temp_vec = list(map(lambda x, y : x - y, temp_vec, proj_vec))
    Y.append(temp_vec)
  return Y