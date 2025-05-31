#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import os

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取配置
    oauth_config = {
        "consumer_key": os.getenv("X_CONSUMER_KEY"),
        "consumer_secret": os.getenv("X_CONSUMER_SECRET"),
        "access_token": os.getenv("X_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET")
    }
    
    # 验证配置
    required_keys = ["consumer_key", "consumer_secret", "access_token", "access_token_secret"]
    missing_keys = [key for key in required_keys if not oauth_config.get(key)]
    
    if missing_keys:
        logger.error(f"缺少必要的OAuth配置: {', '.join(missing_keys)}")
        return
    
    # 创建OAuth1认证对象
    oauth = OAuth1(
        client_key=oauth_config["consumer_key"],
        client_secret=oauth_config["consumer_secret"],
        resource_owner_key=oauth_config["access_token"],
        resource_owner_secret=oauth_config["access_token_secret"],
        signature_method='HMAC-SHA1'
    )
    
    # 测试用户信息接口（这是一个只读接口，适合测试认证）
    endpoint = "https://api.twitter.com/2/users/me"
    
    logger.info(f"测试认证: {endpoint}")
    
    try:
        response = requests.get(endpoint, auth=oauth)
        
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应: {response.text}")
        logger.debug(f"请求头: {response.request.headers}")
        
        if response.status_code == 200:
            logger.info("认证成功!")
        else:
            logger.error("认证失败!")
    
    except Exception as e:
        logger.error(f"请求发生错误: {str(e)}")

if __name__ == "__main__":
    main() 