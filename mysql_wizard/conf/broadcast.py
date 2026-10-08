# mysql_wizard/core/server.py

import socket

from zeroconf import Zeroconf, ServiceInfo

from mysql_wizard.conf.listener import SERVICE_TYPE


def advertise_database_server(port=3306):
    hostname = socket.gethostname()

    service_name = f"{hostname}.{SERVICE_TYPE}"

    service_info = ServiceInfo(
        SERVICE_TYPE,
        service_name,
        port=port,
        properties={
            "service": "darcoran",
            "database": "mysql",
        },
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(service_info)

    return zeroconf, service_info