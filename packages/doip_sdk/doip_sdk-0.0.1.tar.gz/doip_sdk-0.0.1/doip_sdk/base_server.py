import ssl
from pathlib import Path
from socketserver import ThreadingTCPServer

from doip_sdk.base import DOIPHandler
from doip_sdk.selfsigned import generate_selfsigned_cert


class DOIPServer(ThreadingTCPServer):

    def __init__(self, host: str, port: int, handler: DOIPHandler, key_cert_files: tuple[str, str] | None = None,
                 bind_and_activate=True):
        super(DOIPServer, self).__init__((host, port), handler, bind_and_activate=False)

        # Auto generate a self-signed certificate, if not provided
        if key_cert_files:
            key_file, cert_file = key_cert_files
        else:
            key, cert = generate_selfsigned_cert(hostname=host)

            key_file = Path('ssl/key.pem')
            cert_file = Path('ssl/cert.pem')
            key_file.parent.mkdir(parents=True, exist_ok=True)

            with key_file.open('wb+') as f:
                f.write(key)
            with cert_file.open('wb+') as f:
                f.write(cert)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        self.socket = context.wrap_socket(self.socket, server_side=True)

        # Keep the paths so that we can delete them later
        self.key_file = key_file
        self.cert_file = cert_file

        if bind_and_activate:
            self.server_bind()
            self.server_activate()

    def _remove_certificate(self):
        # Remove self-signed certificate
        self.key_file.unlink(missing_ok=True)
        self.cert_file.unlink(missing_ok=True)
        self.key_file.parent.rmdir()

    def start(self):
        """Call this method to start the server."""
        try:
            self.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            print('Shutting down the server')
        finally:
            self._remove_certificate()
