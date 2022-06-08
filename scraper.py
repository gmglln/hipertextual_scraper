import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://hipertextual.com/'
XPATH_LINK_TO_ARTICLE = '//h2[@class="entry-title"]/a/@href'
XPATH_TITLE = '//h1[@class="entry-title entry-title--with-subtitle"]/text()'
XPATH_SUMMARY = '//div[@class="newspack-post-subtitle"]/text()'

def parse_notice(link, today):
  try:
    response = requests.get(link)
    if response.status_code == 200:
      notice = response.content.decode('utf-8')
      parsed = html.fromstring(notice)
      try:
        title = parsed.xpath(XPATH_TITLE)[0]
        title = title.replace('\"', '')
        summary = parsed.xpath(XPATH_SUMMARY)[0]
      except IndexError:
        return

      with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n\n')
        f.write(summary)
        f.write('\n\n')
    else:
      raise ValueError(response.status_code)
  except ValueError as e:
    print(e)

def parse_home():
  try:
    response = requests.get(HOME_URL)
    if response.status_code == 200:
      home = response.content.decode('utf-8')
      parsed = html.fromstring(home)
      links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
      today = datetime.date.today().strftime('%d-%m-%Y')
      if not os.path.isdir(today):
        os.mkdir(today)
      for link in links_to_notices:
        parse_notice(link, today)
        print('info exra')
    else:
      raise ValueError(response.status_code)
  except ValueError as e:
    print(e)

parse_home()