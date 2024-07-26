import json
from json import JSONDecodeError
from socketserver import BaseRequestHandler

from doip_sdk.constant import Operation
from doip_sdk.utils import SocketReader, send_unknown_operation_response, send_invalid_request_response


class DOIPHandler(BaseRequestHandler):
    """
    This is the base class for all DOIP-conformed handler. Whenever a new handler is implemented, it must inherit from
    this class. One do not create an instance of a handler directly, but rather pass the handler class to the
    :py:class:`DOIPServer` to create a DOIP server.
    """

    def hello(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def create(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def retrieve(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def update(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def delete(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def search(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def list_operations(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def extended_operation(self, first_segment: dict, _: SocketReader):
        send_unknown_operation_response(self.request, first_segment.get('requestId'))

    def handle(self):
        reader = SocketReader(self.request)
        first_segment = next(reader.get_chunks()).decode('utf-8')

        if not first_segment.startswith('{'):
            send_invalid_request_response(socket=self.request, reason='The first segment is not a JSON object.')
            return

        try:
            first_segment = json.loads(first_segment)
        except JSONDecodeError:
            send_invalid_request_response(
                socket=self.request,
                reason='Cannot parse the JSON object from the first segment.'
            )
            return

        match first_segment['operationId']:
            case Operation.HELLO.value:
                self.hello(first_segment, reader)
            case Operation.CREATE.value:
                self.create(first_segment, reader)
            case Operation.UPDATE.value:
                self.update(first_segment, reader)
            case Operation.DELETE.value:
                self.delete(first_segment, reader)
            case Operation.SEARCH.value:
                self.search(first_segment, reader)
            case Operation.LIST_OPERATION.value:
                self.list_operations(first_segment, reader)
            case _:
                self.extended_operation(first_segment, reader)
