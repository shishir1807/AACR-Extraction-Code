from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
import os

def fetch_data(i):
    print(i)
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "ASPSESSIONIDCWQDSRAD=POPDMJECAPEACGFMADOHBGGB",
    "Referer": "https://www.postersessiononline.eu/pr/aula_poster_ash.asp?congreso=79937160",
    "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}
    url = f"https://www.postersessiononline.eu/pr/aula_poster_ash.asp?congreso=79937160&direccion_posters=Seleccion&pagina_posters={i}&ordenacion=n_poster&cod_congreso_integracion=&pst_clave=&buscar=&swAcceso=&swAccesoAdmin=&cod_congreso_aula_rel=&busqueda_rapida=&tipo=autor&texto=&texto2=&grupo2_aula=&grupo=&texto_ident=&zoom_menos=&grupo3=&mencion="
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    poster_info = soup.find_all("script", string=re.compile("preposter"))
    data = []
    for p in poster_info:
        id = p.text
        poster_id = re.findall(r'preposter[^"\']*\.png', id)
        poster_number = re.findall(r'url_pdf=([^&]+)', id)
        for i, n in zip(poster_id, poster_number):
            data.append({'poster_id': i, 'poster_number': n})
    return data

def poster_csv():  
    data_list = []
    with ThreadPool(processes=8) as pool:  
        results = pool.map(fetch_data, range(207))
        pool.close()
        pool.join()
    for result in results:
        data_list.extend(result)
    df = pd.DataFrame(data_list)
    df['poster_number'] = df['poster_number'].str.extract(r'_(\d+)_')
    df['poster_number'] = df['poster_number'].astype(int)
    df['poster_id'] = df['poster_id'].str.extract(r'_([0-9_]+\.png)$')
    df.drop_duplicates(inplace=True)
    df['link'] = "https://www.postersessiononline.eu/173580348_eu/congresos/ASH2023/aula/preposter_" + df["poster_id"]
    df.to_csv("check.csv",index=False)
    return df

def download_poster():
    df = poster_csv()
    def download_images(row, folder_path):
        try:
            response = requests.get(row.link)
            img = Image.open(BytesIO(response.content))

            filename = os.path.join(folder_path, f"{row.poster_number}.png")
            img.save(filename)
            print(f"Image for poster {row.poster_number} downloaded and saved as {filename}.")
        except Exception as e:
            print(f"Error downloading image for poster {row.poster_number}: {e}")

    def download_images_parallel(row):
        download_images(row, "Downloaded Posters")

    pool = ThreadPool(processes=8)
    pool.map(download_images_parallel, df.itertuples(index=False))
    pool.close()
    pool.join()


download_poster()