import requests
import pandas as pd
from lxml import etree

wikiData = requests.get('https://en.wikipedia.org/wiki/Demographics_of_Toronto_neighbourhoods')
html = etree.HTML(wikiData.text)
neighbourHoodTable = html.xpath('//table[@class="wikitable sortable"]/tbody/tr')

tableHeaders = [col.text.strip() for col in neighbourHoodTable[0].xpath('th')]
neighbourHood = pd.DataFrame(columns=tableHeaders[0:12])

for row in neighbourHoodTable[2:]:
    columns = row.xpath("td")
    rowData = [columns[0].xpath("a")[0].text]
    rowData.extend([columns[1].text.strip()])
    rowData.append([columns[2].text.strip()])
    rowData.extend([col.text.strip() for col in columns[3:12]])

    neighbourHood = neighbourHood.append(pd.DataFrame([rowData], columns=tableHeaders[0:12]), ignore_index = True)

neighbourHood.to_csv('toronto_neighbourhood_data.csv')

