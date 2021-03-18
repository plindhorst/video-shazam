import ntpath
import sqlite3 as sqlite

import pandas as pd

from code.util.features import get_features, get_video_list
from code.util.video import get_duration


class Database:
    def __init__(self, name):
        self.conn = sqlite.connect(name)

    def close(self):
        self.conn.close()

    def create(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS videos (name TEXT PRIMARY KEY NOT NULL, duration INT NOT NULL, colorhists TEXT, colorhistdiffs TEXT, tempdiffs TEXT);")

    def insert_features(self, name, duration, colorhists, colorhistdiffs, tempdiffs):
        try:
            self.conn.execute(
                "INSERT INTO videos (name, duration, colorhists, colorhistdiffs, tempdiffs) VALUES ('" + name + "', " + str(
                    duration) + ", '" + colorhists + "', '" + colorhistdiffs + "', '" + tempdiffs + "')");
        except sqlite.IntegrityError:
            print("IntegrityError: duplicate key \"" + name + "\"")

    def get_features(self, name):
        rows = self.conn.execute("SELECT * from videos WHERE name = '" + name + "'")
        for row in rows:
            return row

    def get_video_names(self):
        rows = self.conn.execute("SELECT name from videos")
        videos = []
        for row in rows:
            videos.append(row[0])
        return videos

    def build(self, videos_path):
        videos = get_video_list(videos_path)
        for video in videos:
            name = ntpath.basename(video)
            print("Creating database features for: \"" + name + "\"")

            features = get_features(video)

            str_colorhists = pd.Series(features["colorhists"]).to_json(orient='values')
            str_colorhistdiffs = pd.Series(features["colorhistdiffs"]).to_json(orient='values')
            str_tempdiffs = pd.Series(features["tempdiffs"]).to_json(orient='values')

            self.insert_features(name, get_duration(video), str_colorhists, str_colorhistdiffs, str_tempdiffs)
            self.conn.commit()
