#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from mongoengine import *

connect('test')

# 定义文档
class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
        
class Post(Document):
    title = StringField(max_length=120, required=True)
    # ReferenceField相当于foreign key
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    # 允许继承
    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()

# 添加数据
john = User(email = 'john@example.com',first_name = 'John', last_name = 'Tony')
john.save()
ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()
post1 = TextPost(title='Fun with MongoEngine', author=john)
post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
post1.tags = ['mongodb', 'mongoengine']
post1.save()

post2 = LinkPost(title='MongoEngine Documentation', author=ross)
post2.link_url = 'http://docs.mongoengine.com/'
post2.tags = ['mongoengine']
post2.save()

# 查看数据
for post in Post.objects:
    print post.title
    print '=' * len(post.title)

    if isinstance(post, TextPost):
        print post.content

    if isinstance(post, LinkPost):
        print 'Link:', post.link_url
    
for post in TextPost.objects:
    print post.content

# 通过标签查询    
for post in Post.objects(tags='mongodb'):
    print post.title
    
num_posts = Post.objects(tags='mongodb').count()
print 'Found %d posts with tag "mongodb"' % num_posts