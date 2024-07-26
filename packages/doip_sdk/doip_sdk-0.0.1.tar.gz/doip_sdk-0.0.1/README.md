# DOIP-SDK

This is the Software Development Kit (SDK) for DOIP implementation in Python. It provides a template for DOIP servers as
well as some utility methods to facilitate the implementation. Please check our [documentation page][3].

## Quick start

### Server side

For example, you want to implement a DOIP server, first define a handler.

```python
from doip_sdk import DOIPHandler, DOIPResponse, ResponseStatus, SocketReader, write_string_segment, write_empty_segment


class MyHandler(DOIPHandler):
    def hello(self, first_segment: dict, _: SocketReader):
        # Create a response object
        output = {
            'hello': 'world',
        }
        response = DOIPResponse(status=ResponseStatus.SUCCESS, output=output)

        # Send the response
        write_string_segment(socket=self.request, message=response.model_dump_json(exclude_none=True))
        write_empty_segment(socket=self.request)

    def create(self, first_segment: dict, reader: SocketReader):
        # Get the second segment
        chunk = next(reader.get_chunks())

        # Further processing
        print(chunk.decode('utf-8'))
```

Your handler should override methods for the operations. A list of the methods which can be overridden can be found in
the [template](#derive-from-the-template) section. For each method, besides the `self`, the first parameter is the
first segment in the request. The second parameter is a `SocketReader`, which can be used to read other segments. It has
a
method `get_all_segments`, which returns a [generator][2]. Simply call `next()` on it to get the next segment, as shown
in the example code above.

Then, create a `DOIPServer` instance and start it.

```python
from doip_sdk import DOIPServer

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999
    server = DOIPServer(HOST, PORT, MyHandler)
    server.start()
```

According to the DOIP Specification, all communication must take place over a secured channel. Therefore, if a private
key and a certificate are not provided, the `DOIPServer` generates a self-signed certificate and use it. For that
reason, when connecting to such a server, remember to ignore the certificate validation (as done in the
[client example](#client-side) below).

### Client side

An example client for the server above might look like this:

```python
import json
import socket
import ssl

from doip_sdk import write_string_segment, write_empty_segment, SocketReader

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # To ignore the self-signed certificate
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as secured_socket:
            data = {
                'operationId': '0.DOIP/Op.Hello'
            }

            # Send request
            write_string_segment(secured_socket, json.dumps(data))
            write_empty_segment(secured_socket)

            # Print response
            reader = SocketReader(socket=secured_socket)
            segments = []
            chunks = reader.get_chunks()
            while True:
                segment = next(chunks, None)
                if not segment:
                    break
                if segment != b'@':
                    segments.append(segment)
                else:
                    file = bytearray()
                    while True:
                        file_chunk = next(chunks)
                        if file_chunk == b'#':
                            break
                        file.extend(file_chunk)
                    segments.append(file)

            print('--------------')
            print(segments)
```

## Derive from the template

To implement a DOIP server, one needs to define a handler, which will handle incoming requests. To take advantage of
this package, a handler should inherit the `DOIPHandler`.

In the handler, one can define methods which will be used to handle DOIP operations. Currently, all methods which can be
overridden are:

* `hello`
* `create`
* `retrieve`
* `update`
* `delete`
* `search`
* `list_operation`
* `extended_operation`

Each method will be called respectively based on the `operationId` from the client. If the `operationId` does not refer
to a basic operation, the `extended_operation` method will be triggered instead. It is not required to implement all
those methods. If the client asks for an unsupported operation, the server will simply respond with an error message.

## Utility methods

### Read request/response stream

To read the body of a request or response, please use the `SocketReader` class. The code below creates an instance of
the `SocketReader` class and print all segments in the socket.

```python
from doip_sdk import SocketReader

# Create a socket
socket = ...

# Create a read buffer
reader = SocketReader(socket=socket)

for segment in reader.get_chunks():
    print(segment.decode('utf-8'))
```

The only method of the `SocketReader` that can be called is `get_all_segments`, which returns a [generator][2]. You can
loop through it, or simply call `next(buffer.get_all_segments())` to get the next segment. To send out a response,
please use the utility methods from the `from doip_sdk.utils` package.

### Send data over a socket

To send DOIP conformed data over a socket, the DOIP-SDK currently offers 4 methods:

1. `write_string_segment`: as the name suggests, this method sends a string over a socket and a `#` sign to indicate the
   end of the segment.
2. `write_file_segment`: this method send a DOIP conformed byte segment (a segment starts with an `@` sign).
3. `write_empty_segment`: this method simply sends a `#` sign over a socket. The sender can use this method to indicate
   the end of the data stream.
4. `send_unknown_operation_response`: this method sends out a DOIP response with `output.reason` saying "This operation
   is not supported."
5. `send_invalid_request_response`: this method takes a `reason` as a parameter and send out a DOIP response with the
   provided `reason` in the `output.reason`.

[1]: https://docs.python.org/3/library/socketserver.html

[2]: https://wiki.python.org/moin/Generators

[3]: https://doip.pages-ce.gwdg.de/doip-sdk/