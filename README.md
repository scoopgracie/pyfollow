# pyfollow
"Follow" a Twitter user from the command line. No Twitter account required!

Currently, only Linux is officially supported. PyFollow will not work on
Windows. It may work on a Mac, but this is not guaranteed.

## Install
First, install Google Chrome. Next, get the `chromedriver` for your platform.
Install `selenium` with `pip`, `pipenv`, or your preferred Python package
manager. To install PyFollow, run:

    sudo cp pyfollow.py /usr/bin/pyfollow

To configure, run `pyfollow` on the command line. It will ask for the paths to
(not the names of) the Chrome and `chromedriver` binaries, then it will ask
for a user to follow (e.g. "someuser", not "@someuser" or "Some User"). After
this, it will pause for a while, then "dump" a bunch of tweets from that user.

## Usage
To check the default user's tweets again later, just type `pyfollow`. To check
tweets from a different user, use `pyfollow <user>`. Note that with any user,
PyFollow only shows tweets you have not seen.

