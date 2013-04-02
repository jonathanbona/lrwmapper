'''
Script to:
1) scrape the Western New York Local Restaurant Week page (http://localrestaurantweek.com/), and 
2) generate a csv file suitable for upload to batchgeo 

Example result from 2012: http://batchgeo.com/map/856e9cc67cdfa537cf0cdb953ba8443d

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
    # restaurant rows in the table have <a> with no style; neighborhood headers have styled <a>s; the table header has no <a>
    a = r.find('a',attrs={'style' : None}) 
    if not a: return None
    tds =  r.find_all('td')
    return {'street' : tds[0].text.split('\t')[1].lstrip().strip(), 
            'city' : tds[1].text.strip(),
            'cuisine' : tds[2].text.strip(),
            'name' : a.text.strip(),
            'link' : a['href']}

def process_table(soup):
    """Given the beautifulsoup for the restaurants page, returns a list of dicts, one per restaurant, with key info"""
    rests = []
    for r in soup.find('table',attrs={"id" : "rest_list"}).find_all('tr'):
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
            restwriter.writerow([res['street'],res['city'],'NY', '',res['name'],'','','http://localrestaurantweek.com/'+res['link'],'']);
    

#dump_csv(process_table(get_soup("http://localrestaurantweek.com/restaurants.cfm")),"./maprest.csv") # example usage
    
if __name__ == '__main__':
    pass


