import sys
from checker.config import load_config
from checker.tlsChecker import tls_checker
from checker.results import print_results


def main():
    # TODO: Parse the arguments given in input.
    if len(sys.argv) != 2:
        print("Usage: uv run src/main.py <filepath> or [python] instead of [uv run]")
        sys.exit(1)

    filepath = sys.argv[1]

    # TODO: Parse the yaml file to list all sites.
    yaml_parsed = load_config(filepath)

    hostnames = [site['hostname'] for site in yaml_parsed['sites']]
    warn_days = yaml_parsed['warn_days']
    timeout_sec = yaml_parsed['timeout_sec']


    # TODO: Check all the site in sites using checker
    results = []

    for hostname in hostnames:
        result = tls_checker(
            hostname=hostname, 
            port=443, 
            warn_days=warn_days, 
            timeout_sec=int(timeout_sec), 
        )
        results.append(result)


    # TODO: Logging results ready for report.
    print_results(results)    


if __name__=='__main__':
    main()
