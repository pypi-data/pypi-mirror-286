import os
from os.path import join
from dotenv import load_dotenv

class Config:
    def get(value: str):
        load_dotenv(join(os.path.abspath(os.curdir), '.env'))
        return os.getenv(value)
    
    def debug() -> bool:
        return os.getenv('XRAY_DEBUG', Config.get('XRAY_DEBUG')).lower().capitalize() == "True"
    
    def project_key():
        return os.getenv('PROJECT_KEY', Config.get('PROJECT_KEY'))
    
    def test_type():
        return os.getenv('TEST_TYPE', Config.get('TEST_TYPE'))
    
    def xray_api():
        return os.getenv('XRAY_API', Config.get('XRAY_API'))
    
    def xray_client_id():
        return os.getenv('XRAY_CLIENT_ID', Config.get('XRAY_CLIENT_ID'))
    
    def xray_client_secret():
        return os.getenv('XRAY_CLIENT_SECRET', Config.get('XRAY_CLIENT_SECRET'))
    
    def cucumber_path():
        return os.getenv('CUCUMBER_PATH', Config.get('CUCUMBER_PATH'))
    
# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#         sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#         import config
#     else:
#         from .config import Config