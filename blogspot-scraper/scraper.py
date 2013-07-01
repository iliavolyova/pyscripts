'''
Created on Jun 27, 2013

@author: neuro
'''
from __future__ import division
from bs4 import BeautifulSoup
import requests

links = []
posts_dict = {}
post_count = 0

def parse_archive(link):
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data)
    
    posts = soup.find_all(attrs={'class' : ('post')})
    for post in posts:
        title = post.find(attrs={'class' : ('post-title')})
        body = post.find(attrs={'class' : ('post-body')})
        posts_dict[title] = body
        global post_count
        post_count = post_count + 1

if __name__ == '__main__':
    
    r = requests.get("http://unqualified-reservations.blogspot.com/")
    data = r.text
    soup = BeautifulSoup(data)
    
    archives = soup.find(attrs={'class' : ('archive-list')})
    for link in archives.find_all('a'):
        links.append(link.get('href'))
    
    for link in links:
        parse_archive(link)
    
    wordcount = 0
    word_len = 0
    
    for post in posts_dict:
        words_title = str(post).split(' ')
        for word in words_title:
            word_len = word_len + len(word)
        words_title_count = len(words_title)
        words_body = str(posts_dict[post]).split(' ')
        for word in words_body:
            word_len = word_len + len(word)
        words_body_count = len(words_body)
        wordcount = wordcount + words_title_count + words_body_count
    
    print ("Target: http://unqualified-reservations.blogspot.com/")
    print ("Number of posts: "), post_count
    print ("Number of words: "), wordcount
    print ("Average word length: "), word_len / wordcount
    print ("Number of book pages: "), wordcount / 250
        
