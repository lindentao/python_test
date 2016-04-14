#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime

connect('test')

class BlogPost(Document):
    title = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.now())
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}

class TextPost(BlogPost):
    content = StringField(required=True)

class LinkPost(BlogPost):
    url = StringField(required=True)

# Create a text-based post
post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
post1.tags = ['mongodb', 'mongoengine']
post1.save()
# Create a link-based post
post2 = LinkPost(title='MongoEngine Docs', url='hmarr.com/mongoengine')
post2.tags = ['mongoengine', 'documentation']
post2.save()

for post in BlogPost.objects:
    print '===', post.title, '==='
    if isinstance(post, TextPost):
            print post.content
    elif isinstance(post, LinkPost):
        print 'Link:', post.url
    print
