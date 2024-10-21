import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

url = "https://saras.cbse.gov.in/SARAS/AffiliatedList/ListOfSchdirReport"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


data = []
table = soup.find('table')

for row in table.find_all('tr')[1:]:  
    cols = row.find_all('td')
    if cols:
        aff_no = cols[1].text.strip()
        state_district = cols[2].text.strip().split(',')
        state = state_district[0].strip()
        if len(state_district) > 1:
            district = state_district[1].strip()
        else:
            district = ''
        status = cols[3].text.strip()
        school_name = cols[4].text.strip()
        head_name = cols[5].text.strip()
        data.append([aff_no, state, district, status, school_name, head_name])

df = pd.DataFrame(data, columns=['Aff No', 'State', 'District', 'Status', 'School Name', 'Head Name'])
# 1
rk = df[df['Head Name'] == 'RAJESH KUMAR']['School Name'].values
print("School(s) whose head/principal name is RAJESH KUMAR:", rk)
# 2
total_schools = df.shape[0]
print("Total no. of schools", total_schools)
#  3
client = MongoClient('mongodb://localhost:27017/')  
db = client['school_database']
collection = db['schools']

# 4
collection.insert_many(df.to_dict('records'))

# 5
senior_secondary_count = collection.count_documents({'Status': 'Senior Secondary'})
secondary_count = collection.count_documents({'Status': 'Secondary'})

print("Count of Senior Secondary level schools:", senior_secondary_count)
print("Count of Secondary level schools:", secondary_count)

# 6
amity_principal = collection.find_one({'School Name': 'AMITY INTERNATIONAL SCHOOL'}, {'Head Name': 1})
if amity_principal:
    print("Principal of AMITY INTERNATIONAL SCHOOL:", amity_principal['Head Name'])
else:
    print("Principal of AMITY INTERNATIONAL SCHOOL: Not Found")
    
