from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Callable, Generic, TypeVar

from ..metrics import BACKGROUND_JOB_RETRIES
from .logging import log_event

T = TypeVar("T")


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_delay_seconds: float = 0.5
    backoff_multiplier: float = 2.0
    max_delay_seconds: float = 5.0


@dataclass
class RetryAttempt:
    attempt: int
    status: str
    error: str | None = None
    delay_seconds: float | None = None


@dataclass
class RetryOutcome(Generic[T]):
    status: str
    attempts: list[RetryAttempt]
    result: T | None = None
    error: str | None = None


def run_with_retry(
    operation_name: str,
    fn: Callable[[], T],
    policy: RetryPolicy | None = None,
) -> RetryOutcome[T]:
    active_policy = policy or RetryPolicy()
    attempts: list[RetryAttempt] = []
    delay = active_policy.initial_delay_seconds

    for attempt_number in range(1, active_policy.max_attempts + 1):
        try:
            result = fn()
            status = "completed" if attempt_number == 1 else "completed_after_retry"
            attempts.append(RetryAttempt(attempt=attempt_number, status=status))
            log_event(
                "retry.completed",
                operation=operation_name,
                attempts=attempt_number,
                status=status,
            )
            return RetryOutcome(status=status, attempts=attempts, result=result)
        except Exception as exc:  # noqa: BLE001
            is_terminal = attempt_number >= active_policy.max_attempts
            status = "dead" if is_terminal else "retrying"
            next_delay = (
                None if is_terminal else min(delay, active_policy.max_delay_seconds)
            )
            attempts.append(
                RetryAttempt(
                    attempt=attempt_number,
                    status=status,
                    error=str(exc),
                    delay_seconds=next_delay,
                )
            )
            log_event(
                "retry.attempt",
                operation=operation_name,
                attempt=attempt_number,
                status=status,
                error=str(exc),
                next_delay_seconds=next_delay,
            )
            BACKGROUND_JOB_RETRIES.labels(job_type=operation_name, status=status).inc()
            if is_terminal:
                return RetryOutcome(
                    status="dead",
                    attempts=attempts,
                    error=str(exc),
                )
            sleep(next_delay or 0)
            delay = min(
                delay * active_policy.backoff_multiplier,
                active_policy.max_delay_seconds,
            )

    return RetryOutcome(
        status="dead",
        attempts=attempts,
        error="Retry loop exited unexpectedly.",
    )
