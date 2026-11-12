import logging
from checker.config import load_config
from checker.tlsChecker import tls_checker


def main():
    # TODO: Parse the yaml file to list all sites.
    filepath = 'testing.yaml'
    yaml_parsed = load_config(filepath)

    hostnames = [site['hostname'] for site in yaml_parsed['sites']]
    warn_days = yaml_parsed['warn_days']
    timeout_sec = yaml_parsed['timeout_sec']
    print(hostnames)


    # TODO: Check all the site in sites using checker
    results = []

    for hostname in hostnames:
        result = tls_checker(
            hostname=hostname, 
            port=443, 
            timeout_sec=int(timeout_sec), 
        )
        results.append(result)


    # TODO: Logging results ready for report.
    


if __name__=='__main__':
    main()
