from app.config.listener import is_mysql_running_locally, discover_database_server
from app.config.broadcast import advertise_database_server

def set_host_and_port():
    if is_mysql_running_locally():
        host = "127.0.0.1"
        port = 3306
        broadcast, _ = advertise_database_server(
                        hostname=host, 
                        port=port
                        )
    else:
        try:
            host, port = discover_database_server()
            if host is None or port is None:
                raise RuntimeError(
                    "No Darcoran database server was found."
                )
        except RuntimeError as e:
            from app.utils import error
            error(str(e))
            return None, None
    return host, port