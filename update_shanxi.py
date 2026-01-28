#!/usr/bin/env python3
import requests
import re
from datetime import datetime
import sys

def main():
    print("开始获取山西组播源...")
    url = "https://my9.ltd/tvsh/"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            print("成功获取页面内容")
            
            # 查找m3u链接
            m3u_links = re.findall(r'href="([^"]+\.m3u[^"]*)"', response.text, re.IGNORECASE)
            txt_links = re.findall(r'href="([^"]+\.txt[^"]*)"', response.text, re.IGNORECASE)
            all_links = m3u_links + txt_links
            
            print(f"找到 {len(all_links)} 个链接")
            
            # 过滤山西相关链接
            shanxi_links = []
            keywords = ['shanxi', '山西', 'sx']
            for link in all_links:
                if any(keyword in link.lower() for keyword in keywords):
                    shanxi_links.append(link)
            
            if not shanxi_links and all_links:
                print("未找到山西链接，使用前3个链接")
                shanxi_links = all_links[:3]
            
            # 生成M3U内容
            content = [
                "#EXTM3U",
                f"# 山西组播源",
                f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# 来源: {url}",
                ""
            ]
            
            # 处理链接
            for i, link in enumerate(shanxi_links[:3]):
                try:
                    # 构建完整URL
                    if link.startswith('http'):
                        full_url = link
                    elif link.startswith('/'):
                        full_url = f"https://my9.ltd{link}"
                    else:
                        full_url = f"{url}{link}"
                    
                    print(f"下载链接 {i+1}: {full_url}")
                    r2 = requests.get(full_url, headers=headers, timeout=15)
                    
                    if r2.status_code == 200:
                        for line in r2.text.split('\n'):
                            line = line.strip()
                            if line and not line.startswith('#EXTM3U'):
                                content.append(line)
                        content.append("")
                        print(f"链接 {i+1} 处理成功")
                except Exception as e:
                    print(f"链接 {i+1} 处理失败: {e}")
            
            # 保存文件
            with open('shanxi-multicast.m3u', 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            
            print("更新完成")
            return True
        else:
            print(f"获取页面失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"程序出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
