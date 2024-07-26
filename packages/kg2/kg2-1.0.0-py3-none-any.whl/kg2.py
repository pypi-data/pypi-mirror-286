from abc import abstractmethod


class Model:
    """Model is a class that instantiates and manipulates a model in Paraconsistent Gödel Modal Logic.

    Args:
        worlds_size (int): Number of worlds in the model.
        relation (list[list[float]], optional): Adjacency matrix for the accessibility relation between worlds. If relation is None, it will generate an empty graph. Defaults to None.
        valuation1 (dict[str, list[float]], optional): A dictionary of variables mapped to a list containing their valuation 1 for each world. Defaults to None.
        valuation2 (dict[str, list[float]], optional): A dictionary of variables mapped to a list containing their valuation 2 for each world. Defaults to None.
        self_relation (bool, optional): Used if relation is None. If self_relation is True, it the generated graph will have self relations equal to 1. 0 otherwise. Defaults to False.
    """

    def __check_relation_value(relation_value: float) -> None:
        """Check if relations are valid.

        Args:
            relation_value (float): Relation value between two worlds.

        Raises:
            Exception: If the relation value is less than 0 or greater than 1.
        """
        if relation_value < 0 or relation_value > 1:
            raise Exception(
                "Relation error: Relation values must be greater or equal than 0 and less or equal than 1."
            )

    @staticmethod
    def __check_relation(relation: list[list[float]], world_size: int) -> None:
        """Check if accessibility relation is valid.

        Args:
            relation (list[list[float]]): Adjacency matrix for the accessibility relation between worlds.
            world_size (int): Number of worlds in the model.

        Raises:
            Exception: If the adjacency matrix is not a worlds_size x worlds_size matrix.
            Exception: If any value of the adjacency matrix is not valid.
        """
        if len(relation) != world_size:
            raise Exception(
                f"Relation error: Relation must be a list of size {world_size}."
            )
        for world_relation in relation:
            if len(world_relation) != world_size:
                raise Exception(
                    f"Relation error: Relation size for a world must be of size {world_size}."
                )
            for relation_value in world_relation:
                Model.__check_relation_value(relation_value)

    @staticmethod
    def __check_world_variable_valuation(world_value: float, type: int) -> None:
        """Check the valuation of a variable for a world.

        Args:
            world_value (float): Valuation value.
            type (int): 1 for valuation 1 or 2 for valuation 2.

        Raises:
            Exception: If valuation value is less than 0 or greater than 1.
        """
        if world_value < 0 or world_value > 1:
            raise Exception(
                f"Valuation error: Valuation {type} must be greater or equal than 0 and less or equal than 1."
            )

    @staticmethod
    def __check_variable_valuation(value: list, type: int) -> None:
        """Checkes the valuations of a variable for each world/

        Args:
            value (list): List of valuations for each world.
            type (int): 1 if valuation 1 or 2 if valuation 2.
        """
        for world_value in value:
            Model.__check_world_variable_valuation(world_value, type)

    @staticmethod
    def __check_valuation(valuation: dict[str, list[float]], type: int) -> None:
        """Check valuation of all variables.

        Args:
            valuation (dict[str, list[float]]): A dictionary of variables mapped to a list containing their valuation for each world.
            type (int): 1 if valuation 1 or 2 if valuation 2.
        """
        for value in valuation.values():
            Model.__check_variable_valuation(value, type)

    def __init__(
        self,
        worlds_size: int,
        relation: list[list[float]] = None,
        valuation1: dict[str, list[float]] = None,
        valuation2: dict[str, list[float]] = None,
        self_relation: bool = False,
    ) -> None:
        self.worlds_size = worlds_size

        if relation == None:
            self.relation = [
                [1 if i == j and self_relation else 0 for j in range(worlds_size)]
                for i in range(worlds_size)
            ]
        else:
            Model.__check_relation(relation, worlds_size)
            self.relation = relation

        if valuation1 == None:
            self.valuation1 = dict()
        else:
            Model.__check_valuation(valuation1, 1)
            self.valuation1 = valuation1

        if valuation2 == None:
            self.valuation2 = dict()
        else:
            Model.__check_valuation(valuation1, 1)
            self.valuation2 = valuation2

    def set_relation(self, world1: int, world2: int, value: float) -> None:
        """Set a relation between two agents.

        Args:
            world1 (int): Index of the first world.
            world2 (int): Index of the second world.
            value (float): Relation value between the two worlds.
        """
        Model.__check_relation_value(value)
        self.relation[world1][world2] = value

    def set_variable_valuation1(self, variable: str, value: list[float]) -> None:
        """Set the valuation 2 of a variable for all worlds. If there is no such variable in the valuation1 dictionary, it creates one.

        Args:
            variable (str): Name of the variable.
            value (list[float]): List of valuations for each world.
        """
        Model.__check_variable_valuation(value, 1)
        self.valuation1[variable] = value

    def set_variable_valuation2(self, variable: str, value: list[float]) -> None:
        """Set the valuation 2 of a variable for all worlds. If there is no such variable in the valuation2 dictionary, it creates one.

        Args:
            variable (str): Name of the variable.
            value (list[float]): List of valuations for each world.
        """
        Model.__check_variable_valuation(value, 2)
        self.valuation2[variable] = value

    def set_variable_valuation1_for_world(
        self, variable: str, world: int, value: float
    ):
        """Set valuation 1 for a specific existing variable for a single world.

        Args:
            variable (str): Name of the variable.
            world (int): World index.
            value (float): Valuation.
        """
        Model.__check_world_variable_valuation(value, 1)
        self.valuation1[variable][world] = value

    def set_variable_valuation1_for_world(self, variable, world, value):
        """Set valuation 2 for a specific existing variable for a single world.

        Args:
            variable (str): Name of the variable.
            world (int): World index.
            value (float): Valuation.
        """
        Model.__check_world_variable_valuation(value, 2)
        self.valuation1[variable][world] = value


class Formula:
    """An interface class to create formulas in Paraconsistent Gödel Modal Logic. Each subclass of Formula corresponds to a rule in the PGML's syntax, and cointains a methods to calculate their valuations. An Formula object is a parsing tree of a formula in PGML."""

    @staticmethod
    def __implication(a: float, b: float) -> float:
        return 1 if a <= b else b

    @staticmethod
    def __conjunction(a: float, b: float) -> float:
        return max(a, b)

    @abstractmethod
    def valuation1(self, model: Model, world: int) -> float:
        """Calculate the valuation 1 for this formula.

        Args:
            model (Model): A PGML model.
            world (int): World index.

        Returns:
            float: Valuation of the formula.
        """
        pass

    @abstractmethod
    def valuation2(self, model: Model, world: int) -> float:
        """Calculate the valuation 1 for this formula.

        Args:
            model (Model): A PGML model.
            world (int): World index.

        Returns:
            float: Valuation of the formula.
        """
        pass


class Variable(Formula):
    """Subclass of Formula to instantiate it from a single variable.

    Args:
        variable (str): Variable name.
    """

    def __init__(self, variable: str):
        self.variable: str = variable

    def __repr__(self) -> str:
        return f"Variable({self.variable})"

    def valuation1(self, model: Model, world: int) -> float:
        return model.valuation1[self.variable][world]

    def valuation2(self, model: Model, world: int) -> float:
        return model.valuation2[self.variable][world]


class Negation(Formula):
    """Subclass of Formula to instantiate a negation.

    Args:
        operand (Formula): Formula to be negated.
    """

    def __init__(self, operand: Formula):
        self.operand = operand

    def __repr__(self) -> str:
        return f"Negation({self.operand.__repr__()})"

    def valuation1(self, model: Model, world: int) -> float:
        return self.operand.valuation2(model, world)

    def valuation2(self, model: Model, world: int) -> float:
        return self.operand.valuation1(model, world)


class Conjunction(Formula):
    """Subclass of Formula to instantiate a conjunction.

    Args:
        left (Formula): Formula on the left side of the conjuntion.
        right (Formula): Formula on the right side of the conjuntion.
    """

    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Conjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int) -> float:
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return max(a, b)

    def valuation2(self, model: Model, world: int) -> float:
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return min(a, b)


class Disjunction(Formula):
    """Subclass of Formula to instantiate a disjunction.

    Args:
        left (Formula): Formula on the left side of the disjuntion.
        right (Formula): Formula on the right side of the disjuntion.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Disjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int) -> float:
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return min(a, b)

    def valuation2(self, model: Model, world: int) -> float:
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return max(a, b)


class Implication(Formula):
    """Subclass of Formula to instantiate an implication.

    Args:
        left (Formula): Formula on the left side of the implication.
        right (Formula): Formula on the right side of the implication.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Implication({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return 1 if a <= b else b

    def valuation2(self, model: Model, world: int):
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return 0 if b <= a else b


class Coimplication(Formula):
    """Subclass of Formula to instantiate an coimplication.

    Args:
        left (Formula): Formula on the left side of the coimplication.
        right (Formula): Formula on the right side of the coimplication.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Coimplication({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        b = self.left.valuation1(model, world)
        a = self.right.valuation1(model, world)
        return 0 if b <= a else b

    def valuation2(self, model: Model, world: int):
        b = self.left.valuation2(model, world)
        a = self.right.valuation2(model, world)
        return 1 if a <= b else b


class Box(Formula):
    """Subclass of Formula to instantiate a box modality.

    Args:
        operand (Formula): A formula to be applied by the box modality.
    """

    @staticmethod
    def __implication(a: float, b: float) -> float:
        return 1 if a <= b else b

    @staticmethod
    def __conjunction(a: float, b: float) -> float:
        return min(a, b)

    def __init__(self, operand: Formula):
        self.operand = operand

    def __repr__(self) -> str:
        return f"Box({self.operand.__repr__()})"

    def valuation1(self, model: Model, world: int) -> float:
        world_size = model.worlds_size
        return min(
            Box.__implication(
                model.relation[world][world_], self.operand.valuation1(model, world_)
            )
            for world_ in range(world_size)
        )

    def valuation2(self, model: Model, world: int) -> float:
        world_size = model.worlds_size
        return max(
            Box.__conjunction(
                model.relation[world][world_], self.operand.valuation2(model, world_)
            )
            for world_ in range(world_size)
        )


class Diamond(Formula):
    """Subclass of Formula to instantiate a diamond modality.

    Args:
        operand (Formula): A formula to be applied by the diamond modality.
    """

    @staticmethod
    def __implication(a: float, b: float) -> float:
        return 1 if a <= b else b

    @staticmethod
    def __conjunction(a: float, b: float) -> float:
        return min(a, b)

    def __init__(self, operand: Formula):
        self.operand = operand

    def __repr__(self) -> str:
        return f"Diamond({self.operand.__repr__()})"

    def valuation1(self, model: Model, world: int) -> float:
        world_size = model.worlds_size
        return max(
            Diamond.__conjunction(
                model.relation[world][world_], self.operand.valuation1(model, world_)
            )
            for world_ in range(world_size)
        )

    def valuation2(self, model: Model, world: int) -> float:
        world_size = model.worlds_size
        return min(
            Diamond.__implication(
                model.relation[world][world_], self.operand.valuation2(model, world_)
            )
            for world_ in range(world_size)
        )
