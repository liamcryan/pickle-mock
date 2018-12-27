I am trying to figure this out...

a.py
____

from requests_html import HTMLSession

def a():
    with HTMLSession() as s:
        return s.get('http://www.google.com')


b.py
____
from a import a

def test_a():
    assert a() is not None


How can I alter the behavior of s.get within b.py?  Something like below?


b.py ((cont))
_____________
from a import a
from requests_html import HTMLSession

@decorator(alter=HTMLSession.get, args=('http://www.google.com', ))
def test_a():
    assert a() is not None
