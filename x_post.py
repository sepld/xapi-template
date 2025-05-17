#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import json
from datetime import datetime
import base64
import hmac
import hashlib
import time
import urllib.parse
import uuid
import logging
from requests_oauthlib import OAuth1

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class XAPIClient:
    """X API 客户端类，用于发布帖子"""
    
    def __init__(self, oauth_config=None, config_file=None):
        """初始化X API客户端
        
        Args:
            oauth_config: OAuth配置信息字典
            config_file: 配置文件路径
        """
        # OAuth配置信息
        self.oauth_config = oauth_config or {}
        
        # 如果没有提供oauth_config，尝试从配置文件加载
        if not self.oauth_config and config_file:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.oauth_config = config
            except Exception as e:
                logger.error(f"无法从配置文件加载: {str(e)}")
        
        # 如果仍然没有oauth_config，尝试从环境变量加载
        if not self.oauth_config:
            try:
                self.oauth_config = {
                    "consumer_key": os.environ.get("X_CONSUMER_KEY"),
                    "consumer_secret": os.environ.get("X_CONSUMER_SECRET"),
                    "access_token": os.environ.get("X_ACCESS_TOKEN"),
                    "access_token_secret": os.environ.get("X_ACCESS_TOKEN_SECRET")
                }
            except Exception as e:
                logger.error(f"从环境变量加载配置失败: {str(e)}")
            
        # 验证必要的配置信息
        required_keys = ["consumer_key", "consumer_secret", "access_token", "access_token_secret"]
        missing_keys = [key for key in required_keys if not self.oauth_config.get(key)]
        
        if missing_keys:
            raise ValueError(f"缺少必要的OAuth配置: {', '.join(missing_keys)}")
            
        self.base_url = "https://api.twitter.com/2"  # X API仍使用twitter.com域名
        
        # 创建OAuth1会话
        self.oauth = OAuth1(
            client_key=self.oauth_config["consumer_key"],
            client_secret=self.oauth_config["consumer_secret"],
            resource_owner_key=self.oauth_config["access_token"],
            resource_owner_secret=self.oauth_config["access_token_secret"],
            signature_method='HMAC-SHA1'
        )
    
    def create_post(self, text):
        """创建新帖子
        
        Args:
            text: 帖子内容文本
            
        Returns:
            响应JSON数据
        """
        endpoint = f"{self.base_url}/tweets"
        payload = {"text": text}
        
        logger.info(f"发送请求到: {endpoint}")
        logger.info(f"请求载荷: {payload}")
        
        # 使用OAuth1会话发送请求
        response = requests.post(
            endpoint,
            auth=self.oauth,
            json=payload
        )
        
        if response.status_code not in (200, 201):
            logger.error(f"发布失败! 状态码: {response.status_code}")
            logger.error(f"响应: {response.text}")
            logger.error(f"请求头: {response.request.headers}")
            return None
            
        return response.json()


def main():
    """主函数"""
    import argparse 
    text = "用 cursor 写的自动发推代码，提前写好，定时发送，太爽了。 \n\n 这个就是自动发的。 \n 代码：https://github.com/sepld/xapi-template"
    
    parser = argparse.ArgumentParser(description="使用X API发布帖子")
    parser.add_argument("--text", "-t", default=text, help="帖子内容")
    parser.add_argument("--config", "-c", help="配置文件路径，默认为config.json", default="config.json")
    parser.add_argument("--debug", "-d", action="store_true", help="启用调试模式")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    try:
        client = XAPIClient(config_file=args.config)
        result = client.create_post(args.text)
        
        if result:
            post_id = result.get("data", {}).get("id")
            logger.info(f"帖子发布成功! ID: {post_id}")
            print(f"帖子发布成功! ID: {post_id}")
            print(f"帖子链接: https://x.com/i/web/status/{post_id}")
    
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()