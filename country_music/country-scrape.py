# web scraping learning attempt

from lxml import html
import requests
import string
import datetime
from collections import Counter

# specify dates for data collection, duration in weeks
target_date = datetime.date.today()
duration = 5*52;
time_step = datetime.timedelta(weeks=1)

def datestring(target_date):
    # turns dates into formatted strings for urls
    return str(target_date.year)+'_'+str(target_date.month)+'_'+str(target_date.day)

page = requests.get('http://www.billboard.com/charts/country-songs')#'http://www.billboard.com/charts/country-airplay')
tree = html.fromstring(page.content)

song_names = tree.xpath('//h2[@class="chart-row__song"]/text()')
artists = tree.xpath('//a[@class="chart-row__artist"]/text()')

# edit artist names
artists = [x.strip() for x in artists]
artists = [x.replace("&","and") for x in artists]
artists = [x.translate(string.maketrans("",""), string.punctuation) for x in artists]
artists = [" ".join(x.split()) for x in artists]
artists = [x.replace(" ","-") for x in artists]

# edit song names
song_names = [x.strip() for x in song_names]
song_names = [x.replace("&","and") for x in song_names]
song_names = [x.translate(string.maketrans("",""), string.punctuation) for x in song_names]
song_names = [" ".join(x.split()) for x in song_names]
song_names = [x.replace(" ","-") for x in song_names]

#lyrics = [[]*len(song_names)]
#print lyrics
print (len(song_names))
raw_lyrics = [];
errors = 0;

for i in xrange(len(song_names)):
    print (song_names[i],' by ',artists[i])
    #url = 'http://www.azlyrics.com/lyrics/'+artists[1]+'/'+song_names[1]+'.html'
    url = 'http://www.metrolyrics.com/'+song_names[i].lower()+'-lyrics-'+artists[i].lower()+'.html'
    print(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    lyrics = tree.xpath('//p[@class="verse"]/text()')
    lyrics = [x.translate(string.maketrans("",""), string.punctuation) for x in lyrics]
    lyrics = [x.replace("\n","") for x in lyrics]
    lyrics = [x.lower() for x in lyrics]
    #print 'Attempt ',i,': ',lyrics
    for line in lyrics:
        words = line.split()
        raw_lyrics = raw_lyrics+words
    #print 'Raw lyrics: ',raw_lyrics
    if not lyrics:
        print ("-----------------------Error finding lyrics for song ",i)
        errors += 1


#print 'end result',raw_lyrics
print ('-------------------------------'*4)
print ('Unprocessed Songs: ',errors)

counts = Counter(raw_lyrics)
#print counts

print ("-"*500)

text_file = open("output.txt",'w')
for word in raw_lyrics:
    text_file.write(" %s" %word)
text_file.close


