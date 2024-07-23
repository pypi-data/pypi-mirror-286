import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.linear_model import LogisticRegression
import qiskit as qk
from qiskit_aer import Aer
from qiskit import transpile
import numpy as np

def encode(X, layers=2):
    """
    Apply angle encoding to classical dataset
    """
    n_qubits = X.shape[0]
    q = qk.QuantumRegister(n_qubits)
    c = qk.ClassicalRegister(1)
    qc = qk.QuantumCircuit(q, c)

    for l in range(layers):
        for qubit, x in enumerate(X):
            qc.h(qubit)
            qc.rz(2 * x, qubit)

        for qubit in range(n_qubits - 1):
            qc.cx(qubit, qubit + 1)
            qc.rz((1 - X[qubit]) * (1 - X[qubit + 1]), qubit + 1)
            qc.cx(qubit, qubit + 1)

    return qc, c

def variational_circuit(qc, theta):
    """
    Define the variational circuit
    """
    n_qubits = qc.num_qubits

    for qubit in range(n_qubits):
        qc.ry(theta[qubit], qubit)

    for qubit in range(n_qubits - 1):
        qc.cx(qubit, qubit + 1)

    for qubit in range(n_qubits):
        qc.ry(theta[qubit + n_qubits], qubit)

    return qc

def qnn(X, theta, shots=int(1e3)):
    """
    Define the quantum neural network
    """
    qc, c = encode(X)
    qc = variational_circuit(qc, theta)
    qc.measure(0, c)

    backend = Aer.get_backend("qasm_simulator")
    circuits = transpile(qc, backend)
    job = backend.run(circuits, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)
    return counts["1"] / shots

def optimize(X_train, Y_train, a= 2.5, c = 0.25, maxiter = 1e3, shots = int(1e4), alpha = 0.602, gamma = 0.101):
  f = lambda x: objective(x, X_train, Y_train, shots=shots)  # Objective function
  x0 = np.pi * np.random.randn(4)

  xsol = spsa(f, x0, a=a, c=c,
              alpha=alpha, gamma=gamma,
              maxiter=maxiter, verbose=True)
  return xsol

def objective(theta, X, Y, shots=int(1e4)):
  """
  Calculates the objective value for a given set of parameters, input data, and target values.

  Parameters:
      theta (numpy.ndarray): Array of parameters.
      X (numpy.ndarray): Input data.
      Y (numpy.ndarray): Target values.
      shots (int): Number of shots for quantum measurement (default: int(1e4)).

  Returns:
      float: The objective value.

  """
  n_data = X.shape[0]
  to_return = 0

  for idx in range(n_data):
    prediction = qnn(X[idx], theta, shots=shots)
    difference = np.abs(prediction - Y[idx]) ** 2
    to_return += difference

  return to_return / n_data

def spsa(func, x0, a=0.1, c=0.1, alpha=0.602, gamma=0.101, maxiter=100, verbose=False):
  """
  Performs the Simultaneous Perturbation Stochastic Approximation (SPSA) optimization algorithm.

  Parameters:
      func (callable): Objective function to be minimized.
      x0 (numpy.ndarray): Initial guess for the parameters.
      a (float): Perturbation size parameter (default: 0.1).
      c (float): Step size parameter (default: 0.1).
      alpha (float): Exponent for step size decay (default: 0.602).
      gamma (float): Exponent for perturbation size decay (default: 0.101).
      maxiter (int): Maximum number of iterations (default: 100).
      verbose (bool): Whether to print progress messages (default: False).

  Returns:
      numpy.ndarray: Optimized parameters.

  """
  k = 0
  x = x0

  while k < maxiter:
    ak = a / (k + 1) ** alpha  # Step size
    ck = c / (k + 1) ** gamma  # Perturbation size
    delta = 2 * np.random.randint(0, 2, len(x0)) - 1  # Random perturbation (+1 or -1) for each parameter
    xp = x + ck * delta  # Perturbed parameter values (positive direction)
    xm = x - ck * delta  # Perturbed parameter values (negative direction)
    grad = (func(xp) - func(xm)) / (2 * ck) * delta  # Estimated gradient

    x = x - ak * grad

    if verbose and k % int(0.1 * maxiter) == 0:
      fx = func(x)
      print(f"Iteration {k}: f = {fx}")

    k += 1

  return x

def region_of_indecision(local_idx, X_train, xsol, model, eps = 0.45, local_samples = 100, local_region = 0.025, n_samples = 25):

  lines = np.zeros([n_samples, 100])

  x = X_train

  x_min, x_max = x[:, 0].min() - 0.0101, x[:, 0].max() + 0.0101
  y_min, y_max = x[:, 1].min() - 0.0101, x[:, 1].max() + 0.0101

  x1, x2 = np.meshgrid(np.arange(x_min, x_max, 0.01),
                        np.arange(y_min, y_max, 0.01))

  # Generate lines for plotting by sampling new data points around local points
  for idn in range(n_samples):
    new_X_train = X_train[local_idx,:]+local_region*np.random.randn(local_samples,2)
    new_Y_train = np.array([round(model(new_X_train[y])) for y in range(local_samples)])

    lin = LogisticRegression(fit_intercept = True, C=1e5)
    lin.fit(new_X_train, new_Y_train)

    w = lin.coef_[0]
    m = -w[0] / w[1]
    b = (0.5 - lin.intercept_[0]) / w[1]

    lines[idn] = m*np.linspace(x_min,x_max,100)+b

  Z = []
  for idx1, idx2 in zip(x1.ravel(),x2.ravel()):
    Z.append(round(qnn(np.array([idx1, idx2]), xsol)))
  Z = np.array(Z).reshape(x1.shape)

  # Create a custom colormap
  custom_colors = ['#F27200', '#004D80']
  custom_cmap = colors.ListedColormap(custom_colors)

  plt.pcolormesh(x1, x2, Z, alpha=0.4, cmap=custom_cmap)

  plt.plot(x[local_idx,0], x[local_idx,1], marker="o", markersize=12, markeredgecolor="k",
  markerfacecolor="yellow")

  sorted_data = np.sort(lines,0)
  up = sorted_data[int((0.5+eps)*100)*n_samples//100,:]
  down = sorted_data[int((0.5-eps)*100)*n_samples//100,:]
  plt.fill_between(np.linspace(x_min,x_max,100), down, up, color = 'b', alpha=0.25)

  plt.xlabel("Feature 1")
  plt.ylabel("Feature 2")

  plt.xlim(x_min, x_max - 0.001)
  plt.ylim(y_min, y_max)
  plt.xticks(())
  plt.yticks(());

  # Add the legend
  elements = ['Marker', 'Local region of indecision']
  plt.legend(elements, loc='lower right')
  plt.show()






