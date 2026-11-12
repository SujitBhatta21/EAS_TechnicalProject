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

