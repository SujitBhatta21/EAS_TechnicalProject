Mental Model for project.
- 
- Spend about 5-7 hrs spanning over 4-7 days with regular commits.
- Go to company site and skim through projects or case studies which will definitely give me some inspirations.
- Requirements gathering, Language choice, new concept learning draft roadmap figured out in first hr.



## Company Research
### Company MOTO: 
> UNDERSTAND -> DESIGN -> DEVELOP

(FUN COINCIDENCE: ARCUS AI-Powered Building Intelligence project from EAS used YOLO. I have used YOLO in one of my project as well)




## Project Requirements Research (Why that stack?)

### DAY 1
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



### DAY2
Looking into how TLS works and verifying a TLS cert.

1. Establishing connection with URL.
2. Performing TLS handshake using ssl library python3 (why: )
3. Checking if certificate is expired or not.
4. Return something...

**ANSWER**:
    Reading python docs for ssl library gave me sample template to connect to the hostname URL to print TLS version(). 
    Further reseatch using Ctrl + F for certificates helped me find getpeercert() function which returned a JSON with 'notAfter' (i.e. expiry date) which is exactly what I needed.
    Example print with hostname='example.com' for this function.: 
> {'subject': ((('commonName', 'example.com'),),), 'issuer': ((('countryName', 'US'),), (('organizationName', 'SSL Corporation'),), (('commonName', 'Cloudflare TLS Issuing ECC CA 3'),)), 'version': 3, 'serialNumber': '01EEE6AABB521D5E14FC315FD9985690', 'notBefore': 'Sep 26 22:49:11 2026 GMT', '**notAfter**': 'Dec 25 22:56:35 2026 GMT', 'subjectAltName': (('DNS', 'example.com'), ('DNS', '*.example.com')), 'OCSP': ('http://o.cf-i.ssl.com',), 'caIssuers': ('http://i.cf-i.ssl.com/Cloudflare-TLS-I-E3.cer',), 'crlDistributionPoints': ('http://c.cf-i.ssl.com/ae801ed1c55bb579d79208b0d772acfb8cc3a208.crl',)}

### DAY3
It was bhai tika a festival in Tihar(Diwali) so, whole day well spent with family and friends.

### DAY4
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


During my code session trying to build `print_report()` method I learned new thing. I can use `:>number` for amount of align space I want inside a format string print. **Remember** it's :> then left align :< then right align. Example `>>>> f"{result.status:<7}`"


## FINAL REMARKS
