# TLS Checker

A Python CLI application for checking TLS certificates across multiple hostnames.


# 1. What I built and why
I built a standalone TLS certificate checker that takes a YAML configuration file containing hostnames, a certificate expiry warning threshold, and a connection timeout. It prints a report showing which checks passed, which certificates are approaching expiry, and which checks failed.

The aim is to help identify certificate expiry and connection problems before they cause service disruption.

I chose this project because it connects my interest in Python with an area of DevOps I wanted to explore: monitoring. TLS, sockets, and building a command-line application were unfamiliar to me, so this challenge gave me an opportunity to research them and apply what I learned to a practical problem.

The project also includes automated tests using pytest, developed with AI assistance from test scenarios I had written. My research is documented in RESEARCH.md, and my use of AI is explained in AI.md


# 2. How to run it
> Prerequisite: Python and uv.

1. Clone the repository.
2. Install project dependencies: 
```bash
>>> uv sync
```
3.  Run the application with a YAML configuration file:
```bash
>>> uv run src/main.py testing.yml      # Or any other yaml file with your config.

```
Example configuration:

```yaml
sites:
  - hostname: example.com
  - hostname: google.com
warn_days: 30
timeout_sec: 5
```

- `sites`: Hostnames to check, without `https://` or URL paths.
- `warn_days`: Warn when a certificate expires within this many days.
- `timeout_sec`: Connection timeout in seconds.

To run the automated tests:

```bash
>>> uv run pytest -v
```


# 3. How it works
PIPELINE

1. Takes a YAML configuration file as a command-line argument.
2. Loads the file using `load_config()`, parses the YAML, and checks for required fields: `sites`, `warn_days`, and `timeout_sec`.
3. Collects the hostnames listed under `sites`.
4. Calls `tls_checker()` for each hostname on port 443.
5. Attempts a TCP connection using the configured timeout, then performs a TLS handshake. Python's default SSL context verifies the certificate's trust chain and hostname.
6. Retrieves the server certificate using `getpeercert()`, which returns a Python dictionary.
7. Reads the certificate's `notAfter` field and converts it into a UTC expiry date.
8. Compares the expiry date with the current UTC time and assigns a result:
   - **PASS:** The certificate expires beyond the configured warning period.
   - **WARN:** The certificate is still valid but expires within the warning period.
   - **FAIL:** The certificate has expired, the connection or certificate verification fails, or the application detects a deprecated TLS version.
9. Records the elapsed time for each check in milliseconds.
10. Prints a table containing each hostname's status, code, latency, and message, followed by PASS, WARN, and FAIL totals.

The elapsed time covers the connection and TLS check. The displayed code `200` is assigned by the application for valid certificates; it is not obtained from an HTTP request


# 4. What I would improve with more time
With more time I would add Slack incoming webhook integration to send WARN and FAIL results to a dedicated channel whenever the checker runs. This would make certificate and connection problems easier to notice without manually reviewing terminal output.

I would also explore scheduling regular checks so that monitoring does not depend on someone running the application manually. 

# 5. Anything else I think is relevant to help understand the project
- The project was a learning exercise in TLS, sockets, CLI development and automated testing with Python.
- Each run performs a single check of the configured hostnames. The applation does not currently run continously.
- The automated tests mock network connections and TLS operations, allowing them to run without internet connection.
- RESEARCH.md documents my learning process, and AI.md explains how I used AI during development which is just a refresher from the project specification from the email.
