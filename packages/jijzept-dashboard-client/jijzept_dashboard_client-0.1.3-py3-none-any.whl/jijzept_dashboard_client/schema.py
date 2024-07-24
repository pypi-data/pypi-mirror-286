from __future__ import annotations

import typing as tp
from enum import Enum
from typing import List, Optional

import jijmodeling as jm
from pydantic import BaseModel, ConfigDict

DecisionVarType = tp.Union[
    jm.BinaryVar,
    jm.IntegerVar,
    jm.ContinuousVar,
    jm.SemiIntegerVar,
    jm.SemiContinuousVar,
]
RelatedVarType = tp.Union[jm.Placeholder, DecisionVarType]
ConstantType = tp.Union[jm.Placeholder, jm.ArrayLength]


# Remove "\displaystyle" & "$$ " from the latex string
def sanitize_latex(latex: str) -> str:
    text = latex.replace("$$", "").replace("\\displaystyle ", "")
    return text


def sanitize_constraint_latex(latex: str) -> str:
    remove_begin = latex.replace("\\begin{array}{cccc}\n", "")
    remove_end = remove_begin.replace(" \\\\\n\\end{array}", "")
    splited_latex = remove_end.split(" & ")

    INTENDED_SPLIT_LENGTH = 4
    if len(splited_latex) != INTENDED_SPLIT_LENGTH:
        raise ValueError("Invalid LaTeX of `jm.Constraint`.")

    expression_latex = sanitize_latex(splited_latex[2])
    forall_latex = sanitize_latex(splited_latex[3])

    return f"{expression_latex} \\\\ {forall_latex}"


class DecisionVarKind(str, Enum):
    model_config = ConfigDict(from_attributes=True)

    binary = "binary"
    continuous = "continuous"
    integer = "integer"
    semi_continuous = "semi_continuous"
    semi_integer = "semi_integer"


class DecisionVar(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    kind: DecisionVarKind
    lower_bound: str
    upper_bound: str
    shape: List[str]
    latex: str
    description: str

    @classmethod
    def from_variable(cls, var: DecisionVarType) -> DecisionVar:
        if isinstance(var, jm.BinaryVar):
            lower_bound = "0"
            upper_bound = "1"
            kind = DecisionVarKind.binary
        else:
            lower_bound = sanitize_latex(var.lower_bound._repr_latex_())
            upper_bound = sanitize_latex(var.upper_bound._repr_latex_())
            if isinstance(var, jm.IntegerVar):
                kind = DecisionVarKind.integer
            elif isinstance(var, jm.ContinuousVar):
                kind = DecisionVarKind.continuous
            elif isinstance(var, jm.SemiIntegerVar):
                kind = DecisionVarKind.semi_integer
            elif isinstance(var, jm.SemiContinuousVar):
                kind = DecisionVarKind.semi_continuous

        return DecisionVar(
            name=var.name,
            kind=kind,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            shape=[sanitize_latex(s._repr_latex_()) for s in var.shape],
            latex=sanitize_latex(var._repr_latex_()),
            description=var.description,
        )

    @classmethod
    def from_expression(cls, expression: tp.Any) -> list[DecisionVar]:
        return [
            DecisionVar.from_variable(var)
            for var in jm.extract_variables(expression)
            if isinstance(
                var,
                (
                    jm.BinaryVar,
                    jm.IntegerVar,
                    jm.ContinuousVar,
                    jm.SemiIntegerVar,
                    jm.SemiContinuousVar,
                ),
            )
        ]


class Constant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    ndim: int
    latex: str
    description: str

    @classmethod
    def from_variable(cls, var: ConstantType) -> Constant:
        if isinstance(var.description, str):
            description = var.description
        else:
            description = ""

        if isinstance(var, jm.Placeholder):
            return Constant(
                name=var.name,
                ndim=var.ndim,
                latex=sanitize_latex(var._repr_latex_()),
                description=description,
            )
        elif isinstance(var.array, jm.Subscript):
            subscript = sanitize_latex(var.array._repr_latex_())
            return Constant(
                name=(f"length of {subscript} at {var.axis}"),
                ndim=0,
                latex=sanitize_latex(var._repr_latex_()),
                description=description,
            )
        else:
            return Constant(
                name=(f"length of {var.array.name} at {var.axis}"),
                ndim=0,
                latex=sanitize_latex(var._repr_latex_()),
                description=description,
            )

    @classmethod
    def from_expression(cls, expression: tp.Any) -> list[Constant]:
        return [
            Constant.from_variable(var)
            for var in jm.extract_variables(expression)
            if isinstance(var, (jm.Placeholder, jm.ArrayLength))
        ]


class RelatedVariable(BaseModel):
    name: str
    latex: str
    description: str

    @classmethod
    def from_variable(cls, var: RelatedVarType) -> RelatedVariable:
        if isinstance(var.description, str):
            description = var.description
        else:
            description = ""

        return RelatedVariable(
            name=var.name,
            latex=sanitize_latex(var._repr_latex_()),
            description=description,
        )

    @classmethod
    def from_expression(cls, expression: tp.Any) -> list[RelatedVariable]:
        return [
            RelatedVariable.from_variable(var)
            for var in jm.extract_variables(expression)
            if isinstance(
                var,
                (
                    jm.Placeholder,
                    jm.BinaryVar,
                    jm.IntegerVar,
                    jm.ContinuousVar,
                    jm.SemiIntegerVar,
                    jm.SemiContinuousVar,
                ),
            )
        ]


class Objective(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latex: str
    description: str
    related_variables: list[RelatedVariable]

    @classmethod
    def from_objective_and_description(
        cls,
        objective: tp.Any,
        objective_description: tp.Optional[str] = None,
    ) -> Objective:
        if objective_description is None:
            description = ""
        else:
            description = objective_description

        return Objective(
            latex=sanitize_latex(objective._repr_latex_()),
            description=description,
            related_variables=RelatedVariable.from_expression(objective),
        )


class Constraint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latex: str
    name: str
    description: str
    related_variables: list[RelatedVariable]

    @classmethod
    def from_constraint_and_descriptions(
        cls,
        constraint: jm.Constraint,
        constraint_descriptions: tp.Optional[dict[str, str]] = None,
    ) -> Constraint:
        if constraint_descriptions is None:
            description = ""
        elif constraint.name in constraint_descriptions:
            description = constraint_descriptions[constraint.name]
        else:
            description = ""

        return Constraint(
            name=constraint.name,
            latex=sanitize_constraint_latex(constraint._repr_latex_()),
            description=description,
            related_variables=RelatedVariable.from_expression(constraint),
        )


class Source(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

    serializable: str  # jm.to_protobuf(problem) を文字列にしたもの
    objective: Objective
    constraints: List[Constraint]
    decision_vars: List[DecisionVar]
    constants: List[Constant]
    name: Optional[str] = None
