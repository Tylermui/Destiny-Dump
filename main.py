# ---- Workspace setup instructions: ----
# pip install requests
# pip install beautifulsoup4
# pip install lxml

from bs4 import BeautifulSoup
import requests


# appends a file with links to every weapon on light.gg
def getWeaponLinks():
  f = open("weaponLinks.txt", "a")

  counter = 1
  while (counter <=  1154):
    print(counter)
    url = 'https://www.light.gg/db/category/1?page='+ str(counter)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    for link in soup.find_all('a'):
      if '/db/items/' in link.get('href') and 'compare' not in link.get('href'): 
        f.write('https://www.light.gg' + link.get('href') + '\n')

    counter += 1

  f.close()

  lines = open('weaponLinks.txt', 'r').readlines()
  lines_set = set(lines)
  out = open('weaponLinks.txt', 'a')
  for line in lines_set:
    out.write(line)
  lines.close()

  return


# appends a file with an array of dictionaries containing stats about each weapon on light.gg
def getWeaponStats():
  weaponLinksFile = open('weaponLinks.txt', 'r')
  links = weaponLinksFile.readlines()

  weaponStatsFile = open('weaponStats.txt', 'a')
  weaponStatsFile.write("[\n")

  tempDict = {}
  counter = 0

  for link in links:

    print(str(counter) + ' -----------------------------------------------------------------------------')
    counter += 1

    response = requests.get(link.strip())
    soup = BeautifulSoup(response.content, 'lxml')

    if soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[2].strip() == 'Weapon Ornament':
      continue

    tempDict['Name'] = soup.find_all('h2')[0].text.strip()
    tempDict['Rarity'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[0].strip()

    if len(soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')) == 4:
      tempDict['Class'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[1].strip()
      tempDict['Element'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[2].strip()
      tempDict['Type'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[3].strip()
    else:
      tempDict['Class'] = 'Any'
      tempDict['Element'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[1].strip()
      tempDict['Type'] = soup.find_all('span', class_="weapon-type")[0].text.strip().split('/')[2].strip()

    for linkTable in soup.find_all('table', class_="stat-visualizer"):
      for row in linkTable.find_all('tr'):
        tds = row.find_all('td')
        tempDict[tds[0].text.strip()] = tds[-1].text.strip()

    perksArray = []
    for img in soup.find_all("img", {"class": "mod"}):
      if 'Ornament' not in img.get('alt') and img.get('alt').isascii():
        perksArray.append(img.get('alt'))
    
    tempDict['Perks'] = perksArray
    perksArray = []

    print(str(tempDict))
    weaponStatsFile.write(str(tempDict) + ",\n")
    tempDict = {}
    
  weaponStatsFile.write("]")

  return

# getWeaponLinks()
getWeaponStats()