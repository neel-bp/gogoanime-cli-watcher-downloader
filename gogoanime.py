import requests
from bs4 import BeautifulSoup
import os
import sys
from openload import OpenLoad
import apikey
from greeter import greeter
import yaml

# for getting the filepath of executable/.py script depending on if it is frozen or not
if getattr(sys, 'frozen', False):
    filepath=os.path.dirname(sys.executable)
else:
    filepath=os.path.dirname(os.path.realpath(__file__))

#for fetching the series name and series link in form of dictionary
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

#for counting how much pages are there for a search query but it only shows all the page numbers that are visible from the current page so even if there are more pages it will only show like 5 which is the limit but this function is primarily used for checking if pages exist or not for a search query
def numberofpages(webpagedata):  
    try:
        soup=BeautifulSoup(webpagedata,'html.parser')
        pagination=soup.find('ul',attrs={'class':'pagination-list'})
        lis=pagination.find_all('li')
        return len(lis)
    except:
        return None

#for getting the sourcelist
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


def openloadfetch(fileid):
    ol = OpenLoad(apikey.userkey, apikey.passkey)


    file_id = fileid

    preparation_resp = ol.prepare_download(file_id)
    ticket = preparation_resp.get('ticket')

    # Sometimes no captcha is sent in openload.co API response.
    captcha_url = preparation_resp.get('captcha_url')

    if captcha_url:
        # Solve captcha.
        pass
    else:
        captcha_response = ''

    download_resp = ol.get_download_link(file_id, ticket, captcha_response)
    direct_download_url = download_resp.get('url')

    # Process download url.
    return direct_download_url   

#for getting the latest current episode of a series
def latestepisode(link):
    r=requests.get(link)
    soup=BeautifulSoup(r.text,'html.parser')
    latestepisodenumbera=soup.find('a',attrs={'class':'active'})
    return latestepisodenumbera['ep_end']

def bookmark(aniname, anilink):
    if os.path.exists(filepath+"\\"+"bookmarks.yaml") == False:
        bookmarks={}
        indexed={}
        bookmarks.update({aniname:anilink})
        indexed.update({aniname:latestepisode(anilink)})
        favs={'bookmarks':bookmarks, 'indexed':indexed}
        yaml.safe_dump(favs, open(filepath+'\\'+'bookmarks.yaml', 'w+'))
    elif os.path.exists(filepath+"\\"+'bookmarks.yaml'):
        bookmarkindexed=yaml.safe_load(open(filepath+"\\"+'bookmarks.yaml'))
        bookmarkindexed['bookmarks'][aniname]=anilink
        bookmarkindexed['indexed'][aniname]=latestepisode(anilink)
        yaml.safe_dump(bookmarkindexed, open(filepath+"\\"+'bookmarks.yaml', 'w+'))


clrscr()
greeter()
searchurl='https://www.gogoanime.tv/search.html?keyword='
titlelinks={}
while True:
    searchq = input('search: ')
    page = requests.get(searchurl+searchq)
    pagedata=page.text
    titlelinks=websoup(pagedata)
    if titlelinks == {}:
        print('\u001b[31;1m'+'nothing found with your search query'+'\u001b[0m')
    else:
        break

print()
#clrscr()
trig1=0
for titlelink in titlelinks.keys():
    trig1=trig1+1
    print('\u001b[33;1m'+str(trig1)+'.'+chr(26)+' '+'\u001b[34;1m'+titlelink+'\u001b[0m')

print()

if numberofpages(pagedata)==None:
    pagetitlelinks=titlelinks
#    series = input('choose series: ')
#    print(titlelinks[series])

else:
    pagepos=1
    pagetitlelinks = titlelinks

    while True:
       
        print('\u001b[33;1m'+'|Previous-page||Next-page|'+'\u001b[0m')
        print()
        
        pageno=input('if your series is on this page enter this: ')
        
        if pageno == 'next':
            trig2=0
            pagepos=pagepos+1
            r=requests.get(searchurl+searchq+'&page='+str(pagepos))
            pagetitlelinks=websoup(r.text)
            if pagetitlelinks == {}:
                print('\u001b[31;1m'+'this page does not exist'+'\u001b[0m')
                pagepos=pagepos-1
                r=requests.get(searchurl+searchq+'&page='+str(pagepos))
                pagetitlelinks=websoup(r.text)
            else:
                clrscr()
                greeter()
                for pagetitlelink in pagetitlelinks.keys():
                    trig2=trig2+1
                    print('\u001b[33;1m'+str(trig2)+'.'+chr(26)+' '+'\u001b[34;1m'+pagetitlelink+'\u001b[0m')
                print()
            
        elif pageno == "prev":
            
            pagepos=pagepos-1
            trig3=0
            if pagepos==0:
                print('\u001b[31;1m'+'this page does not exist'+'\u001b[0m')
                pagepos=1
                r=requests.get(searchurl+searchq+'&page='+str(pagepos))
                pagetitlelinks=websoup(r.text)
            else:
                
                r=requests.get(searchurl+searchq+'&page='+str(pagepos))
                pagetitlelinks=websoup(r.text)
                clrscr()
                greeter()
                for pagetitlelink in pagetitlelinks.keys():
                    trig3=trig3+1
                    print('\u001b[33;1m'+str(trig3)+'.'+chr(26)+' '+'\u001b[34;1m'+pagetitlelink+'\u001b[0m')
                print()
            
        elif pageno == "this":
            break
        
        else:
            print('\u001b[31;1m'+'unexpected input please try again'+'\u001b[0m')
    
    
while True:
    try:
        series = int(input('choose series: '))
        #print(pagetitlelinks[series])
        #print(list(pagetitlelinks.values())[series-1])
        #link to the series fetched using number instead of full name
        serieslink=list(pagetitlelinks.values())[series-1]
        seriesname=list(pagetitlelinks.keys())[series-1]
        break
    except:
        print('\u001b[31;1m'+"Can't you even count?? try again"+'\u001b[0m')

print()
print('\u001b[33;1m'+'Latest episode in this anime is: '+'\u001b[34;1m'+latestepisode(serieslink)+'\u001b[0m')
print()
bookmarkyn = input('Do you want to bookmark this series? (y or n): ')
print()
if bookmarkyn == 'y':
    bookmark(seriesname, serieslink)
else:
    pass

repeater=-1
while True:
    repeater=repeater+1
    while True:

        try:
            #fetching the name of the series in the format which is used in url so that it can be used in fetching the url of the episode
            if repeater < 1:
                episodenumber=input('enter episode number: ')
            else:
                episodenumber=input('enter next episode number: ')
            animename=serieslink.split('/')[len(serieslink.split('/'))-1]

            ## getting the link to the episode of the series selected and parsing its html

            episoderequest=requests.get('https://gogoanime.tv/'+animename+'-episode-'+str(episodenumber))
            tempsoup=BeautifulSoup(episoderequest.text,'html.parser')

            # fetching link to vidstream where download link to direct video is.

            downloadanime=tempsoup.find('div',attrs={'class':'download-anime'})
            downloadlinkpagea=downloadanime.find('a')
            downloadlinkpage=downloadlinkpagea['href']
            break
        except:
            print('\u001b[31;1m'+'Sorry this episode does not exist'+'\u001b[0m')


    # fetching the direct links

    directrequest=requests.get(downloadlinkpage)
    sourcedictionary=downloadsoup2(directrequest.text)

    clrscr()
    greeter()
    trig4=0
    for sourcename in sourcedictionary.keys():
        trig4=trig4+1
        if '\n' in sourcename:
            sourcename2=sourcename.replace(' ','')
            print('\u001b[33;1m'+str(trig4)+'.'+chr(26)+' '+'\u001b[34;1m'+sourcename2.replace('\n','')+'\u001b[0m')
        else:
            print('\u001b[33;1m'+str(trig4)+'.'+chr(26)+' '+'\u001b[34;1m'+sourcename.replace('Download','')+'\u001b[0m')
    print()

    while True:
        try:
            sourcechoice = int(input('choose source: '))
            qqq=list(sourcedictionary.keys())[sourcechoice-1]
            break
        except:
            print('\u001b[31;1m'+'Invalid Input please try again, (enter the number displayed beside the source you want to select)'+'\u001b[0m')

    if '\n' in list(sourcedictionary.keys())[sourcechoice-1]:
        playlink=list(sourcedictionary.values())[sourcechoice-1].replace(' ','%20')
        os.system('vlc \"'+playlink+'\"')
    elif 'Openload' in list(sourcedictionary.keys())[sourcechoice-1]:
        openloadlink=list(sourcedictionary.values())[sourcechoice-1]
        openloaddirect=openloadfetch(openloadlink.split('/')[len(openloadlink.split('/'))-1])
        opendirectnospace=openloaddirect.replace(' ','%20')
        os.system('vlc \"'+opendirectnospace+'\"')