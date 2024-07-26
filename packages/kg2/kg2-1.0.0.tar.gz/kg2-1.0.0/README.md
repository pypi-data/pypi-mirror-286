# kg2: A Python Tool for Paraconsistent Gödel Modal Logic

This package implements model and evaluation for Paraconsistent Gödel Modal Logic.  In this logic, the belief of an agent in a proposition is defined to be a pair of values in the interval $[0, 1]\times[0,1]$, representing the world's truth-value for and against the proposition.Paraconsistent Gödel Modal Logic is valuable for representing nuanced information about evidence, strength of belief, consistency and inconsistency, and certainty and uncertainty.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kg2.

```bash
pip install kg2
```

## Usage

The full reference of the package can be found in `DOCUMENTATION.md`.

```python
from kg2 import *

# Number of worlds in the model.
world_size = 4

# Accessibility relation.
relation = [[1, 1, 0.5, 0.5], [1, 1, 0.5, 0.5], [0.5, 0.5, 1, 1], [0.5, 0.5, 1, 1]]

# Valuation 1 for each variable and agent.
valuation1 = {"p": [1, 1, 0.4, 0.4]}

# Valuation 2 for each variable and agent.
valuation2 = {"p": [0, 0, 0.8, 0.8]}

# Model instantiation.
model = Model(4, relation, valuation1, valuation2)

# Define a formula.
formula = Diamond(Diamond(Variable("p")))

# Evaluate formula in the model for world 0.
formula.valuation1(model, 0)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## References

Bílková, M., Frittella, S., Kozhemiachenko, D. (2022). Paraconsistent Gödel Modal Logic. In: Blanchette, J., Kovács, L., Pattinson, D. (eds) Automated Reasoning. IJCAR 2022. Lecture Notes in Computer Science(), vol 13385. Springer, Cham. [https://doi.org/10.1007/978-3-031-10769-6_26]
