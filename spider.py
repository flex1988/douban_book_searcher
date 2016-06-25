from bs4 import BeautifulSoup
from lxml import html
import requests

base = 'http://book.douban.com/subject/'

def query_book_comments(book_id):
    r = requests.get(base+book_id+'/comments')
    soup = BeautifulSoup(r.text,"lxml")
    comment_lis = soup.findAll('li',{'class':'comment-item'})
    comments = []

    for li in comment_lis:
        comment = {}
        comment['vote'] = li.find('span',{'class':'vote-count'}).string
        author = li.find('span',{'class':'comment-info'})
        comment['author'] = author.find('a').string
        comment['content'] = li.find('p',{'class':'comment-content'}).string
        comments.append(comment)

    comments = sorted(comments,key=lambda x:int(x['vote']),reverse=True)
    return comments

