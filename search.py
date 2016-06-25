#!/usr/bin/python
import sys
import argparse
import requests
from spider import *

douban = 'https://api.douban.com'

def usage():
    print """
        -l limits default 20
        -q query keyword
        -s minimum score default 7
        -h help

        eg. douban_book -s 8 -q docker -l 100
        """
def print_books(books):
    if len(books) == 0:
        print 'None results'
        sys.exit(0)
    for book in books:
        print 'Name: '+book['title']
        print 'id: '+book['id']
        if book['author']:
            print 'Author: '+reduce(lambda x,y:x+','+y,book['author'])
        print 'Average Score: '+book['rating']['average']
        print 'Price: '+book['price']
        print '\n'
        print book['author_intro']
        print '\n'

def query_books_by_word(word,limit):
    search_url = douban+'/v2/book/search'
    query = {}
    query['q'] = word
    query['count'] = limit
    query['start'] = 0

    r = requests.get(search_url,params=query)
    data = r.json()
    books = data['books']
    results = filter(lambda x:float(x['rating']['average']) > score,books)
    results = sorted(results,key=lambda x:x['rating']['average'],reverse=True)
    print_books(results)

def query_book_by_id(book_id):
    search_url = douban + '/v2/book/' + book_id

    r = requests.get(search_url)
    data = r.json()

def print_comments(comments):
    for comment in comments:
        print comment['author']+'  '+comment['vote']+' Useful'
        print comment['content']
        print "\n"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    if '-h' in sys.argv:
        usage()
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-l",type=int,default=20,help='query limits')
    parser.add_argument("-q",type=str,help='query key word')
    parser.add_argument("-s",type=float,default=7,help='minimum score')
    parser.add_argument("-t",type=str,default='s',help='sript action')
    parser.add_argument("-i",type=str,help='book id')
    args = vars(parser.parse_args())

    word = args['q']
    limit = args['l']
    score = args['s']
    action = args['t']
    book_id = args['i']

    if action == 's':
        query_books_by_word(word,limit)
    elif action == 'c':
        comments = query_book_comments(book_id)
        print_comments(comments)
    else:
        usage()
