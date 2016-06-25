#!/usr/bin/python
import sys
import argparse
import requests

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
        if book['author']:
            print 'Author: '+reduce(lambda x,y:x+','+y,book['author'])
        print 'Average Score: '+book['rating']['average']
        print 'Price: '+book['price']
        print '\n'
        print 'Author_intro: '+book['author_intro']
        print '\n'

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

    args = vars(parser.parse_args())

    word = args['q']
    limit = args['l']
    score = args['s']
    douban = 'https://api.douban.com'
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
