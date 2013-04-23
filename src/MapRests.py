'''
This is a script to
1) Get a page with a table of Local Restaurant Week participating restaurants from the restaurants page at http://localrestaurantweek.com/restaurants.html
2) Extract the names and addresses of participating restaurants
3) Generate a csv file suitable for upload to http://batchgeo.com 

The result is a map of restaurants participating in the Western New York Local Restaurant Week
Example result from 2013: http://tinyurl.com/LRW2013


Example usage:
python -i MapRests.py
> dump_csv(process_table(get_soup("http://localrestaurantweek.com/restaurants.html")),"./maprest.csv")



@author: jonathanbona
'''

import urllib2
import csv
from bs4 import BeautifulSoup

    
def get_soup(url):
    """Gets a page from url and returns the beautifulsoup for it"""
    opener = urllib2.build_opener()
    request = urllib2.Request(url);
    request.add_header('User-Agent','Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1');
    data = opener.open(request).read(); 
    return BeautifulSoup(data);

def rest_row(r):
    """Given a row from the restaurants table, return a dict for that restaurant in case this row contains one"""
    # restaurant rows in the table have <a> with no style; 
    # neighborhood headers have styled <a>s; 
    # X the table header has no <a> --NOT ANY LONGER, NOW IT DOES have links for sorting. 
    #    the fix for this in process_table cuts out first row
    a = r.find('a',attrs={'style' : None}) 
    if not a: return None
    tds =  r.find_all('td')


    # sometimes - e.g. on 4/21 for Pizza Plant - there's no address -- use blank address & fix manually
    st = tds[0].text.split('\t')[1].lstrip().strip() if len(tds[0].text.split('\t')) > 1 else ''
    
    return {'street' : st,
            'city' : tds[1].text.strip(),
            'cuisine' : tds[2].text.strip(),
            'name' : a.text.strip(),
            'link' : a['href'].split('&')[0]}


def process_table(soup):
    """Given the beautifulsoup for the restaurants page, returns a list of dicts, one per restaurant, with key info"""
    rests = []
    rows = soup.find('table',attrs={"id" : "rest_list"}).find_all('tr')
    for r in rows[1:len(rows)]:
        rdict = rest_row(r)
        if rdict:
            rests.append(rdict)
    return rests


def dump_csv(rdl, fname='maprest.csv'):
    """Given a restaurant dict list and a filename, write a batchgeo csv file with one row per restaurant"""
    # write a csv file for batchgeo
    with open(fname, 'wb') as csvfile:
        restwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # write the header
        restwriter.writerow(['Address', 'City', 'State','Zipcode','Name','Phone Number','Group','URL','Email']);
        # write the results
        for res in rdl:
            restwriter.writerow([res['street'].encode('utf8'),res['city'].encode('utf8'),'NY', '',res['name'].encode('utf8'),'','','http://localrestaurantweek.com/'+res['link'].encode('utf8'),'']);

    
if __name__ == '__main__':
    pass


