import os
import requests
import re
from tqdm.rich import tqdm

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

