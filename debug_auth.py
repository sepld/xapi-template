#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import logging
from requests_oauthlib import OAuth1

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_file):
    """从配置文件加载OAuth配置"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"无法加载配置文件: {str(e)}")
        sys.exit(1)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python debug_auth.py config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    oauth_config = load_config(config_file)
    
    # 验证配置
    required_keys = ["consumer_key", "consumer_secret", "access_token", "access_token_secret"]
    missing_keys = [key for key in required_keys if not oauth_config.get(key)]
    
    if missing_keys:
        logger.error(f"缺少必要的OAuth配置: {', '.join(missing_keys)}")
        sys.exit(1)
    
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