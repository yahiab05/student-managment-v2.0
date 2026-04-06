import pytest 
from datetime import date

from app.utils.utils import (
    set_username, get_username,
    pydate_to_qdate
)

def test_username():
    username = "yahia"
    
    set_username(username)
    assert get_username() == username
    
def test_pydate_to_qdate():
    pydate = date(2023, 1, 1)
    qdate = pydate_to_qdate(pydate)
    assert isinstance(qdate, QDate)
    assert qdate == QDate(2023, 1, 1)
    