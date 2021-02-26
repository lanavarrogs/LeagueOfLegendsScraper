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
        name = league_name +'_draft.csv'
        df.to_csv(name)
    except Exception as e:
        print(f"Error: {e}")

def get_info_champions(table_champions):
    data = []
    info = {}
    positions = ['Top','Mid','Jungle','Bot','Support'] 
    try:
        for tr in table_champions.find_all("tr"):
            tds = tr.find_all('td')
            if not tds :
                continue
            if not tds[0].text in positions:
                info['champion']= tds[0].text
            if not tds[1].text in positions:
                info['games'] = tds[1].text
            if not tds[2].text in positions:
                info['bans'] = tds[2].text
            if not tds[4].text in positions:
                info['picks'] = tds[4].text
            info['wins'] = tds[6].text
            info['losses'] = tds[7].text
            winrate = tds[7].text.replace('%')
            print(winrate)
            if info:
                data.append(info.copy())
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
    get_info_champions(tbl)
except Exception as e:
    print(f"Error {e}")


driver.close()
