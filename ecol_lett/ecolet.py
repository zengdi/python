import requests
from lxml import etree
import time
from openpyxl import Workbook

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {"User-Agent" : user_agent}

html = requests.get('https://onlinelibrary.wiley.com/loi/14610248', headers=headers).content
selector = etree.HTML(html)
volumes = selector.xpath('//ul[@class="rlist loi__list"]//li/a/@href')
print(volumes)
issues = []
base_http = 'https://onlinelibrary.wiley.com'
for volume in volumes:
    http_volume = base_http + volume
    html_volume = requests.get(http_volume,headers=headers).content
    volume_selector = etree.HTML(html_volume)
    issue_temp = volume_selector.xpath('//ul[@class="rlist loi__issues"]//h4/a/@href')
    issues.extend(issue_temp)
    break
    time.sleep(1)


headings = []
for issue in issues:
    http_issue = base_http + issue
    print(http_issue)
    html_issue = requests.get(http_issue,headers=headers).content
    issue_selector = etree.HTML(html_issue)
    heading = issue_selector.xpath('//div[@class="issue-item"]/a/h2/text()')
    #print(heading)
    headings.extend(heading)
    break
    time.sleep(1)

wb = Workbook()
ws = wb.active

i = 1
for heading in headings:
   ws.cell(i,1).value = heading
   i+=1
wb.save('/home/zengdi/Desktop/test.xlsx')


