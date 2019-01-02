"""

Suppose you have a file like this that tests your code.

The function is called 'my_code' and the test for this function is 'test_my_code'.

To define the mocks you can specify a directory and then set the function you would like to
mock equal to AutoMock.auto_mock...

The first time you run the test, the test will act normally ie, will not mock.  During
this first run, the response will be saved and used in subsequent runs.

This is useful for interacting with 3rd party APIs.

To try this out, run this file.  Requests to the internet will be made.  You will see a new file that has been
created as well.  This file contains the response of the actual call and will serve as the mock response.

Run the file again.  No requests to the internet this time!  This can work for databases too, right?  Lots of things
I suppose.

"""

import os

from pickle_mock import AutoMock

from requests_html import HTMLSession

url = 'https://google.com'
verify = False

# set the mock directory
AutoMock.directory = os.path.abspath(os.path.dirname(__file__))

# define the mocks.  replaces method with a mock method
HTMLSession.get = AutoMock.auto_mock(method=HTMLSession.get, method_args=(url,), method_kwargs={'verify': verify})


def my_code(url, verify=False):
    """ We want to mock a portion of this function"""
    with HTMLSession() as s:
        r = s.get(url, verify=verify)
        if not r.ok:
            raise Exception('???')
        div = r.html.find('div', first=True)
        body = r.html.find('body', first=True)
        return div, body


def test_my_code():
    my_div, my_body = my_code(url=url, verify=verify)
    assert my_div.attrs == {'class': ('ctr-p',), 'id': 'viewport'}
    assert my_body.attrs == {'class': ('hp', 'vasq'), 'id': 'gsr'}


if __name__ == '__main__':
    test_my_code()