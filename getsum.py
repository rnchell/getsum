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

import sys,urllib2, urllib,getopt
from HTMLParser import HTMLParser

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
	return

def is_int(s):
	try: 
	  int(s)
	  return True
	except ValueError:
	  return False

def main(argv):
	amount = ''
	what = ''

	if len(argv) != 2:
		print """>>> Error: not enough arguments provided. 
Must specify amount of words/paragraphs and what - words (w, word, words) 
or paragraphs (p, para, paras, paragraphs) e.g. 5 words"""

		return

	if is_int(argv[0]):
		amount = argv[0]

	if argv[1] in ['p', 'para', 'paras', 'paragraphs']:
		what = 'paras'
	elif argv[1] in ['w', 'word', 'words']:
		what = 'words'

	url = 'http://www.lipsum.com/feed/html'

	values = {
		'amount':amount,
		'what':what,
		'start':'yes',
		'generate':'Generate Lorem Ipsum'
	}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	page = response.read()

	parser = LipsumParser()
	parser.feed(page)

	for d in parser.data:
		print d

if __name__ == "__main__":
    main(sys.argv[1:])
