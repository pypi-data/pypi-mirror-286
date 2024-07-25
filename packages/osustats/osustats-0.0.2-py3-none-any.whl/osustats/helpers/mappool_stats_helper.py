import pandas as pd


class mappoolStatsHelper:
    def __init__(self, df_preprocess):
        self.df_preprocess = df_preprocess

    
    def df_best_player(self):
        idx = self.df_preprocess.groupby('beatmap_id')['score'].idxmax()
        df_best_player = self.df_preprocess.loc[idx, ['beatmap_id', 'player', 'mods', 'score', 'accuracy']]

        df_best_player.rename(columns={
            'player': 'best_player',
            'score': 'player_score',
            'accuracy': 'player_accuracy'
        }, inplace=True)

        return df_best_player
    

    def df_best_team(self):
        idx = self.df_preprocess.groupby('beatmap_id')['sum_score_team'].idxmax()
        df_best_team = self.df_preprocess.loc[idx, ['beatmap_id', 'team', 'sum_score_team', 'avg_accuracy_team']]

        df_best_team.rename(columns={
            'team': 'best_team',
            'sum_score_team': 'team_score',
            'avg_accuracy_team': 'team_accuracy'
        }, inplace=True)

        return df_best_team
    

    def avg_score(self):
        return self.df_preprocess.groupby('beatmap_id')['score'].mean().reset_index(name="avg_score")
    

    def avg_accuracy(self):
        return self.df_preprocess.groupby('beatmap_id')['accuracy'].mean().reset_index(name="avg_accuracy")
    

    def pick_count(self, team_size):
        pick_count = self.df_preprocess.groupby('beatmap_id').size().reset_index(name='pick_count')
        pick_count['pick_count'] /= 2 * team_size
        return pick_count
    

    def ban_count_map(self, beatmap_dict):
        return {key: value['ban_count'] for key, value in beatmap_dict.items()}