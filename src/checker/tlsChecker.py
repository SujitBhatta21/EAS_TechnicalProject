import ssl
import socket
import logging
from datetime import datetime, timezone
from checker.results import HostCheckResult


def tls_checker(hostname: str, port: int, timeout_sec:int=5) -> HostCheckResult:
    """
    @description    : Connects to server. Retrieves cert information then calculates expiry.
    @param          : Given
    @returns        : HostCheckResult Given
    """


    result = HostCheckResult(
        hostname=hostname,
        status='PENDING',
    )

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=timeout_sec) as sock:
            logging.info("TCP Connection established")
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                logging.info("TLS handshake and cert verify succeded")
                tls_version = ssock.version()
                cert_data = ssock.getpeercert()
                expiry_data = cert_data['notAfter']

                # Checking if tls_version is neither SSL(v2/3) nor TLS1.0 TLS1.1 as it's not secure/depreciated.
                depreciated = ['TLSv1.0', 'TLSv1.1']
                if tls_version in depreciated:
                    result.status = "FAIL"
                    result.message = f"TLS version depreciated curr_version: {tls_version}"
                    print(f'Insecure TLS version detected: {tls_version}')

                else:
                    # Converting notAfter to datetime format.
                    timestamp = ssl.cert_time_to_seconds(expiry_data)
                    expiry_datetime = datetime.fromtimestamp(timestamp=timestamp, tz=timezone.utc)

                    curr_datetime = datetime.now(timezone.utc) # Make sure it's gmt format.

                    days_till_expired = (expiry_datetime.date() - curr_datetime.date()).days

                    # Comparing both datetime
                    if expiry_datetime > curr_datetime:
                        result.status = "PASS"
                        result.message = f"cert expires in {days_till_expired} days"
                        print(f'PASSED: Not expired cert for hostname: {result.message}')
                        
                    else:
                        result.status = "FAIL"
                        result.message = f"certificate has expired ({days_till_expired} days)"    
    except socket.gaierror:
        result.status = "FAIL"
        result.message = "DNS lookup failed"
    except (TimeoutError, socket.timeout):
        result.status = "FAIL"
        result.message = "Connection refused"
    except ssl.SSLCertVerificationError as e:
        result.status = "FAIL"
        result.message = f"Certificate verification failed: {e}"
    except ssl.SSLError as e:
        result.status = "FAIL"
        result.message = f"TLS handshake failed: {e}"

    return result
