from .baseclass import Database
from .msdatabase import MsSQLDatabase
from .mariadatabase import MariaDatabase

def create_db_manager(manager: str, **kwargs) -> Database:
    managers = {
        'MS': MsSQLDatabase(**kwargs),
        'Maria': MariaDatabase(**kwargs)
    }
    if manager not in managers:
        raise ValueError(f"No factory is implemented for provided value {manager}")
    return managers[manager]