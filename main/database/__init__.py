from typing import Optional

from database.dao_psql import *

_DAO: Optional[DAOBase] = None


def get_DAO() -> DAOBase:
    """
    Get the DAO object. If it does not exist, create it.
    Singleton pattern.

    :return: The DAO object.
    """
    global _DAO
    if _DAO is None:
        _DAO = DAOPostgreSQL()
    return _DAO
