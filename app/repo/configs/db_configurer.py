from dataclasses import dataclass
from pathlib import Path
from ipaddress import IPv4Address

from configparser import ConfigParser
from .config_path import CONFIG_FILE, CONFIG_DIR

class DBConfig:
    path: Path = CONFIG_FILE
        
    def get_configuration(self) -> dict:
        config = ConfigParser()
        if not config.read(CONFIG_FILE):
            raise FileNotFoundError(
                f"Configuration file not found: {CONFIG_FILE}. Please ensure the file exists and is readable."
            )
        db_config = config["database"]
        configs = DBConfigData.create_config(db_config)
        return configs
    
    def create_config_file(self, host: str, password: str) -> None:
        config = ConfigParser()
        _configs = DBConfigData(host=host, password=password)
        config["database"] = {
            "host": _configs.host,
            "port": _configs.port,
            "name": _configs.name,
            "user": _configs.user,
            "password": _configs.password,
        }
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
            
    def check_config_file_exists(self) -> bool:
        return CONFIG_FILE.exists()
    
    
@dataclass
class DBConfigData:
    host: str
    password: str
    port: int = 3306
    name: str = "darcoran"
    user: str = "darcoran_app"
    
    def __post_init__(self):
        # Validate the host as an IPv4 address
        try:
            IPv4Address(self.host)
        except ValueError:
            raise ValueError(f"Invalid IPv4 address: {self.host}")
    
    @classmethod
    def create_config(cls, config) -> "DBConfigData":
        return cls(
            host=config.get("host", "localhost"),
            password=config.get("password", ""),
            port=config.getint("port", 3306),
            name=config.get("name", "darcoran"),
            user=config.get("user", "darcoran_app"),
        )