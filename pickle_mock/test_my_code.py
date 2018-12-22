import pickle_mock
# from pickle_mock.api import pickle, mock
from requests_html import HTMLSession

url = 'https://google.com'


def my_code(url, verify=False):
    """ We want to mock a portion of this function"""
    with HTMLSession() as s:
        r = s.get(url, verify=verify)
        if not r.ok:
            raise Exception('???')
        div = r.html.find('div', first=True)
        ps = r.html.find('p')
        return div, ps

# pickle will save the output of the correct call to HTMLSession.get...how to identify the correct call?
pickle_mock.pickle(name='my_function.HTMLSession.get', func=HTMLSession.get, args=('url',), kwargs={'verify': False})


@pickle_mock.mock('my_function.HTMLSession.get')  # this will set MagicMock(side_effect=open('my_function....
def test_my_code():
    my_div, my_ps = my_code()
    assert my_div == ''  # i'm not sure what this will be yet
    assert my_ps == []  # same
    # and then assert some things about my_div and my_ps
