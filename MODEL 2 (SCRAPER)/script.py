# IMPORTING LIBRARIES
import warnings
warnings.filterwarnings("ignore")
import random
import re
#import PyPDF2 as pdf
import os
import requests
import pandas as pd
import time
import urllib
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from flask import Flask, request, render_template
import pandas as pd
# using time module
from tqdm import trange
from requests_html import HTML
from requests_html import HTMLSession
import winsound

# creating folders to store data
if not os.path.exists('output/not found):
    os.makedirs('output/not found')
if not os.path.exists('output/striked off'):
    os.makedirs('output/striked off')
if not os.path.exists('output/Scraped data'):
    os.makedirs('output/Scraped data')
    
useragents = "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
# ts stores the time in seconds
ts = time.time()
phone1 = '(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
phone2 = '(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})'
# print the current timestamp
print(ts)

def get_link(name):
    try:
        links = list(search(name+' zaubacorp',num=1,stop=1, pause=2)) #request 1
        for link in links:
            if 'zaubacorp' in link:
                return link
        return 'n'
    except Exception as e:
        return str(e)

def get_page_data(link):
    try:
        request = requests.get(link,headers={"User-Agent": useragents}) #request 2
        soup = BeautifulSoup(request.text,'lxml')
        request.close()
        time.sleep(2)
        
        data = []
        table = soup.find('table', class_='table table-striped')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            
        table_body = table.find('thead')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        data=dict(data)
        return data
    except Exception as e:
        return str(e)

def get_address(link):
    try:
        request = requests.get(link,headers={"User-Agent": useragents})   #request 3
        soup = BeautifulSoup(request.text,'lxml')
        request.close()
        time.sleep(2)

        #div = soup.find('div', class_='col-lg-6 col-md-6 col-sm-12 col-xs-12')
        #print(div)

        div_body = soup.find('p', text='Address: ')

        rows = div_body.find_next('p').text

        return rows
    except Exception as e:
        return float('NaN')

def get_email(link):
    try:
        request = requests.get(link,headers={"User-Agent": useragents} )  #request 4
        soup = BeautifulSoup(request.text,'lxml')
        request.close()
        time.sleep(2)

        div_body = soup.find('b', text=' Email ID: ')
        email = div_body.next_sibling
        if '-' in email: return float('NaN')
        return email
    except Exception as e:
        return float('NaN')

def get_urls(tag):
    try:
        return list(search(tag,num=5,stop=5, pause=2)) # request 5
    except Exception as e:
        return e

def get_phaddress(link):
    try:
        
        request = requests.get(link,timeout=5)    # request 10
        soup = BeautifulSoup(request.text,'lxml')
        request.close()

        #div = soup.find('div', class_='col-lg-6 col-md-6 col-sm-12 col-xs-12')
        #print(div)

        div_body = soup.find(['p','label','a','span','h1','h2','h3','h4','div'], text=re.compile(phone2+'|'+phone1))

        rows = div_body.text

        return rows
    except Exception as e:
        return e

def get_ph_no(name):
    ans={
        'links':[],
        'data':[]
      }
    l=[]
    print('\nScraping ph no for company: ',name,'-------')
    search_res = scrape_google(name+' phone number')
    try:
        if '429 Client Error' in str(search_res) or 'HTTP Error 429' in str(search_res):
            return 'IP BLOCKED'
    except Exception as e:
        print(e)
        pass
    for res in search_res:
        phaddr = get_phaddress(res)
        if '429 Client Error' in str(phaddr) or 'HTTP Error 429' in str(phaddr):
            return 'IP BLOCKED'
        l.append(phaddr)
        time.sleep(5)
    ans['links']=search_res
    ans['data']=l
    print(l,'\n\n')
    return ans

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    time.sleep(3)
    return links

def beep_sound():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 0.5 second
    for i in range(3):
        winsound.Beep(frequency, duration)
        time.sleep(0.5)

app=Flask(__name__)
xx = ['lollytest']

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="/scrape" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''

@app.route("/scrape", methods=['GET', 'POST'])
def scrape():
    df_name=None
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        
        data_xls = pd.read_excel(f)
        df_name = f.filename
        names = data_xls.iloc[:,1]

    # DRIVER SCRAPER CODE
    not_found=[] # List to store names that donot have any proper search results
    attrs = []   # Column names of dataset
    strike_off={
    'names':[]
    }
    data = {
        'name':[],
        'data':[],
        'link':[]
    }
    c=0
    last_req = time.time()
    phno={
    'name':[],
    'contacts':[],
    'link':[]
    }
    for name_index in trange(200, desc = 'SCRAPING PROGRESS'):
        name = names[name_index]
        if c==9:
            c=0
            print('Sleeping for 5 mins')
            time.sleep( 200 )

        ###################### PH NO EXTRACTION ###################
        '''k=0
        no = get_ph_no(name)
        if no=='IP BLOCKED':
            print('XXXXXXXXXXXXXXXXXXXXXXXXX------------ IP ADDRESS BLOCKED :( ---------------XXXXXXXXXXXXXXXXXXX')
            print('XXXXXXXXXXXXXXXXXXXXXXXXX------------ TRY AFTER 24 hrs or use a VPN ---------------XXXXXXXXXXX')
            break
        for i in range(len(no['links'])):
            if k==0:
                phno['name'].append(name)
                k=1
            else:phno['name'].append(float('Nan'))
            try:
                phno['contacts'].append(re.search(phone2+'|'+phone1,no['data'][i])[0])

            except:
                phno['contacts'].append(float('Nan'))
            phno['link'].append(no['links'][i])'''

        link = get_link(name)
        data['link'].append(link)
        if link=='n':
            not_found.append(name)
            continue
        elif '429 Client Error' in str(link) or 'HTTP Error 429' in str(link):
            print('XXXXXXXXXXXXXXXXXXXXXXXXX------------ IP ADDRESS BLOCKED :( ---------------XXXXXXXXXXXXXXXXXXXx')
            print('XXXXXXXXXXXXXXXXXXXXXXXXX------------ TRY AFTER 24 hrs or use a VPN ---------------XXXXXXXXXXX')
            break
        try:
            details = get_page_data(link)
            status = details['Company Status']
            if 'strik' in status.lower():
                strike_off['names'].append(details['Company Name'])
            else:
                data['name'].append(name)
                data['data'].append(details)
                for keyl in details.keys():
                    if keyl not in attrs:
                        attrs.append(keyl)
        except:
            not_found.append(name)
        c+=1
        now = time.time()
        delay = last_req + random.randint(2,11) - now
        last_req = now
        if delay >= 0:
            time.sleep(delay)
    
    print("Not found entries:",len(not_found))

    # FORMATTING THE DATA
    real_data = {}            #making the skeleton for data storage
    for i in attrs:
        if i not in ['RoC','Registration Number','Company Category','Company Sub Category','Class of Company','Age of Company','Number of Members','CIN','Foreign Company Registration Number']:
            real_data[i]=[]
    
    real_data['Address']=[]
    real_data['Email']=[]

    # PROCESSING SCRAPE DATA
    email_not_found = []

    for i in trange(len(data['data']), desc='PROCESSING DATA'):
        tab = data['data'][i]

        for attr in attrs:
            if attr in ['RoC','Registration Number','Company Category','Company Sub Category','Class of Company','Age of Company','Number of Members','CIN','Foreign Company Registration Number']:
                continue
            try:
                real_data[attr].append(tab[attr])
            except:
                real_data[attr].append(float('NaN'))

        link = data['link'][i]
        try:
            email_adr = get_email(link)
            if '429 Client Error' in str(email_adr) or 'HTTP Error 429' in str(email_adr):
                print('IP BLOCKED')
                email_adr = 'IP BLOCKED'
            else:
                real_data['Email'].append(email_adr)
            if pd.isnull(email_adr):
                email_not_found.append(list(real_data['Company Name'])[i])     #emailexc
        except Exception as e:
            real_data['Email'].append(float('NaN'))

        try:
            real_data['Address'].append(get_address(link))
        except:
            real_data['Address'].append(float('NaN'))

    beep_sound()
    # EXPORT AS EXCEL
    '''final_data = pd.DataFrame(phno)
    final_data.to_excel('output/contact_info_{}.xlsx'.format(df_name))'''
    real_data = pd.DataFrame.from_dict(real_data, orient='index').transpose()
    pd.DataFrame.from_dict({'Names':email_not_found}).to_excel('output/not found/not_found_email_{}.xlsx'.format(df_name))
    pd.DataFrame.from_dict({'Names':not_found}).to_excel('output/not found/not_found_other_info_{}.xlsx'.format(df_name))
    pd.DataFrame(strike_off).to_excel('output/striked off/striked_off_{}.xlsx'.format(df_name))
    print('Details not found for:\n')
    real_data.to_excel('output/Scraped data/email_other_info_{}.xlsx'.format(df_name))

    return render_template("out.html",p="data scraped succesfully, {} not found out of {}".format(len(not_found),len(real_data['Email'])))

if __name__ == "__main__":
    app.run()
