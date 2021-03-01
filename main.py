from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import pandas as pd

def get_info_draft(table_draft,league_name):
    data = []
    info = {}
    league_name = league_name.replace(" ","")
    try:
        for tr in table_draft.find_all("tr"):
            td = tr.find_all('td')
            if not td:
                continue
            info['patch'] = td[4].text
            if td[1].get('class'):
                info["winside"] = 'Blue'
            else:
                info["winside"] = 'Red'
            info['BB1'] = td[5].get('data-c1')
            info['RB1'] = td[6].get('data-c1')
            info['BB2'] = td[7].get('data-c1')
            info['RB2'] = td[8].get('data-c1')
            info['BB3'] = td[9].get('data-c1')
            info['RB3'] = td[10].get('data-c1')
            info['BP1'] = td[11].get('data-c1')
            info['RP1'] = td[12].get('data-c1')
            info['RP2'] = td[12].get('data-c2')
            info['BP2'] = td[13].get('data-c2')
            info['BP3'] = td[13].get('data-c2')
            info['RP3'] = td[14].get('data-c1')
            info['RB4'] = td[15].get('data-c1')
            info['BB4'] = td[16].get('data-c1')
            info['RB5'] = td[17].get('data-c1')
            info['BB5'] = td[18].get('data-c1')
            info['RP4'] = td[19].get('data-c1')
            info['BP4'] = td[20].get('data-c1')
            info['BP5'] = td[20].get('data-c2')
            info['RP5'] = td[21].get('data-c1')
            data.append(info.copy())
        df = pd.DataFrame(data)
        name ='./datasets/draft/'+league_name +'_draft.csv'
        df.to_csv(name)
    except Exception as e:
        print(f"Error: {e}")

def get_info_champions(table_champions,league_name):
    data = []
    info = {}
    positions = ['Top','Mid','Jungle','Bot','Support'] 
    try:
        for tr in table_champions.find_all("tr"):
            tds = tr.find_all("td")
            if not tds:
                continue
            if not tds[0].text in positions:
                info['champion'] = tds[0].text
            if not tds[1].text in positions:
                info['games'] = tds[1].text
            if not tds[2].text in positions:
                presence = tds[2].text.replace('%','')
                presence = float(presence)
                presence = presence/100
                info['prescence'] = presence
            if not tds[3].text in positions:
                info['bans'] = tds[3].text
            if not tds[4].text in positions:
                info['picks'] = tds[4].text
            if len(tds) >5:
                info['byteam'] = tds[5].text
                info['wins'] = tds[6].text
                info['losses'] = tds[7].text
                winrate = tds[8].text
                if winrate == '-':
                    info['winrate'] = None
                else:
                    info['winrate'] = winrate.replace('%','')
                if tds[9].text == '-':
                    info['kills'] = None
                else:
                    info['kills'] = float(tds[9].text)
                if tds[10].text == '-':
                    info['deaths'] =None
                else:    
                    info['deaths'] = float(tds[10].text)
                if tds[11].text == '-':
                    info['assists'] = None
                else:
                    info['assists'] = tds[11].text
                if tds[12].text == '-':
                    info['kda'] = None
                else:
                    info['kda'] = tds[12].text
                if tds[13].text == '-':
                    info['cs'] = None
                else:
                    info['cs'] = float(tds[13].text)
                if tds[14].text == '-':
                    info['cspm'] = None
                else:
                    info['cspm'] = float(tds[14].text)
                if tds[15].text == '-':
                    info['gold'] = None
                else:
                    gold = tds[15].text
                    info['gold'] = gold.replace('k','')
                if tds[16].text == '-':
                    info['gpm'] = None
                else:
                    info['gpm'] = float(tds[16].text)
                if tds[17].text == '-':
                    info['killpart'] = None
                else:
                    killpart = tds[17].text.replace('%','')
                    killpart = float(killpart)
                    killpart = killpart/100
                    info['killpart'] = killpart
                if tds[18].text == '-':
                    info['killshare'] = None
                else:
                    killshare = tds[18].text.replace('%','')
                    killshare = float(killshare)
                    killshare = killshare/100
                    info['killshare'] = killshare
                if tds[19].text == '-':
                    info['goldshare'] = None
                else:
                    goldshare = tds[19].text.replace('%','')
                    goldshare = float(goldshare)
                    goldshare = goldshare/100
                    info['goldshare'] = goldshare
            if info:
                data.append(info.copy())
        name = './datasets/champstats/'+league_name +'_champstats.csv'
        df = pd.DataFrame(data)
        df.to_csv(name)
    except Exception as e:
        print(f"Error: {e}")



driver=webdriver.Chrome("/usr/bin/chromedriver")
url = 'https://lol.gamepedia.com/League_of_Legends_Esports_Wiki'
driver.get(url)
links = driver.find_element_by_id('p-2021_Season-list')
link_list = links.text
leagues = link_list.split('\n')

try:
    boton = driver.find_element(By.PARTIAL_LINK_TEXT,leagues[2])
    boton.click()
    picks_bans_button = driver.find_element(By.PARTIAL_LINK_TEXT,'Picks & Bans')
    picks_bans_button.click()
    content = driver.page_source
    soup = BeautifulSoup(content,'lxml')
    tbl=soup.find('table',attrs={'id': 'pbh-table'})
    get_info_draft(tbl,leagues[2])
    champions_button = driver.find_element(By.PARTIAL_LINK_TEXT,'Champion Stats')
    champions_button.click()
    content = driver.page_source
    soup = BeautifulSoup(content,'lxml')
    tbl=soup.find('table',attrs={'class': 'wikitable'})
    get_info_champions(tbl,leagues[2])
except Exception as e:
    print(f"Error {e}")


driver.close()
