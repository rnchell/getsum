#!/usr/bin/python
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys,urllib2, urllib,getopt,os,argparse
from subprocess import Popen, PIPE, STDOUT
from HTMLParser import HTMLParser

parser = None
amount = ''
format = ''
echo = False

class LipsumParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.processing = False
		self.data = []

	def handle_starttag(self, tag, attrs):
		if tag != 'div':
			return
		for name, value in attrs:
			if name == 'id' and value == 'lipsum':
				self.processing = True
				break
				
	def handle_endtag(self, tag):
		if tag == 'div' and self.processing:
			self.processing = False

	def handle_data(self, data):
		if not self.processing:
			return
		self.data.append(data.strip())

def usage():
	parser.print_help()

def is_int(s):
	try: 
	  int(s)
	  return True
	except ValueError:
	  return False

def args_init():
	global parser

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--format',help='Format - words or paragraphs.')
	parser.add_argument('-a', '--amount',help='Amount of words or paragraphs.')
	parser.add_argument('-e', '--echo',help='Output to stdout',action='store_true')

def parse_args():
	global amount,format,echo

	args = parser.parse_args()

	if not args.format or not args.amount:
		usage()
		return

	if is_int(args.amount):
		amount = args.amount
	else:
		usage()
		return


	if args.echo:
		echo = True

	if args.format in ['p','para','paras','paragraph','paragraphs']:
		format = 'paras'
	elif args.format in ['w','word','words']:
		format = 'words'
	else:
		usage()

def main(argv):
	global format,amount,echo

	args_init()
	parse_args()

	url = 'http://www.lipsum.com/feed/html'

	values = {
		'amount':amount,
		'what':format,
		'start':'yes',
		'generate':'Generate Lorem Ipsum'
	}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	page = response.read()

	parser = LipsumParser()
	parser.feed(page)

	ipsum = ''
	for d in parser.data:
		ipsum += d + '\r\n'

	if os.name == 'posix' and not echo:
		p = Popen('pbcopy', stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		result = p.communicate(input=ipsum)
	else:
		print ipsum


if __name__ == "__main__":
    main(sys.argv[1:])
