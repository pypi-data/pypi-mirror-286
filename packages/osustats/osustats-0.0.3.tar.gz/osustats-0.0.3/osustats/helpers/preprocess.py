import requests, json
import pandas as pd
import time

def df_preprocess_columns():
    return  ["match_id", "match_name", \
             "pick", "beatmap", "beatmap_id", \
             "player", "user_id", "team", \
             "score", "normalised_score", "accuracy", "mods"]


def process_raw_df(main_df):
    player_df = main_df[["user_id", "player", "team"]].dropna(how='all')
    beatmap_df = main_df[["beatmap_id", "mod", "beatmap"]].dropna(how='all')
    match_df = main_df[["mp_link", "ban_1", "ban_2", "ban_3", "ban_4"]].dropna(how='all')
    
    player_dict = {}
    for index, row in player_df.iterrows():
        player_dict[row["user_id"]] = {"player": row["player"], "team": row["team"]}

    combined_series = pd.concat([match_df[col].astype(str) for col in ["ban_1", "ban_2", "ban_3", "ban_4"]])
    ban_dict = combined_series.value_counts().to_dict()

    beatmap_dict = {}
    for index, row in beatmap_df.iterrows():
        if row["mod"] in ban_dict:
            ban_count = ban_dict[row["mod"]]
        else:
            ban_count = 0

        beatmap_dict[row["beatmap_id"]] = {"beatmap": row["beatmap"], "pick": row["mod"], "ban_count": ban_count}

    match_id_list = []
    for mp_link in match_df["mp_link"]:
        mp_link = mp_link.split("/")[-1]
        match_id_list.append(mp_link)

    return player_dict, beatmap_dict, match_id_list


def mod_process(mod_list, ez_mult, ht_mult):
    mod_str = ""
    mod_multiplier = 1

    mult_dict = {
                'RX':1,
                'AP':1,
                'SO':0.9,
                'EZ':0.5 * ez_mult,
                'HD':1.06,
                'HT':0.3 * ht_mult,
                'DT':1.2,
                'NC':1.2,
                'HR':1.1,
                'SD':1,
                'FL':1.12,
                'NF':1,
                'MR':1
    }

    for mod in mod_list:
        mod_multiplier *= mult_dict[mod]
        if mod != "NF":
            mod_str += mod
    
    if mod_str == "":
        mod_str = "NM"

    return mod_str, mod_multiplier


def get_token(client_id, client_secret):
    url = "https://osu.ppy.sh/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "public"
    }

    json_file = requests.post(url, headers=headers, data=data)
    content = json.loads(json_file.content)
    
    return content["access_token"]


class getMatchJson:
    def __init__(self, token):
        self.token = token


    def get_match_json(self, match_id):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        json_file = requests.get(f"https://osu.ppy.sh/api/v2/matches/{match_id}", headers=headers)
        match_json = json.loads(json_file.content)

        while match_json["events"][0]["detail"]["type"] != "match-created":
            event_id = match_json["events"][0]["id"]

            json_file = requests.get(f"https://osu.ppy.sh/api/v2/matches/{match_id}?before={event_id}", headers=headers)
            match_json_add = json.loads(json_file.content)\
            
            match_json["events"] = match_json_add["events"] + match_json["events"] 

        return match_json


if __name__ == "__main__":
    start_time = time.time()


    with open('client_info.txt', 'r') as file:
        client_info = file.read()

    print(f"Finish reading file --- {time.time() - start_time} seconds ---")
    
    client_id, client_secret = client_info.split()
    token = get_token(client_id, client_secret)

    print(f"--- {time.time() - start_time} seconds ---")