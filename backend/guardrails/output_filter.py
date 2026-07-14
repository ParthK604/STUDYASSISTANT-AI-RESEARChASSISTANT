from typing import Optional


MAX_RESPONSE_LENGTH = 4000


def clean_output(answer: str) -> str:
    """
    Cleans the final LLM response.
    """

    answer = answer.strip()

    while "\n\n\n" in answer:
        answer = answer.replace("\n\n\n", "\n\n")

    return answer


def validate_output(
    answer: Optional[str],
) -> Optional[str]:
    """
    Validates the generated answer.
    Returns None if valid.
    """

    if answer is None:
        return "Empty response."

    answer = clean_output(answer)

    if not answer:
        return "Response is empty."

    if len(answer) > MAX_RESPONSE_LENGTH:
        return (
            f"Response exceeds "
            f"{MAX_RESPONSE_LENGTH} characters."
        )

    return None