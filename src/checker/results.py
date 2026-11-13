from dataclasses import dataclass
from collections import Counter


@dataclass
class HostCheckResult:
    hostname: str
    status: str
    http_status_code: int | None = None
    response_time_ms: float | None = None
    message: str = ""


def print_results(results: [HostCheckResult]) -> None:
    counter = Counter(result.status for result in results)

    # Titles for the result
    print(
        f"{'STATUS':<7}"
        f"{'HOSTNAME':<24}"
        f"{'CODE':<7}"
        f"{'LATENCY':<9}"
        f"{'MESSAGE'}"
    )

    # Printing results of all result for all hostnames inside yaml file.
    for result in results:
        status_code = result.http_status_code if result.http_status_code is not None else "---"

        latency = (
            f"{result.response_time_ms:.0f}ms"
            if result.response_time_ms is not None
            else "---"
        )

        print(
            f"{result.status:<7}"
            f"{result.hostname:<24}"
            f"{str(status_code):<7}"
            f"{latency:<9}"
            f"{result.message}"
        )

    # Printing final total of STATUS of results i.e. WARN, PASS, FAIL.
    print(
        f"\nPASS: {counter['PASS']:<5}"
        f"WARN: {counter['WARN']:<5}"
        f"FAIL: {counter['FAIL']:<5}"
        f"(TOTAL: {len(results)})"
    )
