# DAY1:

Used AI to figure out how to compare two datetime and how to convert a string type to datetime.
> PROMPT 1: compare two datetime python

> PROMPT 2: How to convert a string in datetime structure to datetime (Answer: `fromisoformat(date_str)`)



# DAY4:

Used AI in tlsChecker.py for exception error types. 
> PROMPT1 : how to do lookup if the connection was unsuccessful. I need that as well check.     with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())

> ANSWER: <br>

Handle connection failures with
| Operation | Possible exception |
|---|---|
| DNS resolution | `socket.gaierror` |
| TCP connection | `ConnectionRefusedError`, `TimeoutError`, `OSError` |
| TLS handshake | `ssl.SSLError` |
| Certificate verification | `ssl.SSLCertVerificationError` |
Important: SSLCertVerificationError is a subclass of SSLError, so catch it first.

You can also catch other OSError exceptions to handle network failures not covered above.
What about checking whether the connection succeeded?
You don't need an additional check like:
if sock.connected:


The socket API doesn't expose a connected property like that.

If socket.create_connection() returns successfully, the TCP connection was established.

If context.wrap_socket() returns successfully with the default context, the TLS handshake and certificate verification also succeeded.


--- 


# Day 5
Used GPT-6.1-Sol default to Implement pytest test suite.

## PROMPT: 
"I've already designed the test scenarios/requirements for my TLS certificate monitoring application.

Please inspect my existing source code and test designs, then implement the required automated tests using pytest.

Requirements:

1. I have created a dedicated `tests/` directory with test files organised according to the source modules with test requirements inside it in """""". Don't remove these requirements.&#x20;
2. Follow my existing test designs rather than inventing additional requirements.
3. Use mocking for network connections and TLS operations so tests run without internet access.
4. Use pytest fixtures and parameterization only where they genuinely simplify testing.
5. Ensure tests verify the actual application's behaviour, not merely mocked return values.
6. Do not modify production code or restructure the project.
7. If you discover bugs or discrepancies, report them rather than changing the expected test outcomes.
8. Run the complete test suite using `uv run pytest -v`.
9. Report the number of passing and failing tests, along with any bugs or untested scenarios.

Keep the tests simple, readable and maintainable. Avoid unnecessary abstractions or dependencies.

Once finished, briefly explain what each test file covers and how the important network failures are simulated.
"

### ANSWER:
Implemented 20 tests, preserving all requirement docstrings and leaving production code unchanged.

uv run pytest -v: 14 passed, 6 failed.

The failures expose these discrepancies:

- Missing sites, warn_days, or timeout_sec is accepted: 3 failures.
- An empty site list is accepted: 1 failure.
- Timeouts are incorrectly reported as “Connection refused”: 1 failure.
- ConnectionRefusedError escapes instead of returning a FAIL result: 1 failure.

Configuration rejection is an interpretation of your scenarios; they do not specify an exact validation contract.

Coverage by file:

- test_config.py: valid, missing and malformed YAML, missing fields, and empty sites.
- test_results.py: result fields/defaults, terminal formatting, latency display, and summary counts.
- test_tls_checker.py: successful TLS, PASS/WARN/FAIL certificate classification, elapsed time, and all listed network failures.
- conftest.py: imports the existing src layout.

Socket connections and TLS contexts are mocked. Exceptions simulate DNS, timeout, refusal, reset, handshake, and certificate-verification failures. Fixed clocks make expiry and latency assertions deterministic; application logic performs the classification.

All listed scenarios are represented. Real network/TLS integration and CLI execution remain untested.
  Worked for 1m 46s • 9:16 AM