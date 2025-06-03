import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///disaster_management.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 高德地图配置
    AMAP_KEY = 'be7f08115df6d0a758f1421bb9b0d14e'  # 你的Web端Key
    AMAP_SECURITY_CODE = 'e264a7a60ee6de4a3fe05dada426da95'  # 你的安全密钥
    
    # 生产环境域名配置
    SERVER_NAME = os.environ.get('SERVER_NAME')  # 在生产环境设置为 xxx.com 