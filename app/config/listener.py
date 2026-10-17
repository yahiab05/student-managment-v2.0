# mysql_wizard/core/discovery.py

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import socket


SERVICE_TYPE = "_darcoran._tcp.local."


class DatabaseServiceListener(ServiceListener):
    def __init__(self):
        self.service_info = None

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.service_info = info

    def update_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.service_info = info

    def remove_service(self, zeroconf, service_type, name):
        pass


def discover_database_server(timeout=3000):
    zeroconf = Zeroconf()

    listener = DatabaseServiceListener()

    browser = ServiceBrowser(
        zeroconf,
        SERVICE_TYPE,
        listener,
    )

    try:
        import time

        deadline = time.monotonic() + timeout / 1000

        while (
            listener.service_info is None
            and time.monotonic() < deadline
        ):
            time.sleep(0.05)

        if listener.service_info is None:
            raise RuntimeError(
                "No Darcoran database server was found."
            )

        info = listener.service_info

        addresses = info.parsed_addresses()

        if not addresses:
            raise RuntimeError(
                "Database server was found but has no address."
            )

        return addresses[0], info.port

    finally:
        zeroconf.close()
        
def is_mysql_running_locally(
    host="127.0.0.1",
    port=3306,
    timeout=0.3,
):
    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            return True
    except OSError:
        return False