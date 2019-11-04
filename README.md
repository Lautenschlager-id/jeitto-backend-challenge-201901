# Phone Recharge

## Setting up
First, run `git clone` this repository.

### Dependencies
Run `pip3 install -r requirements.txt` to install the requirements to run the challenge.

### MongoDB
###### If you do not have it installed, please follow this guide: **https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/**
Start the database server by running `sudo service mongod start`. You can check whether it's connected or not by running `sudo service mongod status`.

## Tests
You can run the tests by executing the file `test.py` with the command `python3 test.py`.

All tests are located in the folder `/tests` and it may populate some data.

## Documentation
You can read the documentation in the file [**DOCS.md**](DOCS.md)

## Q & A
Q: What were the main challenges you have faced during the development?

A: Thinking about the API structure and how it would look like took me a certain time.<br>
Working with MongoDB in 32 bits was also a bit painful, but gave me a lot of experience on how to install it in machines in precarious situation (aka mine).

Q: What did you choose as framework and database and why?

A: As framework I choose Flask, since it's widely used and has a lot of topics in the internet that guided me through the challenge development.<br>
As database I choose MongoDB (managed by PyMongo) since it's lightweight in comparison to the alternatives and is very easy to use and set up.

Q: What's missing to be developed / how could we improve your project?

A: If the endpoint was about to be used in a huge company, Flask would certainly be a problem since it's not really asynchronous (even though there are some solutions using Celery). Probably a switch to Sanic would solve it, but it was a framework I had no experience with when I faced the challenge.

Q: Is Python the best choice for this project? Why?

A: Even though I'm not a big fan of the language, it's very efficient and easy to use and clearly fits all the needs for the project. There is an impressively huge community of webdevs using Python. I would probably choose JavaScript over Python due to my familiarity with it.

## Soundtrack
- [Welcome to Hell](https://open.spotify.com/album/6yr2eD95NnZk5yUE6wNAPG)