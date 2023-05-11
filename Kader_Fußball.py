#access website

import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
import os

#Land auswählen
länder={'Deutschland':40, 'England':189, 'Frankreich':50, 'Österreich':127, 'Spanien':157, 'Italien':75}
print('')
print('Herzlich willkommen zur Kader-Ausgabe!\n')
lst=[]
for land in länder:
    lst.append(land)
count = 0
for land in lst:
    print(str(count + 1) + ' ' + land)
    count += 1
print('')
inp=None
while True:
    inp=input('Wähle ein Land (Name oder Nummer): ')
    try:
        x = int(inp)
        inp = lst[x-1]
        break

    except:
        if inp.lower() not in (land.lower() for land in lst):
            print('Land nicht in Liste!\n')
            continue
        else:
            break
print('')

#auf Länderseite gehen
myurl='https://www.transfermarkt.de/wettbewerbe/national/wettbewerbe/'+str(länder[inp.title()])
#myurl='https://www.transfermarkt.de/wettbewerbe/national/wettbewerbe/189'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

#request
req=urllib.request.Request(url=myurl, headers=headers)
with urllib.request.urlopen(req) as response:
    page_html=response.read().decode()

#eingrenzen auf Ligen
soup=BeautifulSoup(page_html, 'lxml')
table_total=soup.find('div', class_="responsive-table")
lst_ligen_unsauber=table_total.find_all('a', title=True)
lst_ligen=[]
for liga in lst_ligen_unsauber:
    if 'Zum Wettbewerbsforum' in str(liga) or 'Seite' in str(liga):
        continue
    else:
        lst_ligen.append(liga)
lst_ligen=lst_ligen[:5]

#Liganame und Nummer in Dictionary
liga_dict={}
lst_liga=[]
for liga in lst_ligen:
    liganame=liga.text
    lst_liga.append(liganame)
    link=liga['href']
    linkparts=link.split('/')
    liganummer=linkparts[-1]
    liga_dict[liganame]=liganummer

#Ligen drucken
count = 0
for liga in lst_liga:
    print(str(count + 1) + ' ' + liga)
    count += 1
print('')

#Liga auswählen
inp=None
while True:
    inp=input('Wähle eine Liga (Name oder Nummer): ')
    try:
        x = int(inp)
        inp = lst_liga[x-1]
        break
    except:
        if inp.lower() not in (liga.lower() for liga in liga_dict):
            print('Liga nicht in Liste!\n')
            continue
        else:
            for liga in liga_dict:
                if inp.lower() == liga.lower():
                    inp = liga
            break
print('')

#Gehe zu Ligaseite
ligaurl='https://www.transfermarkt.de/bundesliga/startseite/wettbewerb/'+str(liga_dict[inp])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
#Request
req=urllib.request.Request(url=ligaurl, headers=headers)
with urllib.request.urlopen(req) as response:
    page_html=response.read().decode()

#Mannschaftsliste und -dictionary
soup=BeautifulSoup(page_html, 'lxml')
ligatabelle=soup.find('div', class_='responsive-table')
teamliste_unsauber=ligatabelle.find_all('a', title=True)
teamliste=[]
teamdict={}
for team in teamliste_unsauber:
    if 'img' not in str(team) and 'startseite' in str(team):
        #team=team.text
        teamliste.append(team.text)
        link=team['href']
        linksliced=link.split('/')
        teamnr=linksliced[4]
        teamdict[team.text.lower()]=teamnr

while inp.capitalize() !='N':#for repetition after execution
    count = 0
    for team in teamliste:
        if count < 9:
            print(' ' + str(count + 1) + ' ' + team)
        else:
            print(str(count + 1) + ' ' + team)
        count += 1
    print('')

#Verein auswählen
    inp=None
    while True:
        inp=input('Wähle einen Verein (Name oder Nummer): ')
        try:
            x = int(inp)
            if x < 1:
                print('Verein nicht in Liste!\n')
                continue
            else:
                inp = teamliste[x-1].lower()
                break
        except:
            if inp.lower() not in (team.lower() for team in teamliste):
                print('Verein nicht in Liste!\n')
                continue
            else:
                inp = inp.lower()
                break
    print('')

#Gehe zu Vereinseite
    teamurl='https://www.transfermarkt.de/fc-bayern-munchen/startseite/verein/'+str(teamdict[inp])
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
    #Request
    req=urllib.request.Request(url=teamurl, headers=headers)
    with urllib.request.urlopen(req) as response:
        page_html=response.read().decode()

    soup=BeautifulSoup(page_html, 'lxml')
    kadertabelle=soup.find('div', class_='responsive-table')
    kaderliste_unsauber=kadertabelle.find_all('a', title=True)
    spielerliste_unsauber=[]
    for spieler in kaderliste_unsauber:
        if 'verein' not in str(spieler) and '.' not in str(spieler):
            spielerliste_unsauber.append(spieler)
    spielerliste=[]

    #spieler hinzufügen
    for spieler in spielerliste_unsauber:
        if spieler.text not in spielerliste:
            spielerliste.append(spieler.text)
        else:
            continue

    #Trainer hinzufügen
    try:
        trainer=soup.find('a', id = '0')
        spielerliste.append(trainer.text)
    except:
        pass

    #Namen in Datei ausgeben
    for team in teamliste:
        if inp == team.lower():
            inp = team
        else:
            continue

    # Datei öffnen und reinschreiben
    path_name = os.getcwd()
    print(path_name)
    with open(os.path.join(path_name, 'Kader Fußball', f'Kader {inp}.txt'), 'w', encoding = 'ANSI') as file:
        file.write(inp + '\n')
        for spieler in spielerliste:
            namensliste=spieler.split(' ')
            if len(namensliste)==2:
                file.write(spieler + '\n')
                file.write(namensliste[1] + '\n')
            elif len(namensliste)==1:
                file.write(spieler + '\n')
            elif len(namensliste)>=3:
                file.write(spieler + '\n')
                file.write(namensliste[-1] + '\n')
                file.write(namensliste[-2]+' '+namensliste[-1] + '\n')

    print('Datei wurde erstellt!\n')
    inp=input('Noch ein Verein aus der Liga (J/N): ')
