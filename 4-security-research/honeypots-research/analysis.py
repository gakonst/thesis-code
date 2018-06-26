import pandas as pd
import sys
import os
import json


DATA_DIR = './data'

### Load Data
honeypots_file = 'identified_honeypot_names'


with open(sys.argv[1]) as f:
    data = json.loads(f.read())

with open(honeypots_file) as f:
    honeypot_names = [i.strip() for i in f.readlines()]

data = pd.DataFrame.from_dict(data)
data = data.drop('checked')

data.to_csv('data_asdf.csv')


### Identify known honeypots

hp = data.T
honeypots = hp.loc[hp['contract_name'].isin(honeypot_names)]

honeypots = honeypots.sort_values('contract_name')

### Save source codes for all known honeypots, grouped by contract name
# for addr in honeypots.T:
#     name = honeypots.T[addr]['contract_name']
#     src = honeypots.T[addr]['contract_source_code']
#     directory = os.path.join(DATA_DIR, name)
#     if not os.path.exists(directory):
#         os.mkdir(directory)
#     with open(os.path.join(directory, addr+'.sol'), 'w') as f:
#             f.write(src)
#             print('Wrote', name)


### 
dates = pd.to_datetime(data.T['verified_data']).sort_values()
print(dates)



