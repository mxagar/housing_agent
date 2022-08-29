import pandas as pd
import json
import urllib
import requests as rq
import base64
import matplotlib.pyplot as plt
import datetime
import time

def get_oauth_token():
    '''
    Get OAuth bearer token.
    '''
    # Load key:secret obtained from Idealista and saved into a TXT file (local)
    key_file = open('key.txt')
    lines = key_file.readlines()
    key_str = lines[0].split(':')[0]
    secret_str = lines[0].split(':')[1][:-2]
    # Request token
    url = 'https://api.idealista.com/oauth/token'    
    apikey = key_str # put your key here (provided by Idealista)
    secret = secret_str  # put your key here (provided by Idealista)
    apikey_secret = apikey + ':' + secret
    auth = str(base64.b64encode(bytes(apikey_secret, 'utf-8')))[2:][:-1]
    headers = {'Authorization': 'Basic '+auth,'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    params = urllib.parse.urlencode({'grant_type': 'client_credentials'}) #,'scope':'read'
    content = rq.post(url, headers=headers, params=params)
    bearer_token = json.loads(content.text)['access_token']
    return bearer_token

def search_api(token, URL): 
    '''
    Idealista API request.
    '''
    headers = {'Content-Type': 'Content-Type: multipart/form-data;', 'Authorization': 'Bearer '+token}
    content = rq.post(url, headers=headers)
    result = json.loads(content.text)
    return result

def query(num_items):
    '''
    Quick and dirty custom query.
    Query parameters are hard-coded.
    Idealista API is queried with the parameters.
    '''
    # Housing Parameters
    country = 'es' # values: es, it, pt
    locale = 'es' # values: es, it, pt, en, ca
    language = 'es'
    operation = 'sale' # rent
    property_type = 'homes'
    order = 'priceDown'
    # Bidebieta: 43.32222093197415, -1.940486953608932
    # Lasarte: 43.27044123284123, -2.0200276593105064
    # Hernani: 43.266944705720235, -1.9751387613285116
    # Zarautz: 43.28563835253485, -2.167198244296092
    center = '43.32222093197415,-1.940486953608932'
    distance = '5000'
    sort = 'desc'
    flat = 'true'
    #elevator= 'true'

    # Search parameters
    max_items = '50'
    page_limit = int(num_items/int(max_items))
    df_tot = pd.DataFrame()

    # Search in a loop
    # Watch out: free tier: 100 req/month, 1 req/sec
    for page in range(1, page_limit):
        url = ('https://api.idealista.com/3.5/'+country+'/search?operation='+operation+
            '&maxItems='+max_items+
            '&order='+order+
            '&center='+center+
            '&distance='+distance+
            '&propertyType='+property_type+
            '&sort='+sort+ 
            '&flat='+flat+
#            '&elevator='+elevator+
            '&numPage=%s'+
            '&language='+language) %(page)  
        a = search_api(get_oauth_token(), url)
        df = pd.DataFrame.from_dict(a['elementList'])
        df_tot = pd.concat([df_tot,df])
        time.sleep(1.5)

    df_tot = df_tot.reset_index()
    df_tot['date'] = datetime.date.today()
    return df_tot

if __name__ == "__main__":

    # Custom query - quick and dirty for now: query defined in function
    num_items = 2500
    df = query(num_items)
    df.to_csv('./data/test.csv')
