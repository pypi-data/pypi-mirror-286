import pandas as pd


class performanceScoreHelper:
    def __init__(self, player_dict, df_preprocess):
        self.player_dict = player_dict
        self.df_preprocess = df_preprocess

    
    def assign_mvp(self, group):
        max_score = group["score"].max()
        group["mvp"] = group["score"] == max_score
        return group
    
    
    def player_mapping(self):
        return {k: v["player"] for k, v in self.player_dict.items()}
    

    def team_mapping(self):
        return {k: v["team"] for k, v in self.player_dict.items()}
    

    def user_id_counts(self):
        return self.df_preprocess["user_id"].value_counts()
    

    def team_counts(self):
        return self.df_preprocess["team"].value_counts()
    

    def sum_ratio(self):
        self.df_preprocess["sum_ratio"] = self.df_preprocess["score"] / self.df_preprocess["avg_score_map"]
        return self.df_preprocess.groupby("user_id")["sum_ratio"].sum().reset_index()
    
    
    def sum_score(self):
        return self.df_preprocess.groupby("user_id")["score"].sum().reset_index(name="avg_score")
    

    def sum_normalised_score(self):
        return self.df_preprocess.groupby("user_id")["normalised_score"].sum().reset_index(name="avg_normalised_score")
    

    def sum_accuracy(self):
        return self.df_preprocess.groupby("user_id")["accuracy"].sum().reset_index(name="avg_accuracy")
    

    def best_score(self):
        idx = self.df_preprocess.groupby("user_id")["score"].idxmax()
        best_score = self.df_preprocess.loc[idx, ["user_id", "score", "pick"]]
        best_score.rename(columns={"score": "best_score", "pick": "best_pick"}, inplace=True)
        return best_score
    

    def best_normalised_score(self):
        idx = self.df_preprocess.groupby("user_id")["normalised_score"].idxmax()
        best_normalised_score = self.df_preprocess.loc[idx, ["user_id", "normalised_score", "pick"]]
        best_normalised_score.rename(columns={"normalised_score": "best_normalised_score", "pick": "best_normalised_pick"}, inplace=True)
        return best_normalised_score
    

    def mvp(self, team_size):
        self.df_preprocess = self.df_preprocess.groupby(self.df_preprocess.index // (2 * team_size)).apply(self.assign_mvp).reset_index(drop=True)
        return self.df_preprocess.groupby("user_id")["mvp"].sum().reset_index()

    
    def update_df_preprocess(self, df_preprocess):
        self.df_preprocess = df_preprocess