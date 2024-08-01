import pandas as pd
import json
import pytz

# Your Google Sheet URL
url = 'https://docs.google.com/spreadsheets/d/1MUk8bcxuXxcrgz4IR4HbqouWXa3fFfKb38k2SM2AdQ8/edit?resourcekey#gid=1041016962'

# Make sure to replace with the correct export format and sheet ID
csv_export_url = url.replace('/edit?resourcekey#gid=', '/export?format=csv&gid=')

df = pd.read_csv(csv_export_url, on_bad_lines='skip')  # Skip problematic lines

df = df.dropna(how='all').drop(columns = "Zeitstempel")
df = df[df['BewilligungFuerAbruf'].str.lower() == 'ja']

new_column_names = {'Zu welchen Fachbereichen lässt sich die Veranstaltung zuordnen': 'event_topics',
                    'Titel der Veranstaltung': 'event_title',
                    'Beschreibung der Veranstaltung': 'event_description',
                    'URL zur Beschreibung im Internet': 'event_link',
                    'Für welche Zielgruppen ist die Veranstaltung relevant': 'event_target_audience',
                    'Beginn (Datum) der Veranstaltung': 'event_date_start',
                    'Ende (Datum) der Veranstaltung': 'event_date_end',
                    'Ende (Uhrzeit) der Veranstaltung': 'event_end',
                    'Beginn (Uhrzeit) der Veranstaltung': 'event_start',
                    'Kostenlose Teilnahme möglich?': 'event_has_fees',
                    'Ist die Veranstaltung Online?': 'event_is_online',
                    'Kann die Veranstaltung durch eine Schulklasse gebucht werden?': 'event_school_bookable',
                   'Name des Veranstalters': 'organization_name'}

df.rename(columns=new_column_names, inplace=True)

replacement_mapping_target_audience = {
    'Klein- Vorschulkinder: Elementarstufe': 10,
    'Schulkinder: Primarstufe': 20,
    'Jugendliche: Sekundarstufe I': 30,
    'Jugendliche: Berufsschulen / PTS': 40,
    'Jugendliche: Sekundarstufe II': 50,
    'Erwachsene': 60,
    'Familien': 70
}

replacement_mapping_event_topics = {
    'Digitalisierung / Künstliche Intelligenz / IT / Technik': 100,
    'Kunst / Kultur': 200,
    'Sprachen / Literatur': 300,
    'Medizin / Gesundheit': 400,
    'Geschichte / Demokratie / Gesellschaft': 500,
    'Wirtschaft / Recht': 600,
    'Naturwissenschaft / Klima / Umwelt': 700,
    'Mathematik / Zahlen / Daten': 800
}

def replace_values(lst, repdict):
    return [repdict.get(item, item) for item in lst]

df['event_topics'] = df['event_topics'].str.split(',').apply(lambda x: [item.strip() for item in x])
df['event_target_audience'] = df['event_target_audience'].str.split(',').apply(lambda x: [item.strip() for item in x])
df['event_topics'] = df['event_topics'].apply(lambda x: [replacement_mapping_event_topics.get(item,item) for item in x])
df['event_target_audience'] = df['event_target_audience'].apply(lambda x: [replacement_mapping_target_audience.get(item,item) for item in x])


replace_values = {'Ja': True, 'Nein': False}
df[['event_has_fees', 'event_is_online', 'event_school_bookable']] = df[['event_has_fees', 'event_is_online', 'event_school_bookable']].replace(replace_values)

df['event_start'] = pd.to_datetime(df['event_date_start'] + ' ' + df['event_start'], format='%d.%m.%Y %H:%M:%S')
df['event_end'] = pd.to_datetime(df['event_date_end'] + ' ' + df['event_end'], format='%d.%m.%Y %H:%M:%S')

cet_timezone = pytz.timezone('CET')
df['event_end'] = df['event_end'].dt.tz_localize('UTC').dt.tz_convert(cet_timezone).dt.strftime('%Y-%m-%dT%H:%M:%S%z')
df['event_start'] = df['event_start'].dt.tz_localize('UTC').dt.tz_convert(cet_timezone).dt.strftime('%Y-%m-%dT%H:%M:%S%z')


#df['event_location_name'] = "1"
#df['event_address_street'] = "1"
#df['event_address_city'] = "1"
#df['event_address_zip'] = "1"
df['event_address_state'] = "Salzburg"

#df['event_contact_name'] = "1"
#df['event_contact_org'] = "1"
#df['event_contact_email'] = "1"
#df['event_contact_phone'] = "1"

#df['location'] = [1]
#df['program_name'] = "1"
#df['event_format'] = "1"
df['event_classification'] = "scheduled"

df = df[['event_title', 'event_description', 'event_link',
       'event_target_audience', 'event_topics', 'event_start', 'event_end',
       'event_classification', 'event_has_fees', 'event_is_online', 'organization_name', 
       'event_school_bookable','event_address_state']]

df_json = {"events":[]}

for i in range(len(df)):
    df_json["events"].append(df.iloc[i].to_dict())

    
with open('output.json', 'w', encoding='utf-16') as f:
    json.dump(df_json, f, indent=3)
