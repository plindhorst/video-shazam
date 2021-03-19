import ntpath
import os
import sqlite3 as sqlite

import pandas as pd

from code.util.features import get_features, get_video_list
from code.util.log import log
from code.util.video import get_duration, save_audio


class Database:
    def __init__(self, name):
        self.conn = sqlite.connect(name)

    def close(self):
        self.conn.close()

    def create(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS videos (name TEXT PRIMARY KEY NOT NULL, duration INT NOT NULL, colorhists TEXT, colorhistdiffs TEXT, tempdiffs TEXT, audiopowers TEXT);")

    def insert_features(self, name, duration, colorhists, colorhistdiffs, tempdiffs, audiopowers, verbose=False):
        try:
            self.conn.execute(
                "INSERT INTO videos (name, duration, colorhists, colorhistdiffs, tempdiffs, audiopowers) VALUES ('" + name + "', " + str(
                    duration) + ", '" + colorhists + "', '" + colorhistdiffs + "', '" + tempdiffs + "', '" + audiopowers + "')");
        except sqlite.IntegrityError:
            log("IntegrityError: duplicate key \"" + name + "\"", verbose)

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

    def build(self, videos_path, verbose=False):
        videos = get_video_list(videos_path)
        videos_database = self.get_video_names()
        for video in videos:
            name = ntpath.basename(video)
            if name in videos_database:
                log("Error: video features already in database for \"" + name + "\"", verbose)
                continue
            log("Creating database features for \"" + name + "\"", verbose)

            audio_path = os.path.splitext(video)[0] + '.wav'
            save_audio(video, audio_path)
            features = get_features(video, audio_path)

            str_colorhists = pd.Series(features["colorhists"]).to_json(orient='values')
            str_colorhistdiffs = pd.Series(features["colorhistdiffs"]).to_json(orient='values')
            str_tempdiffs = pd.Series(features["tempdiffs"]).to_json(orient='values')
            str_audiopowers = pd.Series(features["audiopowers"]).to_json(orient='values')

            self.insert_features(name, get_duration(video), str_colorhists, str_colorhistdiffs, str_tempdiffs,
                                 str_audiopowers, verbose)
            self.conn.commit()
