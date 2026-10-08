from unittest.mock import MagicMock, call

import pytest

from mysql_wizard.conf import broadcast, listener


def test_advertise_database_server_registers_service(monkeypatch):
    zeroconf = MagicMock()
    service_info = MagicMock()
    service_info_type = MagicMock(return_value=service_info)

    monkeypatch.setattr(broadcast.socket, "gethostname", lambda: "test-host")
    monkeypatch.setattr(broadcast, "ServiceInfo", service_info_type)
    monkeypatch.setattr(broadcast, "Zeroconf", lambda: zeroconf)

    result = broadcast.advertise_database_server(port=3307)

    service_info_type.assert_called_once_with(
        listener.SERVICE_TYPE,
        f"test-host.{listener.SERVICE_TYPE}",
        port=3307,
        properties={
            "service": "darcoran",
            "database": "mysql",
        },
    )
    zeroconf.register_service.assert_called_once_with(service_info)
    assert result == (zeroconf, service_info)


def test_database_service_listener_stores_service_info_for_available_service():
    service_info = object()
    zeroconf = MagicMock()
    zeroconf.get_service_info.return_value = service_info
    service_listener = listener.DatabaseServiceListener()

    service_listener.add_service(zeroconf, listener.SERVICE_TYPE, "service-name")

    zeroconf.get_service_info.assert_called_once_with(
        listener.SERVICE_TYPE, "service-name"
    )
    assert service_listener.service_info is service_info


def test_database_service_listener_ignores_missing_service_info():
    zeroconf = MagicMock()
    zeroconf.get_service_info.return_value = None
    service_listener = listener.DatabaseServiceListener()

    service_listener.add_service(zeroconf, listener.SERVICE_TYPE, "service-name")

    assert service_listener.service_info is None


def test_database_service_listener_updates_service_info():
    first_info = object()
    updated_info = object()
    zeroconf = MagicMock()
    zeroconf.get_service_info.side_effect = [first_info, updated_info]
    service_listener = listener.DatabaseServiceListener()

    service_listener.add_service(zeroconf, listener.SERVICE_TYPE, "service-name")
    service_listener.update_service(zeroconf, listener.SERVICE_TYPE, "service-name")

    assert service_listener.service_info is updated_info
    assert zeroconf.get_service_info.call_args_list == [
        call(listener.SERVICE_TYPE, "service-name"),
        call(listener.SERVICE_TYPE, "service-name"),
    ]


def test_database_service_listener_remove_service_does_nothing():
    service_listener = listener.DatabaseServiceListener()
    service_listener.remove_service(
        MagicMock(), listener.SERVICE_TYPE, "service-name"
    )

    assert service_listener.service_info is None


def test_discover_database_server_returns_first_address_and_port(monkeypatch):
    service_info = MagicMock()
    service_info.parsed_addresses.return_value = ["192.0.2.10", "192.0.2.11"]
    service_info.port = 3306
    zeroconf = MagicMock()
    zeroconf.get_service_info.return_value = service_info

    monkeypatch.setattr(listener, "Zeroconf", lambda: zeroconf)
    monkeypatch.setattr(
        listener,
        "ServiceBrowser",
        lambda _zeroconf, _service_type, service_listener: (
            service_listener.add_service(
                zeroconf, listener.SERVICE_TYPE, "service-name"
            )
        ),
    )

    result = listener.discover_database_server(timeout=1)

    assert result == ("192.0.2.10", 3306)
    zeroconf.close.assert_called_once_with()


def test_discover_database_server_raises_when_no_service_is_found(monkeypatch):
    zeroconf = MagicMock()
    monkeypatch.setattr(listener, "Zeroconf", lambda: zeroconf)
    monkeypatch.setattr(
        listener,
        "ServiceBrowser",
        lambda *_args: None,
    )

    with pytest.raises(RuntimeError, match="No Darcoran database server"):
        listener.discover_database_server(timeout=0)

    zeroconf.close.assert_called_once_with()


def test_discover_database_server_raises_when_service_has_no_address(monkeypatch):
    service_info = MagicMock()
    service_info.parsed_addresses.return_value = []
    zeroconf = MagicMock()
    zeroconf.get_service_info.return_value = service_info
    monkeypatch.setattr(listener, "Zeroconf", lambda: zeroconf)
    monkeypatch.setattr(
        listener,
        "ServiceBrowser",
        lambda _zeroconf, _service_type, service_listener: (
            service_listener.add_service(
                zeroconf, listener.SERVICE_TYPE, "service-name"
            )
        ),
    )

    with pytest.raises(RuntimeError, match="has no address"):
        listener.discover_database_server(timeout=1)

    zeroconf.close.assert_called_once_with()


def test_is_mysql_running_locally_returns_true_when_connection_succeeds(monkeypatch):
    connection = MagicMock()
    create_connection = MagicMock(return_value=connection)
    monkeypatch.setattr(listener.socket, "create_connection", create_connection)

    assert listener.is_mysql_running_locally("db.example", 3307, 0.5) is True
    create_connection.assert_called_once_with(
        ("db.example", 3307),
        timeout=0.5,
    )
    connection.__enter__.assert_called_once_with()
    connection.__exit__.assert_called_once()


def test_is_mysql_running_locally_returns_false_for_socket_errors(monkeypatch):
    monkeypatch.setattr(
        listener.socket,
        "create_connection",
        MagicMock(side_effect=OSError("connection refused")),
    )

    assert listener.is_mysql_running_locally() is False
