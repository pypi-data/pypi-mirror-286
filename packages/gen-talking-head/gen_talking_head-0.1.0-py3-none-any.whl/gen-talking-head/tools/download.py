""" 自动下载底模

    底模管理文档：
"""
import os
import zipfile
from tqdm import tqdm
import os.path
import uuid
import requests
from qiniu import Auth, put_file

RESULTS_CACHE = {}
OSS_ACCESS_KEY = '91WmLWTfrv_vGm4v6vF2gHn0I5c37SzVWU2HS4BN'
OSS_SECRET_KEY = '6IYN7C37_DD5xGiFloPTbBprJ1SQsuGnejabav4N'


# 这个类封装了与对象存储服务（OSS）交互的功能，如上传和下载文件。
# 它使用了七牛云的 Auth 和 put_file 方法进行身份验证和文件上传。
class DHVideoOSS(object):

    def __init__(self):
        self.auth = Auth(OSS_ACCESS_KEY, OSS_SECRET_KEY)
        self.bucket = 'glsp'
        self.domain = 'https://glsp-img.unipus.cn/'
        self.file_dir = 'sd_webui_server'

    def upload(self, src_path):
        postfix = os.path.basename(src_path).split('.')[-1]
        file_name = str(uuid.uuid4()) + '.' + postfix
        key = os.path.join(self.file_dir, file_name)  # 文件地址
        token = self.auth.upload_token(self.bucket, key, 3600)
        ret, info = put_file(token, key, src_path, version='v2')
        return info, self.domain + key

    def download(self, url):
        # 识别文件类型
        postfix = os.path.basename(url).split('.')[-1]
        # 创建临时目录来存储下载的zip文件
        tar_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
        os.makedirs(tar_dir, exist_ok=True)
        # 为下载的文件创建唯一的文件名
        tar_name = str(uuid.uuid4()) + '.' + postfix
        tar_path = os.path.join(tar_dir, tar_name)
        print(f"Starting download model files from {url}...")
        # 下载文件
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        with open(tar_path, 'wb') as file, tqdm(
                total=total_size, unit='iB', unit_scale=True, unit_divisor=1024, desc="Downloading") as bar:
            for data in response.iter_content(block_size):
                bar.update(len(data))
                file.write(data)
        print("Download completed.")

        # 解压到项目根目录下的weights文件夹
        extract_dir = os.path.join(os.path.dirname(tar_dir), 'weights')
        os.makedirs(extract_dir, exist_ok=True)
        print("Starting extraction...")
        with zipfile.ZipFile(tar_path, 'r') as zip_ref:
            total_files = len(zip_ref.namelist())
            with tqdm(total=total_files, desc="Extracting", unit='files') as bar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, extract_dir)
                    bar.update(1)
        print("Extraction completed.")

        # 删除下载的zip文件
        os.remove(tar_path)
        print(f"Removed temporary file {tar_path}.")
        return extract_dir


def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    weights_url = 'https://glsp-img.unipus.cn/ai/weights.zip'
    oss = DHVideoOSS()
    extract_dir = oss.download(weights_url)
    print(extract_dir)
