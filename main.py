import pandas as pd
import json

# Example code to read a Google Sheets document into a Pandas DataFrame
url = 'https://docs.google.com/spreadsheets/d/1e0b0mybZrToEL6QYPj-_i7aKUBrP0eGHvOQozO_Wo7A/edit#gid=1080009798'
csv_export_url = url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(csv_export_url)

df_json = {"events":[]}

for i in range(len(df)):
    df_json["events"].append(df.iloc[i].to_dict())

with open('output.json', 'w') as f:
    json.dump(df_json, f, indent=3)
