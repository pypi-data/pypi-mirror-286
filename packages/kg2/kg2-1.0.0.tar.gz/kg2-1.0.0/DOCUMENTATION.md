<!-- markdownlint-disable -->

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pgml.py`






---

## <kbd>class</kbd> `Box`
Subclass of Formula to instantiate a box modality. 



**Args:**
 
 - <b>`operand`</b> (Formula):  A formula to be applied by the box modality. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L375"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(operand: Formula)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L381"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L390"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```






---

## <kbd>class</kbd> `Coimplication`
Subclass of Formula to instantiate an coimplication. 



**Args:**
 
 - <b>`left`</b> (Formula):  Formula on the left side of the coimplication. 
 - <b>`right`</b> (Formula):  Formula on the right side of the coimplication. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L342"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(left, right)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L349"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int)
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L354"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int)
```






---

## <kbd>class</kbd> `Conjunction`
Subclass of Formula to instantiate a conjunction. 



**Args:**
 
 - <b>`left`</b> (Formula):  Formula on the left side of the conjuntion. 
 - <b>`right`</b> (Formula):  Formula on the right side of the conjuntion. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(left: Formula, right: Formula)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```






---

## <kbd>class</kbd> `Diamond`
Subclass of Formula to instantiate a diamond modality. 



**Args:**
 
 - <b>`operand`</b> (Formula):  A formula to be applied by the diamond modality. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L415"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(operand: Formula)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L421"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```






---

## <kbd>class</kbd> `Disjunction`
Subclass of Formula to instantiate a disjunction. 



**Args:**
 
 - <b>`left`</b> (Formula):  Formula on the left side of the disjuntion. 
 - <b>`right`</b> (Formula):  Formula on the right side of the disjuntion. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L290"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(left, right)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L302"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```






---

## <kbd>class</kbd> `Formula`
An interface class to create formulas in Paraconsistent Gödel Modal Logic. Each subclass of Formula corresponds to a rule in the PGML's syntax, and cointains a methods to calculate their valuations. An Formula object is a parsing tree of a formula in PGML. 




---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```

Calculate the valuation 1 for this formula. 



**Args:**
 
 - <b>`model`</b> (Model):  A PGML model. 
 - <b>`world`</b> (int):  World index. 



**Returns:**
 
 - <b>`float`</b>:  Valuation of the formula. 

---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```

Calculate the valuation 1 for this formula. 



**Args:**
 
 - <b>`model`</b> (Model):  A PGML model. 
 - <b>`world`</b> (int):  World index. 



**Returns:**
 
 - <b>`float`</b>:  Valuation of the formula. 


---

## <kbd>class</kbd> `Implication`
Subclass of Formula to instantiate an implication. 



**Args:**
 
 - <b>`left`</b> (Formula):  Formula on the left side of the implication. 
 - <b>`right`</b> (Formula):  Formula on the right side of the implication. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(left, right)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L323"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int)
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L328"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int)
```






---

## <kbd>class</kbd> `Model`
Model is a class that instantiates and manipulates a model in Paraconsistent Gödel Modal Logic. 



**Args:**
 
 - <b>`worlds_size`</b> (int):  Number of worlds in the model. 
 - <b>`relation`</b> (list[list[float]], optional):  Adjacency matrix for the accessibility relation between worlds. If relation is None, it will generate an empty graph. Defaults to None. 
 - <b>`valuation1`</b> (dict[str, list[float]], optional):  A dictionary of variables mapped to a list containing their valuation 1 for each world. Defaults to None. 
 - <b>`valuation2`</b> (dict[str, list[float]], optional):  A dictionary of variables mapped to a list containing their valuation 2 for each world. Defaults to None. 
 - <b>`self_relation`</b> (bool, optional):  Used if relation is None. If self_relation is True, it the generated graph will have self relations equal to 1. 0 otherwise. Defaults to False. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    worlds_size: int,
    relation: list[list[float]] = None,
    valuation1: dict[str, list[float]] = None,
    valuation2: dict[str, list[float]] = None,
    self_relation: bool = False
) → None
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `set_relation`

```python
set_relation(world1: int, world2: int, value: float) → None
```

Set a relation between two agents. 



**Args:**
 
 - <b>`world1`</b> (int):  Index of the first world. 
 - <b>`world2`</b> (int):  Index of the second world. 
 - <b>`value`</b> (float):  Relation value between the two worlds. 

---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `set_variable_valuation1`

```python
set_variable_valuation1(variable: str, value: list[float]) → None
```

Set the valuation 2 of a variable for all worlds. If there is no such variable in the valuation1 dictionary, it creates one. 



**Args:**
 
 - <b>`variable`</b> (str):  Name of the variable. 
 - <b>`value`</b> (list[float]):  List of valuations for each world. 

---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `set_variable_valuation1_for_world`

```python
set_variable_valuation1_for_world(variable, world, value)
```

Set valuation 2 for a specific existing variable for a single world. 



**Args:**
 
 - <b>`variable`</b> (str):  Name of the variable. 
 - <b>`world`</b> (int):  World index. 
 - <b>`value`</b> (float):  Valuation. 

---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `set_variable_valuation2`

```python
set_variable_valuation2(variable: str, value: list[float]) → None
```

Set the valuation 2 of a variable for all worlds. If there is no such variable in the valuation2 dictionary, it creates one. 



**Args:**
 
 - <b>`variable`</b> (str):  Name of the variable. 
 - <b>`value`</b> (list[float]):  List of valuations for each world. 


---

## <kbd>class</kbd> `Negation`
Subclass of Formula to instantiate a negation. 



**Args:**
 
 - <b>`operand`</b> (Formula):  Formula to be negated. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L243"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(operand: Formula)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```






---

## <kbd>class</kbd> `Variable`
Subclass of Formula to instantiate it from a single variable. 



**Args:**
 
 - <b>`variable`</b> (str):  Variable name. 

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(variable: str)
```








---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation1`

```python
valuation1(model: Model, world: int) → float
```





---

<a href="https://github.com/josecoliveira/pgml/tree/v1.0.0\pgml.py#L232"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `valuation2`

```python
valuation2(model: Model, world: int) → float
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
