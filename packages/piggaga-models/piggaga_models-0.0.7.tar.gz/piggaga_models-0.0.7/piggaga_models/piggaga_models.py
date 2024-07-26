import os
import requests
import re
from tqdm.rich import tqdm
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading

def download_google_images(query, num_images):
    # 将搜索关键词编码为URL安全格式
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    # 发送GET请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # 使用正则表达式找到所有图片URL
    image_urls = re.findall(r'(?<=["\'])https://[^"\']*?(?:\.jpg|\.jpeg|\.png|\.gif)(?=["\'])', response.text)

    # 创建以查询名字命名的文件夹
    folder_path = f'img/{query}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 下载图片
    for i, image_url in enumerate(tqdm(image_urls[:num_images], desc='Downloading Images')):
        try:
            # 发送请求下载图片
            img_response = requests.get(image_url, headers=headers)
            
            # 检查图片是否模糊处理
            if 'image/jpeg' in img_response.headers.get('Content-Type', ''):
                # 构建 Referer 头部，以解除模糊处理
                headers['Referer'] = image_url
                img_response = requests.get(image_url, headers=headers)
            
            img_data = img_response.content
            image_path = f'{folder_path}/image_{i}.jpg'
            with open(image_path, 'wb') as f:
                f.write(img_data)
                print(f'Downloaded {image_path}')

            # 删除第一张图片 image_0.jpg
            if i == 0:
                os.remove(image_path)
                print(f'Deleted {image_path}')

        except Exception as e:
            print(f'Error downloading image: {e}')


def print_all_models():
    print("---- All Models Name ----")
    print('download_google_images')
    print('download_website_images')
    print(f'\n----Models Instructions ----')
    print('download_google_images(query, num_images)')
    print('download_website_images(url, save_folder)')


def _download_website_images(img_url, folder_path, headers, img_idx, downloaded_urls):
    try:
        if img_url in downloaded_urls:
            print(f'圖片已經下載過: {img_url}')
            return
        
        if img_url.startswith('data:image'):
            base64_str = img_url.split(',')[1]
            img_data = base64.b64decode(base64_str)
            img_name = f'image_{img_idx}.png'
        else:
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()
            content_type = img_response.headers.get('Content-Type', '')
            if 'image/png' in content_type:
                img_ext = '.png'
            elif 'image/jpeg' in content_type:
                img_ext = '.jpg'
            else:
                img_ext = '.png'
            img_name = os.path.basename(img_url).replace('/', '_').replace('?', '_') + img_ext
            img_data = img_response.content
        
        img_path = os.path.join(folder_path, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        
        downloaded_urls.add(img_url)
        print(f'下載圖片: {img_name}')
    except Exception as e:
        print(f'無法下載圖片 {img_url}: {e}')

def fetch_images(url, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img')
        total_images = len(img_tags)

        downloaded_urls = set()
        with tqdm(total=total_images, desc="下載圖片") as pbar:
            threads = []
            for idx, img_tag in enumerate(img_tags):
                img_src = img_tag.get('src')
                if not img_src:
                    pbar.update(1)
                    continue
                
                img_url = urljoin(url, img_src)
                thread = threading.Thread(target=_download_website_images, args=(img_url, folder_path, headers, idx, downloaded_urls))
                thread.start()
                threads.append(thread)
                
                if len(threads) >= 10:
                    for thread in threads:
                        thread.join()
                    threads = []
                
                pbar.update(1)
            
            for thread in threads:
                thread.join()
        
        print(f'總共下載圖片數量: {len(downloaded_urls)}')
    except Exception as e:
        print(f'無法處理網站 {url}: {e}')