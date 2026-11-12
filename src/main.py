import ssl
import socket
from datetime import datetime
from config import load_config


def main():
    # TODO: Parse the yaml file to list all sites.
    filepath = 'src/testing.yaml'
    yaml_parsed = load_config(filepath)

    sites = [site['hostname'] for site in yaml_parsed['sites']]
    warn_days = yaml_parsed['warn_days']
    timeout_sec = yaml_parsed['timeout_sec']



    # TODO: 
    try:
        hostname = 'www.example.com'
        port = 443
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(ssock.version())
                cert_data = ssock.getpeercert()
                expiry_data = cert_data['notAfter']

                # Converting notAfter to datetime format.
                timestamp = ssl.cert_time_to_seconds(expiry_data)
                expiry_datetime = datetime.fromtimestamp(timestamp=timestamp)

                curr_datetime = datetime.now() # Make sure it's gmt format.

                # Comparing both datetime
                if expiry_datetime > curr_datetime:
                    print('PASSED: The certificate is not expired.')
                else:
                    print('FAILED')
    except:
        return ssl.SSLCertVerificationError


if __name__=='__main__':
    main()
