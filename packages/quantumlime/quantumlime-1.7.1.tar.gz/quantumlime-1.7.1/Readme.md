# Description

# User guide

You can find below a sample client python script calling Quantumlime

```Python
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import numpy as np
import quantumlime

# Load the Iris dataset
iris = load_iris()
# Normalize the data by subtracting the minimum value and dividing by the maximum value
iris.data = (iris.data - iris.data.min()) / iris.data.max()

# Use the first two classes of the Iris dataset only (100 of 150 data points)
X_train, X_test, Y_train, Y_test = train_test_split(
    iris.data[0:100, [0, 1]],
    iris.target[0:100],
    test_size=0.75,
    random_state=0)

a = 2.5
c = 0.25
maxiter = 1e3
shots = int(1e4)
alpha = 0.602
gamma = 0.101

f = lambda x: quantumlime.objective(x,X_train,Y_train,shots=shots) # Objective function
x0 = np.pi*np.random.randn(4)

xsol = quantumlime.spsa(f, x0, a=a, c=c,
            alpha=alpha, gamma=gamma,
            maxiter=maxiter, verbose=True)

# Explain the local behavior of the model
quantumlime.region_of_indecision(1,X_train,xsol, lambda x : quantumlime.qnn(x,xsol))
# Explain the local behavior of the model at a local region of value
quantumlime.region_of_indecision(2,X_train,xsol, lambda x : quantumlime.qnn(x,xsol), local_region = 0.05)
```

# Administration Guide
## Bump version

Bumping a version requires bumpver.
If bumpver is not installed yet use

```Shell
pip install bumpver
```

### Bump Z in X.Y.Z

```Shell
bumpver update --patch
```

### Bump Y in X.Y.Z

```Shell
bumpver update --minor
```

### Bump X in X.Y.Z

```Shell
bumpver update --major
```

## Publish to the TEST Pypi repository

Once the version number has been properly bumped use (note your credentials must be properly setup into your `$HOME/.pypirc` file:
```Shell
rm -rf dist/
python -m build
twine upload -r testpypi dist/*
```

## Publish to the PROD Pypi repository

Once the version number has been properly bumped use (note your credentials must be properly setup into your `$HOME/.pypirc` file:
```Shell
rm -rf dist/
python -m build
twine upload -r pypi dist/*
```
