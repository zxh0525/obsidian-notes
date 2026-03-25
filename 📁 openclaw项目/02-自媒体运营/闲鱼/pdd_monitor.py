#!/usr/bin/env python3
"""
拼多多爆款监控脚本
功能：监控拼多多商品数据，选出有利润的爆款
"""

import requests
import json
import time
from datetime import datetime

# 拼多多搜索接口（非官方，仅供学习）
PDD_SEARCH_URL = "https://mobile.yangkeduo.com/proxy/api/search/queryV4"

def search_goods(keyword, page=1):
    """搜索商品"""
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0",
        "Referer": "https://mobile.yangkeduo.com/"
    }
    
    data = {
        "keyword": keyword,
        "page": page,
        "page_size": 20,
        "sort_type": 1,  # 综合排序
    }
    
    try:
        response = requests.post(PDD_SEARCH_URL, json=data, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def analyze_profit(goods):
    """分析利润空间"""
    # 简单估算：售价 * 0.7 - 成本 = 利润
    # 实际需要根据具体商品计算
    return goods

def main():
    keywords = ["家居", "数码", "百货", "女装"]
    
    print(f"=== 拼多多爆款监控 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    
    all_goods = []
    
    for keyword in keywords:
        print(f"搜索关键词: {keyword}")
        result = search_goods(keyword)
        
        if result and "items" in result:
            goods_list = result["items"]
            for item in goods_list:
                goods = {
                    "keyword": keyword,
                    "title": item.get("goodsName", ""),
                    "price": item.get("price", 0) / 100,  # 分转元
                    "sales": item.get("sales", 0),
                    "tags": item.get("tags", []),
                }
                all_goods.append(goods)
        
        time.sleep(1)  # 避免请求过快
    
    # 按销量排序
    all_goods.sort(key=lambda x: x["sales"], reverse=True)
    
    print(f"\n=== 销量前20 ===")
    for i, g in enumerate(all_goods[:20], 1):
        print(f"{i}. {g['title'][:30]}...")
        print(f"   价格: ¥{g['price']:.2f} | 销量: {g['sales']}")
    
    # 保存到文件
    output_file = f"/home/xxh/文档/xxhnote/📁 项目笔记/拼多多爆款/{datetime.now().strftime('%Y-%m-%d')}.json"
    print(f"\n数据已保存到: {output_file}")

if __name__ == "__main__":
    main()
