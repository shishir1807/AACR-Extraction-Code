import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing.pool import ThreadPool as Pool

start_time = time.time()

def listid():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--log-level=3') 
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get("https://www.abstractsonline.com/pp8/#!/10828")
    time.sleep(15)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find_all('div', {'class': 'span4'})
    second_div = all_divs[1]
    link = second_div.find_all('a')
    driver.quit()
    l=[]
    for links in link:
        href = links.get('href')
        s = "https://www.abstractsonline.com/pp8/" + href
        l.append(s)
    df = pd.DataFrame(l, columns=['links'])
    df['session_type'] = df['links'].str.extract(r'@sessiontype=([^/]+)')
    header = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Backpack': 'b8d8930d-56a3-4757-a76c-23bee8fe9ef8',
    'Caller': 'PP8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'www.abstractsonline.com',
    'Origin': 'https://www.abstractsonline.com',
    'Referer': 'https://www.abstractsonline.com/pp8/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'Access-Control-Allow-Headers': 'x-test-header, Origin, X-Requested-With, Content-Type, Accept, Authorization, withcredentials, Prefer, Caller, Backpack, MfaToken',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, PATCH, PUT, OPTIONS',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-cache, no-store',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'upgrade-insecure-requests',
    'Content-Type': 'application/json; charset=utf-8',
    'Date': 'Wed, 07 Feb 2024 05:30:39 GMT',
    'Expires': '-1',
    'Pragma': 'no-cache',
    'Server': ''}
    l = []
    url = 'https://www.abstractsonline.com/oe3/Program/10828/Search/New/session'
    for i in df['session_type']:
        payload = json.loads(f'{{"Phrase":"@sessiontype={i}"}}')
        response = requests.post(url,headers=header,data=json.dumps(payload))
        soup = BeautifulSoup(response.text, "html.parser")
        search_id = json.loads(soup.text)['SearchId']
        l.append(int(search_id))
    print("list id acquired")
    return l

def session_title():
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Backpack': 'b8d8930d-56a3-4757-a76c-23bee8fe9ef8',
    'Connection': 'keep-alive',
    'Host': 'www.abstractsonline.com',
    'Referer': 'https://www.abstractsonline.com/pp8/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'X-Requested-With': 'XMLHttpRequest'}
    final_df = pd.DataFrame()
    l=listid()
    for i in l:
        url = f'https://www.abstractsonline.com/oe3/Program/10828/Search/{i}/Results?page=1&pagesize=10000&sort=1&order=asc'
        response = requests.get(url, headers=headers)
        json_data = response.json()
        results_data = []
        for result in json_data['Results']:
            row = { 'Session_Title': result['Body'],
                'Location': result['Foot'],
                'Date&Time': result['Head'],
                'STitle_Id': result['Id'] }
            results_data.append(row)
        search_data = {'Session Type': json_data['Search']['Phrase'],'SType_Id': json_data['Search']['SearchId']}
        results_df = pd.DataFrame(results_data)
        search_df = pd.DataFrame([search_data] * len(results_df), index=results_df.index)
        final_df = pd.concat([final_df, pd.concat([results_df, search_df], axis=1)])

    final_df['abs_link'] = 'https://www.abstractsonline.com/oe3/Program/10828/Session/' + final_df['STitle_Id'].astype(str) + '/presentations'
    final_df.to_csv("session_title.csv", index=False)
    print("session title downloaded")
    return final_df

def abstract_title():
    df1 = session_title()
    df_combined = pd.DataFrame()
    headers= {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Backpack": "b8d8930d-56a3-4757-a76c-23bee8fe9ef8",
        "Caller": "PP8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "www.abstractsonline.com",
        "Referer": "https://www.abstractsonline.com/pp8/",
        "Sec-Ch-Ua": 'Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "X-Requested-With": "XMLHttpRequest" }

    pool = Pool(8)
     
    def fetch_data(url):
        response = requests.get(url, headers=headers)
        json_data = response.json()
        df = pd.DataFrame([
            {
                "Abs_Id": entry.get("Id"),
                "End_date": entry.get("End"),
                "Start_date": entry.get("Start"),
                "Session_Title": entry.get("SessionTitle"),
                "STitle_Id": entry.get("SessionId"),
                "Abstract_title": entry.get("SearchResultBody"),
                "AuthorBlock": entry.get("AuthorBlock"),
            }
            for entry in json_data if "Id" in entry
        ])
        print(f"Data fetched from: {url}")
        return df
    
    results = pool.map(fetch_data, df1['abs_link'])
    pool.close()
    pool.join()
    df_combined = pd.concat(results, ignore_index=True)
    df_combined.to_csv("abstract_title.csv", index=False)

abstract_title()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")







