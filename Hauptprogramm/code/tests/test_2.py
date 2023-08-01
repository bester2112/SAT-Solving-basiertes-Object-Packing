import src._main2 as test1

test1.hello()

def test_hello():
	assert test1.hello() == "hello"

def test_hello_2():
	assert test1.hello() == "hello"