import ssl
import socket
from enum import Enum
from datetime import datetime


class MONTHS(Enum):
    Jan = 1 
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    Jun = 6
    Jul = 7
    Aug = 8
    Sept = 9
    Oct = 10
    Nov = 11
    Dec = 12

def main():
    hostname = 'www.example.com'
    port = 443
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())
            cert_data = ssock.getpeercert()
            expiry_data = cert_data['notAfter']
            print(cert_data)

            curr_datetime = datetime.now() # Make sure it's gmt format.
            print(curr_datetime)
        
            # Changing 'notAfter' time format to datetime format.
            month, day, exp_time, year, _ = expiry_data.split(' ')
            exp_date_str = f'{year}-{MONTHS[month].value}-{day}'
            print(exp_date_str)
            exp_datetime = datetime.fromisoformat(exp_date_str + ' ' + exp_time)
            print(exp_datetime)

            # Comparing both datetime
            if exp_datetime > curr_datetime:
                print('PASSED: The certificate is not expired.')
            else:
                print('FAILED')


if __name__=='__main__':
    main()
