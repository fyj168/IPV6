import requests
import re
from datetime import datetime
import os

def main():
    print('开始获取山西组播源...')
    source_url = "https://my9.ltd/tvsh/"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(source_url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            print('成功获取页面内容')
            
            m3u_links = re.findall(r'href="([^"]+\.m3u[^"]*)"', response.text)
            m3u_links += re.findall(r'href="([^"]+\.txt[^"]*)"', response.text)
            
            if m3u_links:
                print(f'找到 {len(m3u_links)} 个可能的m3u/txt链接')
                
                shanxi_links = []
                for link in m3u_links:
                    if any(keyword in link.lower() for keyword in ['sx', 'shanxi', '山西', 'tvsh']):
                        shanxi_links.append(link)
                
                if not shanxi_links:
                    print('未找到明确的山西链接，尝试获取所有链接...')
                    shanxi_links = m3u_links[:5]
                
                all_content = []
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                all_content.append('#EXTM3U')
                all_content.append('# 山西组播源')
                all_content.append(f'# 更新时间: {timestamp}')
                all_content.append(f'# 来源: {source_url}')
                all_content.append('')
                
                for i, link in enumerate(shanxi_links[:3]):
                    try:
                        if link.startswith('http'):
                            full_link = link
                        elif link.startswith('/'):
                            full_link = f"https://my9.ltd{link}"
                        else:
                            full_link = f"https://my9.ltd/tvsh/{link}"
                        
                        print(f'正在下载: {full_link}')
                        m3u_response = requests.get(full_link, headers=headers, timeout=30)
                        
                        if m3u_response.status_code == 200:
                            content = m3u_response.text
                            lines = content.split('\n')
                            for line in lines:
                                if line.strip() and not line.strip().startswith('#EXTM3U'):
                                    all_content.append(line)
                            all_content.append('')
                    except Exception as e:
                        print(f'处理链接时出错: {str(e)}')
                
                with open('shanxi-multicast.m3u', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_content))
                
                print('山西组播源已更新')
                
        else:
            print(f'获取页面失败: {response.status_code}')
            
    except Exception as e:
        print(f'执行过程中出错: {str(e)}')

if __name__ == "__main__":
    main()
