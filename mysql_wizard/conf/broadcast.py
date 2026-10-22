# mysql_wizard/core/server.py

import socket

from zeroconf import Zeroconf, ServiceInfo

from mysql_wizard.conf.listener import SERVICE_TYPE


def advertise_database_server(hostname=None, port=3306):
    
    if hostname is None:
        raise ValueError("hostname must be provided")

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