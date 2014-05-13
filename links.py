#!/usr/bin/env python

from github import Github
from github.InputFileContent import InputFileContent
from urlparse import urlparse
import sys
import os
import urllib2

AUTH_TOKEN = ""
GIST_ID = "45879bad62b9a7bd9f62"
FILENAME = "links.md"

def get_header(link):
    response = urllib2.urlopen(link)
    html = response.read()
    import re
    return re.search("<h1>(.*?)</h1>", html).group(1)

def get_gist_filename(link):
    parse_result = urlparse(link).path
    return "{}.md".format(os.path.split(parse_result)[1])


if len(sys.argv) < 2:
    raise ValueError

link = sys.argv[1]

link_title = get_header(link)
link_md = get_gist_filename(link)

g = Github(AUTH_TOKEN)
user = g.get_user()

link_gist_blob = InputFileContent(content="* [{}]({})".format(link_title, link))

link_gist = user.create_gist(public=True,
                             description=link_title,
                             files={link_md: link_gist_blob})

gist = g.get_gist(GIST_ID)
gist_files = gist.files
blob = gist_files[FILENAME].content
blob += "\n\n* [{}]({})".format(link_title, link_gist.html_url)
blob = InputFileContent(content=blob)
gist.edit(files={FILENAME: blob})
