import requests
from bs4 import BeautifulSoup
import os



def websoup(webpagedata):   
    soup=BeautifulSoup(webpagedata,'html.parser')
    resultuls=soup.find_all('p',attrs={'class':'name'})
    
    results=[]
    for resultul in resultuls:
        namechild=resultul.find('a')
        results.append(namechild)

    titles=[]
    links=[]
    
    for result in results:
        titles.append(result['title'])
        links.append('https://gogoanime.tv'+result['href'])

    title_link_dictionary=dict(zip(titles, links))

    return title_link_dictionary

def numberofpages(webpagedata):  
    try:
        soup=BeautifulSoup(webpagedata,'html.parser')
        pagination=soup.find('ul',attrs={'class':'pagination-list'})
        lis=pagination.find_all('li')
        return len(lis)
    except:
        return None

def downloadsoup2(webpagedata):
    directsoup=BeautifulSoup(webpagedata,'html.parser')
    directdivs=directsoup.find_all('div',attrs={'class':'dowload'})
    directlinksa=[]
    for directdiv in directdivs:
        directlinksa.append(directdiv.find('a'))

    a=[]
    b=[]
    for x in directlinksa:
        a.append(x.text)
        b.append(x['href'])

    
    a_b_dictionary=dict(zip(a,b))
    return a_b_dictionary

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



searchurl='https://www.gogoanime.tv/search.html?keyword='
titlelinks={}
while True:
    searchq = input('search: ')
    page = requests.get(searchurl+searchq)
    pagedata=page.text
    titlelinks=websoup(pagedata)
    if titlelinks == {}:
        print('nothing found with your search query')
    else:
        break

print()
clrscr()
for titlelink in titlelinks.keys():
    print(titlelink)

print()

if numberofpages(pagedata)==None:
    pagetitlelinks=titlelinks
#    series = input('choose series: ')
#    print(titlelinks[series])

else:
    pagepos=1
    pagetitlelinks = titlelinks

    while True:
       
        print('|Previous-page||Next-page|')
        print()
        
        pageno=input('if your series is on this page enter this: ')
        
        if pageno == 'next':
            clrscr()
            pagepos=pagepos+1
            r=requests.get(searchurl+searchq+'&page='+str(pagepos))
            pagetitlelinks=websoup(r.text)
            
            for pagetitlelink in pagetitlelinks.keys():
                print(pagetitlelink)
            print()
            
        elif pageno == "prev":
            clrscr()
            pagepos=pagepos-1
            r=requests.get(searchurl+searchq+'&page='+str(pagepos))
            pagetitlelinks=websoup(r.text)
            
            for pagetitlelink in pagetitlelinks.keys():
                print(pagetitlelink)
            print()
            
        elif pageno == "this":
            break
        
        else:
            print('unexpected input please try again')
    
    
series = int(input('choose series: '))
#print(pagetitlelinks[series])
#print(list(pagetitlelinks.values())[series-1])

episodenumber=input('enter episode number: ')

#link to the series fetched using number instead of full name
serieslink=list(pagetitlelinks.values())[series-1]
#fetching the name of the series in the format which is used in url so that it can be used in fetching the url of the episode
animename=serieslink.split('/')[len(serieslink.split('/'))-1]

## getting the link to the episode of the series selected and parsing its html

episoderequest=requests.get('https://gogoanime.tv/'+animename+'-episode-'+str(episodenumber))
tempsoup=BeautifulSoup(episoderequest.text,'html.parser')

# fetching link to vidstream where download link to direct video is.

downloadanime=tempsoup.find('div',attrs={'class':'download-anime'})
downloadlinkpagea=downloadanime.find('a')
downloadlinkpage=downloadlinkpagea['href']

# fetching the direct links

directrequest=requests.get(downloadlinkpage)
sourcedictionary=downloadsoup2(directrequest.text)

print()
for sourcename in sourcedictionary.keys():
    if '\n' in sourcename:
        sourcename2=sourcename.replace(' ','')
        print(sourcename2.replace('\n',''))
    else:
        print(sourcename)






        
