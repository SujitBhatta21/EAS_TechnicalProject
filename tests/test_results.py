"""
TESTING REQUIREMENTS:
- Correct HostCheckResult fields.
- Correct PASS, WARN and FAIL classification.
- Correct response-time handling.
- Correct formatting of terminal output.
- Correct summary counts.
"""

from checker.results import HostCheckResult, print_results


def test_host_check_result_fields():
    result = HostCheckResult("example.com", "PASS", 200, 12.5, "cert expires in 60 days")

    assert result.hostname == "example.com"
    assert result.status == "PASS"
    assert result.http_status_code == 200
    assert result.response_time_ms == 12.5
    assert result.message == "cert expires in 60 days"


def test_host_check_result_defaults():
    result = HostCheckResult("example.com", "FAIL")

    assert result.http_status_code is None
    assert result.response_time_ms is None
    assert result.message == ""


def test_terminal_formatting_and_summary(capsys):
    results = [
        HostCheckResult("valid.example", "PASS", 200, 12.6, "valid"),
        HostCheckResult("soon.example", "WARN", 200, 0.0, "expires soon"),
        HostCheckResult("failed.example", "FAIL", message="DNS lookup failed"),
        HostCheckResult("other.example", "PASS", 200, 8.0, "valid"),
    ]

    print_results(results)

    assert capsys.readouterr().out == (
        f"{'STATUS':<7}{'HOSTNAME':<24}{'CODE':<7}{'LATENCY':<9}MESSAGE\n"
        f"{'PASS':<7}{'valid.example':<24}{'200':<7}{'13ms':<9}valid\n"
        f"{'WARN':<7}{'soon.example':<24}{'200':<7}{'0ms':<9}expires soon\n"
        f"{'FAIL':<7}{'failed.example':<24}{'---':<7}{'---':<9}DNS lookup failed\n"
        f"{'PASS':<7}{'other.example':<24}{'200':<7}{'8ms':<9}valid\n"
        f"PASS: {2:<5}WARN: {1:<5}FAIL: {1:<5}(TOTAL: 4)\n"
    )
