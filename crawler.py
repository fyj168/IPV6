#!/usr/bin/env python3
"""
山西IPTV源信息爬取（仅用于学习研究）
请遵守相关法律法规，合法使用
"""

import requests
import re
import json
import time
from datetime import datetime
from pathlib import Path
import hashlib

class ShanxiIPTVCrawler:
    def __init__(self):
        self.base_url = "https://my9.ltd/tvsh/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://my9.ltd/',
        }
        self.session = requests.Session()
        
    def fetch_page(self):
        """获取网页内容"""
        try:
            response = self.session.get(
                self.base_url, 
                headers=self.headers,
                timeout=15
            )
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def extract_shanxi_sources(self, html):
        """提取山西相关的源（示例）"""
        sources = []
        
        # 示例解析逻辑 - 实际需要根据网站结构调整
        if html:
            # 查找m3u8链接
            m3u_pattern = r'https?://[^\s<>"\']+\.m3u8?'
            m3u_links = re.findall(m3u_pattern, html, re.IGNORECASE)
            
            # 查找组播地址
            udp_pattern = r'udp://(@)?\d{1,3}(\.\d{1,3}){3}:\d+'
            udp_links = re.findall(udp_pattern, html, re.IGNORECASE)
            
            # 合并结果
            all_links = m3u_links + [udp[0] if isinstance(udp, tuple) else udp for udp in udp_links]
            
            # 过滤山西相关的内容（根据关键词）
            shanxi_keywords = ['山西', 'shanxi', 'sx', '太原', '晋']
            for link in all_links:
                if any(keyword.lower() in link.lower() for keyword in shanxi_keywords):
                    sources.append(link)
        
        return sources
    
    def save_to_json(self, data, filename="shanxi_iptv.json"):
        """保存为JSON文件"""
        output = {
            "update_time": datetime.now().isoformat(),
            "source_url": self.base_url,
            "count": len(data),
            "channels": data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(data)} 个源到 {filename}")
        return filename
    
    def create_m3u_playlist(self, sources, filename="shanxi_iptv.m3u"):
        """生成M3U播放列表"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write(f"# Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Source: {self.base_url}\n")
            f.write("# 仅供学习研究使用\n\n")
            
            for i, source in enumerate(sources, 1):
                f.write(f"#EXTINF:-1,频道{i}\n")
                f.write(f"{source}\n\n")
        
        print(f"已生成M3U播放列表: {filename}")
        return filename

def main():
    """主函数"""
    print("开始爬取山西IPTV源信息...")
    print("=" * 50)
    
    crawler = ShanxiIPTVCrawler()
    
    # 获取网页内容
    html = crawler.fetch_page()
    if not html:
        print("获取网页内容失败")
        return
    
    # 提取源
    sources = crawler.extract_shanxi_sources(html)
    
    if sources:
        print(f"找到 {len(sources)} 个山西相关的源")
        
        # 保存为JSON
        json_file = crawler.save_to_json(sources)
        
        # 生成M3U
        m3u_file = crawler.create_m3u_playlist(sources)
        
        # 输出摘要信息
        print("\n摘要信息:")
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"数据文件: {json_file}, {m3u_file}")
    else:
        print("未找到山西相关的源")

if __name__ == "__main__":
    main()