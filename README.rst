===========
pickle mock
===========

Note: This repository serves as a proof-of-concept and came about off the cuff.  It has served its purpose
and will hopefully lead to further ideas.

With a name like 'pickle mock', I would say this library does something like pickle mock your tests.

What does that mean exactly?  I'm not sure yet, but here is an example of some code you might have in a project::

    # my_code_file.py
    from requests_html import HTMLSession

    def my_code():
        with HTMLSession() as s:
            r = s.get('https://google.com')
            if not r.ok:
                raise Exception('???')
            div = r.html.find('div', first=True)
            ps = r.html.find('p')
            return div, ps

Then you might want to test it::

    from my_code_file import my_code

    def test_my_code():
        my_div, my_ps = my_code()
        # and then assert some things about my_div and my_ps

All right, so I had some code like this and the tests were taking a long time because a lot of requests
were being made.  I wanted to mock the request so that it didn't actually make the request.  vcrpy is a library
that will do this automatically, but wasn't working for me because I am using a proxy.  It looks like a long-standing
bug.  I chose to write a custom class that mirrored some of the aspects of the response 'r' so that default responses
were provided and I didn't actually need to make the time consuming requests::

    class CustomResponse:
        def __init__():
            self.ok = True
            self.html = CustomHTML()

Oh, it looks like I also needed to mirror some aspects of the r.html.html attribute as well::

    class CustomHTML:
        def find(*args, first)
            return # don't return None, but something useful, how about the element?

So for the above example, my mock test might look like::

    from unittest.mock import MagicMock
    from requests_html import HTMLSession

    def get(*args, *kwargs)
        return CustomResponse()

    HTMLSession.get = MagicMock(side_effect=get)

    def test_my_code():
        def test_my_code():
        my_div, my_ps = my_code()
        # and then assert some things about my_div and my_ps

So, with mocking, instead of HTMLSession.get doing it's normal thing, it is now returning an instance of CustomResponse.

That wasn't too bad I suppose.  But this method doesn't seem like a good idea. Let's suppose my code changes to::

    from requests_html import HTMLSession
    with HTMLSession() as s:
        r = s.get('https://google.com')
        if r.status_code != 200:  # <--------  see, I changed it here
            raise Exception('???')
        div = r.html.find('div', first=True)
        ps = r.html.find('p')

Now, I need to remember to change the CustomResponse class!::

    class CustomResponse:
        def __init__():
            self.ok = True
            self.html = HTML()
            self.status_code = 200

It seems like these small changes can get out of hand.  There must be a better way.  I'm sure there are a lot of
solutions, but I think this one is pretty general...once I create my code, what if my responses to functions could be
saved so that they were the exact response instead of one that I hand craft.  Pickle, isn't that what you do?


With pickle mock
________________

Here's my test again::

    def test_my_code():
        my_div, my_ps = my_code()
        # and then assert some things about my_div and my_ps

Now, this time, the first time your code runs, it doesn't mock.  What it does is actually make the request.  The
response 'r' will be pickled and each time you run your test in the future, this pickled response will be used
instead.

Let's add in the pickle mock code::

    import pickle_mock
    from my_code_file import my_code
    from requests_html import HTMLSession

    @pickle_mock.pickle_mock(func=HTMLSession.get, args=('https://google.com', ))
    def test_my_code():
        my_div, my_ps = my_code()
        # and then assert some things about my_div and my_ps


So, using pickle_mock, all of the mocking is done through being pickled.  The assumptions are that most things are
pickle-able and that your tests can actually be run one time irrespective of mocking.  Is this a good idea?
I'm not sure.  Right now it doesn't seem like a bad one.
