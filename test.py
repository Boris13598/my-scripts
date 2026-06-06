import os
import sys

def say_hello(count):
	for i in range(count):
		print('hello')
	os.exit(1)

def main():
	c = sys.argv[1]
	say_hello(c)

if __name__ == '__main__':
	main()
