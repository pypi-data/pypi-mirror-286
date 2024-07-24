from __future__ import annotations

import dataclasses
import pydantic
import typing as typ

import jijmodeling as jm

from jijzept.entity.schema import SolverType
from jijzept.response import JijModelingResponse
from jijzept.sampler.base_sampler import (
    JijZeptBaseSampler,
    ParameterSearchParameters,
    check_kwargs_against_dataclass,
    merge_params_and_kwargs,
    sample_instance,
    sample_model,
)
from jijzept.type_annotation import FixedVariables, InstanceData
from jijzept.utils import serialize_fixed_var

from jijzept.exception.exception import JijZeptClientValidationError

T = typ.TypeVar("T")


@dataclasses.dataclass
class JijSolverParameters:
    """Manage Parameters for using JijSolver's WeightedLS.

    Attributes:
        num_iters (int): The number of iterations (each iteration consists of SFSA, SFLS, MFLS, and update of the weights).
        time_limit_msec (int): How long does the solver take for each SA (LS) part (in units of millisecond).
        count (int): The number of iterations during each SA (LS) part.
        ignored_constraints (list[str]): The list of constraint names to be ignored.
    """

    num_iters: int = 4
    time_limit_msec: typ.Optional[float] = None
    count: typ.Optional[int] = None
    ignored_constraints: typ.Optional[typ.List[str]] = None


class JijSolver(JijZeptBaseSampler):
    jijmodeling_solver_type = SolverType(
        queue_name="openjijsolver", solver="JijSolverV2"
    )

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        fixed_variables: FixedVariables = {},
        parameters: JijSolverParameters = JijSolverParameters(time_limit_msec=2000),
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijSolver.

        To configure the solver, instantiate the `JijSolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            parameters (JijSAParameters | None, optional): defaults JijSolverParameters().
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 600 will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: Parameters of jijsolver. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=n)
            problem = jm.Problem('problem')
            problem += jm.sum(i, d[i] * x[i])

            sampler = jz.JijSolver(config='config.toml')
            response = sampler.sample_model(problem, feed_dict={'n': 5, 'd': [1,2,3,4,5]})
            ```
        """
        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        solver_params = self._create_solver_params(
            fixed_variables=fixed_variables,
            parameters=parameters,
            kwargs=kwargs,
        )

        sample_set = sample_model(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            problem=model,
            instance_data=feed_dict,
            max_wait_time=max_wait_time,
            sync=sync,
            parameters=solver_params,
        )
        return sample_set

    def sample_instance(
        self,
        instance_id: str,
        fixed_variables: FixedVariables = {},
        parameters: JijSolverParameters = JijSolverParameters(time_limit_msec=2000),
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijSolver.

        To configure the solver, instantiate the `JijSolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            parameters (JijSAParameters | None, optional): defaults JijSolverParameters().
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 600 will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: Parameters of jijsolver. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=n)
            problem = jm.Problem('problem')
            problem += jm.sum(i, d[i] * x[i])

            # initialize sampler
            sampler = jz.JijSolver(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample uploaded instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        solver_params = self._create_solver_params(
            fixed_variables=fixed_variables,
            parameters=parameters,
            kwargs=kwargs,
        )

        sample_set = sample_instance(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            instance_id=instance_id,
            max_wait_time=max_wait_time,
            sync=sync,
            system_time=system_time,
            parameters=solver_params,
        )

        return sample_set

    def _create_solver_params(
        self,
        *,
        fixed_variables: FixedVariables,
        parameters: JijSolverParameters,
        kwargs: dict[str, typ.Any],
    ) -> dict:
        class JijSolverV2(pydantic.BaseModel):
            fixed_variables: dict[
                str, list[typ.Union[list[list[int]], list[typ.Union[int, float]]]]
            ]
            num_iters: pydantic.PositiveInt
            time_limit_msec: typ.Optional[pydantic.PositiveInt] = None
            count: typ.Optional[pydantic.PositiveInt] = None
            ignored_constraints: typ.Optional[typ.List[str]]

            @pydantic.model_validator(mode="after")
            def verify_either_count_or_time_limit_msec_is_not_none(self):
                if self.count is None and self.time_limit_msec is None:
                    raise JijZeptClientValidationError(
                        "Either 'count' or 'time_limit_msec' must be set."
                    )
                return self

        check_kwargs_against_dataclass(kwargs, JijSolverParameters)
        solver_params = merge_params_and_kwargs(parameters, kwargs, JijSolverParameters)

        para_search_params = ParameterSearchParameters()

        solver_params["fixed_variables"] = serialize_fixed_var(fixed_variables)
        solver_params.update(dataclasses.asdict(para_search_params))

        try:
            return JijSolverV2(**solver_params).model_dump()
        except pydantic.ValidationError as e:
            raise JijZeptClientValidationError(str(e))
