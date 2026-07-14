from backend.guardrails.output_filter import (
    validate_output,
)

from backend.guardrails.validators import (
    IterationGuard,
    validate_input,
)


iteration_guard = IterationGuard()


def validate_agent_input(
    query: str,
):

    return validate_input(query)


def validate_agent_output(
    answer: str,
):

    return validate_output(answer)


def validate_iterations(
    iterations: int,
) -> bool:

    return iteration_guard.check(
        iterations
    )