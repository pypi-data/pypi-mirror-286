import pandas as pd
import os, time
from helpers import *
from multiprocessing import Pool


class osuStats:
    def __init__(self, stage_name, stage_type, team_size, csv_file, client_id, client_secret, ez_mult = 1, ht_mult = 1):
        self.stage_name = stage_name
        self.stage_type = stage_type
        self.team_size = team_size

        os.makedirs(stage_name, exist_ok=True)

        self.preprocess(csv_file, client_id, client_secret, ez_mult, ht_mult)

        if stage_type == "qualifiers":
            self.df_preprocess_better_run = self.filter_better_run()
    

    def preprocess(self, csv_file, client_id, client_secret, ez_mult, ht_mult):
        print("Preprocessing data", end="")

        # Read raw input file
        df_raw = pd.read_csv(csv_file, dtype=str)

        # Extract info about players, beatmaps and matches
        self.player_dict, self.beatmap_dict, self.match_id_list = process_raw_df(df_raw)
        
        # Create empty df for data to be inserted into
        self.df_preprocess = pd.DataFrame(columns=df_preprocess_columns())

        # Get token for osu API v2
        token = get_token(client_id, client_secret)

        # Get list of match json using multiprocessing
        api_obj = getMatchJson(token)
        with Pool() as pool:
            match_json_list = pool.map(api_obj.get_match_json, self.match_id_list)

        # Iterate through matches
        id = 0
        for match_id in self.match_id_list:
            match_json = match_json_list[id]
            id += 1
            match_name = match_json["match"]["name"]
            
            for event in match_json["events"]:
                if "game" in event:
                    game = event["game"]
                    beatmap_id = str(game["beatmap_id"])

                    if beatmap_id in self.beatmap_dict:
                        pick, beatmap = self.beatmap_dict[beatmap_id]["pick"], self.beatmap_dict[beatmap_id]["beatmap"]

                        for play in game["scores"]:
                            user_id = str(play["user_id"])

                            if user_id in self.player_dict:
                                player, team = self.player_dict[user_id]["player"], self.player_dict[user_id]["team"]
                                score, accuracy, mod_list = play["score"], play["accuracy"] * 100, play["mods"]
                                
                                mod_str, mod_multiplier = mod_process(mod_list, ez_mult, ht_mult)
                                normalised_score = score / mod_multiplier

                                new_row = {"match_id": match_id, "match_name": match_name, \
                                           "pick": pick, "beatmap": beatmap, "beatmap_id": beatmap_id, \
                                           "player": player, "user_id": user_id, "team": team, \
                                           "score": score, "normalised_score": normalised_score, "accuracy": accuracy, "mods": mod_str}
                                
                                self.df_preprocess.loc[len(self.df_preprocess)] = new_row
        
        # Add extra info that will be used often
        # Average score for each map
        self.df_preprocess["avg_score_map"] = self.df_preprocess.groupby(self.df_preprocess.index // (2 * self.team_size))["score"].transform("mean")

        # Sum of score for each team in each map
        self.df_preprocess["sum_score_team"] = self.df_preprocess.groupby(self.df_preprocess.index // self.team_size)["score"].transform("sum")

        # Average accuracy for each team in each map
        self.df_preprocess["avg_accuracy_team"] = self.df_preprocess.groupby(self.df_preprocess.index // self.team_size)["accuracy"].transform("mean")

        # Save csv
        self.df_preprocess.to_csv(os.path.join(self.stage_name, "preprocess.csv"), index=False)
        print(" -- Done")


    def remove_rows_preprocess(self, start, end):
        print(f"Deleting rows {start} to {end} in preprocess.csv", end="")

        # Deleting rows
        self.df_preprocess = self.df_preprocess.drop(self.df_preprocess.index[start : end+1]).reset_index()

        # Recalculate extra info that will be used often
        # Average score for each map
        self.df_preprocess["avg_score_map"] = self.df_preprocess.groupby(self.df_preprocess.index // (2 * self.team_size))["score"].transform("mean")

        # Sum of score for each team in each map
        self.df_preprocess["sum_score_team"] = self.df_preprocess.groupby(self.df_preprocess.index // self.team_size)["score"].transform("sum")

        # Average accuracy for each team in each map
        self.df_preprocess["avg_accuracy_team"] = self.df_preprocess.groupby(self.df_preprocess.index // self.team_size)["accuracy"].transform("mean")

        # Save csv
        self.df_preprocess.to_csv(os.path.join(self.stage_name, "preprocess.csv"), index=False)
        print(" -- Done")


    def performance_score(self):
        print("Generate performance score sheet", end="")

        df_main = pd.DataFrame()
        helper = performanceScoreHelper(self.player_dict, self.df_preprocess)

        # Get ID
        df_main["user_id"] = self.df_preprocess["user_id"].unique()

        # Get player name
        df_main["player"] = df_main["user_id"].astype(str).map(helper.player_mapping())

        # Get team name
        df_main["team"] = df_main["user_id"].astype(str).map(helper.team_mapping())

        # Get number of maps played
        df_main["match_count"] = df_main["user_id"].map(helper.user_id_counts())

        # Calculate percentage of match played
        df_main["team_match_count"] = df_main["team"].map(helper.team_counts()) / self.team_size
        df_main["percentage_play"] = df_main["match_count"] / df_main["team_match_count"] * 100

        # If quals, filter only tries that counts toward the result, and recalculate number of maps played for player and team for each
        if self.stage_type == "qualifiers":
            # Filter and update the helper object
            helper.update_df_preprocess(self.df_preprocess_better_run)

            # Get number of maps played
            df_main["taken_match_count"] = df_main["user_id"].map(helper.user_id_counts())

            # Calculate percentage of match played
            df_main["taken_team_match_count"] = df_main["team"].map(helper.team_counts()) / self.team_size
            df_main["taken_percentage_play"] = df_main["taken_match_count"] / df_main["taken_team_match_count"] * 100
 
        # Get sum of score ratio
        df_main = df_main.merge(helper.sum_ratio(), on="user_id", how="left")

        # Calculate match cost and sort df
        df_main["match_cost"] = 2 / (df_main["match_count"] + 2) * df_main["sum_ratio"]
        df_main.sort_values(by="match_cost", ascending=False, inplace=True)

        # Calculate MVP count (only for bracket stage)
        if self.stage_type == "bracket":
            df_main = df_main.merge(helper.mvp(self.team_size), on="user_id", how="left")

        # Calculate average score
        df_main = df_main.merge(helper.sum_score(), on="user_id", how="left")
        df_main["avg_score"] = df_main["avg_score"] / df_main["match_count"]

        # Calculate normalised average score
        df_main = df_main.merge(helper.sum_normalised_score(), on="user_id", how="left")
        df_main["avg_normalised_score"] = df_main["avg_normalised_score"] / df_main["match_count"]

        # Calculate average accuracy
        df_main = df_main.merge(helper.sum_accuracy(), on="user_id", how="left")
        df_main["avg_accuracy"] = df_main["avg_accuracy"] / df_main["match_count"] * 100

        # Calculate best score and corresponding pick
        df_main = df_main.merge(helper.best_score(), on="user_id", how="left")

        # Calculate normalised best score and corresponding pick
        df_main = df_main.merge(helper.best_normalised_score(), on="user_id", how="left")

        # Drop columns and sort
        df_main.drop(columns=["user_id", "sum_ratio"], inplace=True)

        # Save csv
        df_main.to_csv(os.path.join(self.stage_name, "performance_score.csv"), index=False)
        print(" -- Done")


    def filter_better_run(self):
        df_preprocess = self.df_preprocess.copy()

        df_preprocess["sum_score"] = df_preprocess.groupby(df_preprocess.index // self.team_size)["score"].transform("sum")

        # Identify segments by using a helper column
        df_preprocess['segment'] = ((df_preprocess['team'] != df_preprocess['team'].shift(1)) | (df_preprocess['beatmap_id'] != df_preprocess['beatmap_id'].shift(1))).cumsum()

        # Group by segments and calculate max sum_score for each segment
        segments = df_preprocess.groupby('segment').agg({
            'team': 'first',
            'beatmap_id': 'first',
            'sum_score': 'first'
        }).reset_index()

        # Identify segments to keep
        to_keep = segments.loc[segments.groupby(['team', 'beatmap_id'])['sum_score'].idxmax()]

        # Filter out rows from df_preprocess where segments are not in to_keep
        df_preprocess = df_preprocess[df_preprocess['segment'].isin(to_keep['segment'])].drop(columns='segment')

        self.df_preprocess_better_run = df_preprocess


    def mappool_stats(self):
        # Note that for qualifiers, this takes the results of all runs

        print("Creating mappool stats", end="")

        # Create helper object
        helper = mappoolStatsHelper(self.df_preprocess)

        # Create df with basic beatmap info
        keys, values = list(self.beatmap_dict.keys()), list(self.beatmap_dict.values())

        # Create DataFrame
        df_main = pd.DataFrame(values)
        df_main.insert(0, 'beatmap_id', keys)

        # Extract info of best player
        df_main = df_main.merge(helper.df_best_player(), on='beatmap_id', how='left')

        # Extract info of best team
        df_main = df_main.merge(helper.df_best_team(), on='beatmap_id', how='left')

        # Calculate average score
        df_main = df_main.merge(helper.avg_score(), on='beatmap_id', how='left')

        # Calculate average accuracy
        df_main = df_main.merge(helper.avg_accuracy(), on='beatmap_id', how='left')

        # Only calculates pick and ban stats for bracket stage
        if self.stage_type == "bracket":
            match_count = self.df_preprocess["match_id"].nunique()
            
            # Calculate pick count
            df_main = df_main.merge(helper.pick_count(self.team_size), on='beatmap_id', how='left')

            # Calculate pick percentage
            df_main["pick_percentage"] = df_main["pick_count"] / match_count * 100

            # Calculate ban count
            df_main["ban_count"] = df_main['beatmap_id'].map(helper.ban_count_map(self.beatmap_dict))

            # Calculate ban percentage
            df_main["ban_percentage"] = df_main["ban_count"] / match_count * 100


        # Save csv
        df_main.to_csv(os.path.join(self.stage_name, "mappool_stats.csv"), index=False)
        print(" -- Done")
        
    


if __name__ == "__main__":
    start_time = time.time()


    with open('client_info.txt', 'r') as file:
        client_info = file.read()
    
    client_id, client_secret = client_info.split()

    test_bracket = True
    test_speed = True

    if test_bracket:
        stats = osuStats("OWC - Grand Final", "bracket", 4, "raw_test_bracket.csv", client_id, client_secret)
        stats.remove_rows_preprocess(64, 73)
    elif test_speed:
        stats = osuStats("Beginner Tourney", "bracket", 1, "raw_test_speed.csv", client_id, client_secret)
    else:
        stats = osuStats("4DM4 - Qualifiers", "qualifiers", 3, "raw_test_qual.csv", client_id, client_secret)
    
    stats.performance_score()
    stats.mappool_stats()

    print(f"--- {time.time() - start_time} seconds ---")
