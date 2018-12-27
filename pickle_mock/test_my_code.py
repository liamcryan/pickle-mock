import pickle_mock
# from pickle_mock.api import pickle, mock
from requests_html import HTMLSession

url = 'https://google.com'
verify = False


def my_code(url, verify=False):
    """ We want to mock a portion of this function"""
    with HTMLSession() as s:
        r = s.get(url, verify=verify)
        if not r.ok:
            raise Exception('???')
        div = r.html.find('div', first=True)
        ps = r.html.find('p')
        return div, ps


@pickle_mock.pickle_mock(func=HTMLSession.get, args=(url,), kwargs={'verify': verify})
def test_my_code():
    my_div, my_ps = my_code(url=url, verify=verify)
    assert my_div.attrs == {'class': ('ctr-p',), 'id': 'viewport'}
    assert my_ps[0].full_text == 'Your Google Account'


if __name__ == '__main__':
    test_my_code()