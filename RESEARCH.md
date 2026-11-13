Mental Model for project.
- 
- Spend about 5-7 hrs spanning over 4-7 days with regular commits.
- Go to company site and skim through projects or case studies which will definitely give me some inspirations.
- Requirements gathering, Language choice, new concept learning draft roadmap figured out in first hr.



## Company Research
### Company MOTO: 
> UNDERSTAND -> DESIGN -> DEVELOP

(FUN COINCIDENCE: ARCUS AI-Powered Building Intelligence project from EAS used YOLO. I have used YOLO in one of my project as well)




# Project Requirements Research (Why that stack?)

## DAY 1
**TASK DESCRIPTION:**
>'The format and technology are entirely up to you. It could be a command-line application ...'<br>

I have not worked with CLI before and it is something mentioned as a first option in the email, brainstorming more might only spiral my mind into picking a perfect project.

Language: Python  
WHY?
- > Go is best for scripting a CLI but learning new language syntax for simple project was more time consuming so, I decided to stick with Python which is also great alternative for CLI projects.

My choice of problem: TLS certificate and uptime checker CLI
- > Input: a file of URLs (preferrably yaml) in format `tlschecker <filename>`
- > Processing: checks HTTP status, response time and certificate expiry for each URL.
- > Output: a redable report, preferable exit codes if anything fails or else 0. (Optional) notifying user in email/slack if anything fails.


Testing: Using pytest and badssl.com
WHY?
-   > Pytest because I have read about this during one of my modules at my university as a industry standard test for python.
-   > badssl.com contains several deliberately broken certificates (found with simple google search).


RISKS/LIMITATIONS (what might break or not go my way)
- > Underestimating project requirements 
- > Proper faliure handling gracefully.

CHALLANGE FOR ME ((Just 2 right now)):
- > I know what TLS cert is but don't know what's under the hood and how it works.
- > Haven't worked on a CLI project.
- > Figuring out pytest and how it works.



## DAY2
Looking into how TLS works and verifying a TLS cert.

1. Establishing connection with URL.
2. Performing TLS handshake using ssl library python3 (why: )
3. Checking if certificate is expired or not.
4. Return something...

**ANSWER**:
    Reading python docs for ssl library gave me sample template to connect to the hostname URL to print TLS version(). 
    Further reseatch using Ctrl + F for certificates helped me find getpeercert() function which returned a Python dictionary with 'notAfter' (i.e. expiry date) which is exactly what I needed.
    Example print with hostname='example.com' for this function.: 
> {'subject': ((('commonName', 'example.com'),),), 'issuer': ((('countryName', 'US'),), (('organizationName', 'SSL Corporation'),), (('commonName', 'Cloudflare TLS Issuing ECC CA 3'),)), 'version': 3, 'serialNumber': '01EEE6AABB521D5E14FC315FD9985690', 'notBefore': 'Sep 26 22:49:11 2026 GMT', '**notAfter**': 'Dec 25 22:56:35 2026 GMT', 'subjectAltName': (('DNS', 'example.com'), ('DNS', '*.example.com')), 'OCSP': ('http://o.cf-i.ssl.com',), 'caIssuers': ('http://i.cf-i.ssl.com/Cloudflare-TLS-I-E3.cer',), 'crlDistributionPoints': ('http://c.cf-i.ssl.com/ae801ed1c55bb579d79208b0d772acfb8cc3a208.crl',)}

## DAY3
It was bhai tika a festival in Tihar(Diwali) so, whole day well spent with family and friends.

## DAY4
Previous code simply was a draft for me to get familar with ssl library.
Today research involves:
- Me optimising my draft code inside main() function.
> `ssl.cert_time_to_seconds()` made it more easier for me to convert `notAfter` in tls cert json in datetime format for easier calculations.
- Structuring my files for better readability 
> Breaking down main file into config which parses and returns yaml file contents.
- Making a sample test sites yaml file with a code for parsing the file.
> 
- Adding exception handling.
> Using try and except. Including Timeout error if stuck for connection for 5 sec in single link. 
- In the end performing tests.
> Used badssl repository error links like expired.badssl.com,
- (optional) research on CLI in Python and taking in args.

During today research during optimising main() function's TLS certification check I wanted to add functionality to avoid unsecured or depreciated ssl/tls versions i.e. TLSv1.0/TLSv1.1/SSLv3. So, 


### Bugfix
--- 
During working out I wanted to make sure that datetime I collect using datetime.now() has timezone specific utc. Then I got this error: 
    if expiry_datetime > curr_datetime:
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: can't compare offset-naive and offset-aware datetimes
I learned something new. Didn't realise I had to add timezone specific information to both datetime type if I want to use expression on it.

I initially tried to use `datetime.now(timezone.utc)` to calculate the timestamp for the hostname TCP connection but later realised that timezone might not be viable option considering it changes drastically for my local location in London 2 times a year. Once increases by 1 hr and other decreases by 1. It is the worst case scenario. 

<br>
During research I found `time.monotonic()` function: 

It's description: 
> Return the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards. The clock is not affected by system clock updates.

The not affected by system clock is exactly what I need.


During my code session trying to build `print_report()` method I learned new thing. I can use `:>number` for amount of align space I want inside a format string print. **Remember** it's :> then right align :< then left align. Example `>>>> f"{result.status:<7}`"

### ERROR
--- 
I was adding more hostname tests in my testing.yaml file and got this error. "`  File "/home/sujit/.local/share/uv/python/cpython-3.15.2-linux-x86_64-gnu/lib/python3.15/ssl.py", line 1115, in _create
    self.do_handshake()
    ~~~~~~~~~~~~~~~~~^^
  
  File "/home/sujit/.local/share/uv/python/cpython-3.15.2-linux-x86_64-gnu/lib/python3.15/ssl.py", line 1446, in do_handshake
    self._sslobj.do_handshake()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
**ConnectionResetError**: [Errno 104] Connection reset by peer`"

THE Error is not reproducible now when I tried to rerun multiple times in terminal. Upon further investigation I learned that this occurs when Connection is Reset during TLS handshake.
. As a countermeasure for that error I added another exemption in the try/except block to take care of `ConnectionResetError` if it occurs again.


## Day 5

### Goal of the day (30 mins)
- Add CLI arguments input feature.
- Create automated test inside /test using pytest preferably.
- (optional) Try to look into how to connect to Slack/Discord preferably Slack to notify of any WARN or FAIL status for hostnames.

CLI integration was easier than expected. Simple enough as I was already familar with some sort of argument workthrough when I was learning C for my CS50 course that I completed.

#### Workthrough tests.

My approach when testing is: I design test cases, AI implements them and I review and verify and improve the tests if needed. 

#### Automated Testing Approach

Testing is an essential part of software development and shouldn't be treated lightly. While AI can accelerate test development, relying on it entirely introduces risks, such as generating superficial tests that pass without thoroughly validating the application's behaviour.


To reduce these risks, I adopted the following approach:

1. **Test design:** Identify and define the important test cases myself, including successful connections, certificate expiry warnings and network failures.
2. **AI-assisted implementation:** Use an AI agent to implement the tests with pytest, following the test cases and requirements I defined.
3. **Manual review:** Review the generated tests in small batches to ensure the assertions and mocks correctly validate the intended behaviour.
4. **Test verification:** Deliberately introduce small changes to the application's logic and rerun pytest to confirm that the relevant tests detect incorrect behaviour.


> During Manual Review I am not going to review every line of the boilerplate generated but focus on the assertions and the mocks. 


#### AI pyTest Results:
`../../../.local/share/uv/python/cpython-3.15.2-linux-x86_64-gnu/lib/python3.15/unittest/mock.py:1241: ConnectionRefusedError

===================== short test summary info ======================

FAILED tests/test_config.py::test_missing_required_field_is_rejected[sites] - Failed: DID NOT RAISE any of (ValueError, KeyError, TypeError)
FAILED tests/test_config.py::test_missing_required_field_is_rejected[warn_days] - Failed: DID NOT RAISE any of (ValueError, KeyError, TypeError)
FAILED tests/test_config.py::test_missing_required_field_is_rejected[timeout_sec] - Failed: DID NOT RAISE any of (ValueError, KeyError, TypeError)
FAILED tests/test_config.py::test_empty_hostnames_list_is_rejected - Failed: DID NOT RAISE any of (ValueError, KeyError, TypeError)
FAILED tests/test_tls_checker.py::test_network_failure[timeout] - AssertionError: assert 'tim' in 'connection refused'
FAILED tests/test_tls_checker.py::test_network_failure[refused] - ConnectionRefusedError: connection refused

=================== 6 failed, 14 passed in 0.12s ===================`


#### Researching/Improving/Adding tests
Inside test_tls_checker.py: 
FAILED tests/test_tls_checker.py::test_network_failure[timeout] - AssertionError: assert 'tim' in 'connection refused'
FAILED tests/test_tls_checker.py::test_network_failure[refused] - ConnectionRefusedError: connection refused

ANSWER:
> This error was caused because I failed to differenciate between TimeOutError and kept ConnectionRefusedError in the same umbrella. Simply adding separate error execpt in try/except block inside tlsChecker.py solved the issue.


##### LEARNING IMP CONCEPTS:
1. @pytest.fixture: 

`@pytest.fixture
def tls_environment(monkeypatch):`

This is a fixture which prepares an object for a test needs. Any test with a tls_environment parameter receives the objects returned by this function.
So, pytest runs this fixture afresh for each test case, so changes from one case/test doesn't affect another.

2. MagicMock and Mock - It simply creates fake objects and functions.

3. monkeypatch - This temporarily replaces real functions with fake ones.

4. @pytest.mark.parametrize - This is important one. This runs the same test with different inputs. Example inside `test_results.py` 

@pytest.mark.parametrize("missing_field", ["sites", "warn_days", "timeout_sec"])

This runs the function it's called on 3 different times like in a loop so, first function called missing_field is sites and so on for 3 times.

5. tls_socket = context.wrap_socket.return_value.__enter__.return_value

This __enter__ is like wrapping dummy TCP connection and using with block. So, fake ssock object that my application will use inside the with block.


# FINAL REMARKS

This project gave me practical experience with TLS, sockets, command-line arguments, and automated testing in Python. Starting with a small connection example and gradually separating configuration, certificate checking, and reporting helped me understand each part before combining them.

One important lesson was that establishing a TCP connection does not guarantee a successful TLS handshake. Certificate verification and network failures also need handling. Automated tests exposed gaps that manual checks had missed, including incorrect timeout messages and an unhandled refused connection.

Working with AI-generated tests introduced another learning challenge. I needed to understand fixtures, parameterization, and mocks before I could assess whether the tests checked my application's behaviour correctly. AI helped with implementation, while I remained responsible for reviewing the assumptions and understanding the results.

The finished application focuses on checking TLS connectivity and certificate expiry when run. Scheduled monitoring, Slack notifications, and actual HTTP availability checks remain possible improvements.

The main outcome was learning how to break an unfamiliar problem into smaller steps, use documentation to make progress, and investigate failures rather than only checking successful results.