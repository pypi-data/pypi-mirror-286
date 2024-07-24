from __future__ import annotations

import datetime

import jijmodeling as jm
from google.protobuf.text_encoding import CEscape, CUnescape

from jijzept_dashboard_client import schema


# Remove "\displaystyle" & "$$ " from the latex string
def sanitize_latex(latex: str) -> str:
    text = latex.replace("$$", "").replace("\\displaystyle ", "")
    return text


class Problem:
    def __init__(self, name: str):
        """
        Create a Problem instance with descriptions.

        Args:
            name (str): The name of the problem.
        """
        self.name = name
        self.constraints: dict[str, jm.Constraint] = {}
        self.constraint_description: dict[str, str] = {}
        self.obj_description = ""
        self.objective = 0

    # Support += operator
    def __iadd__(
        self,
        expr_description: tuple[jm.Constraint, str] | jm.Constraint,
    ) -> Problem:
        if isinstance(expr_description, tuple):
            INTENDED_TUPLE_LENGTH = 2
            if len(expr_description) != INTENDED_TUPLE_LENGTH:
                raise ValueError("The tuple must have 2 elements")
            expr, description = expr_description
        else:
            expr = expr_description
            description = ""

        if isinstance(expr, jm.Constraint):
            self.constraints[expr.name] = expr
            self.constraint_description[expr.name] = description
        else:
            self.objective = expr
            self.obj_description = description
        return self

    def get_jm_problem(self) -> jm.Problem:
        problem = jm.Problem(self.name)
        for c in self.constraints.values():
            problem += c
        problem += self.objective
        return problem

    # このメソッドがこのセクションにおける具体的な処理
    def to_serializable(self) -> dict:
        problem = self.get_jm_problem()

        objective = schema.Objective.from_objective_and_description(
            problem.objective, self.obj_description
        )

        constraints = [
            schema.Constraint.from_constraint_and_descriptions(
                constraint, self.constraint_description
            )
            for constraint in problem.constraints.values()
        ]

        decision_vars = schema.DecisionVar.from_expression(problem)

        constants = schema.Constant.from_expression(problem)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        return schema.Source(
            serializable=CEscape(jm.to_protobuf(problem), as_utf8=False),
            objective=objective,
            constraints=constraints,
            decision_vars=decision_vars,
            constants=constants,
            name=f"{problem.name} ({timestamp})",
        ).model_dump()

    @classmethod
    def from_serializable(cls, serializable: dict) -> Problem:
        prob_proto = serializable["serializable"]
        prob: jm.Problem = jm.from_protobuf(CUnescape(prob_proto))
        p = cls(prob.name)
        p.objective = prob.objective
        for const in prob.constraints.values():
            p.constraints[const.name] = const
        p.obj_description = serializable["objective"]["description"]
        for const in serializable["constraints"]:
            p.constraint_description[const["name"]] = const["description"]
        return p

    @classmethod
    def from_jm_problem(
        cls,
        jm_problem: jm.Problem,
        objective_description: str = "",
        constraint_descriptions: dict[str, str] = {},
    ) -> Problem:
        """
        Create a Problem instance from a Problem instance of jijmodeling.

        Args:
            jm_problem (jm.Problem): A Problem instance of jijmodeling.
            objective_description (str):
                A description of the objective function.
            constraint_descriptions (dict[str, str]):
                A dictionary of constraint names and their descriptions.

        Returns:
            Problem: A Problem with descriptions.
        """
        for constr_name in constraint_descriptions.keys():
            if constr_name not in jm_problem.constraints:
                raise ValueError(
                    f"Constraint {constr_name} is not found "
                    f"in the `jm_problem`."
                )

        jdc_problem = cls(jm_problem.name)
        jdc_problem += (jm_problem.objective, objective_description)

        for k, v in jm_problem.constraints.items():
            if k in constraint_descriptions:
                jdc_problem += (v, constraint_descriptions[k])
            else:
                jdc_problem += v

        return jdc_problem
