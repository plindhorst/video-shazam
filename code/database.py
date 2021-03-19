import json
import ntpath
import os
import sqlite3 as sqlite

import pandas as pd

from code.util.features import get_features, get_video_list
from code.util.log import log
from code.util.video import get_duration, save_audio


class Database:
    def __init__(self, name):
        """
        initializes database
        :param name: name of database file
        """
        self.conn = sqlite.connect(name)

    def close(self):
        """
        closes connection to database
        """
        self.conn.close()

    def create(self):
        """
        create database tables
        """
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS videos (name TEXT PRIMARY KEY NOT NULL, duration INT NOT NULL, colorhists TEXT, colorhistdiffs TEXT, tempdiffs TEXT, audiopowers TEXT);")

    def insert_features(self, name, duration, colorhists, colorhistdiffs, tempdiffs, audiopowers, verbose=False):
        """
        initializes database
        :param name: name of database file
        :param duration: duration of video
        :param colorhists: colorhists features of video
        :param colorhistdiffs: colorhistdiffs features of video
        :param tempdiffs: tempdiffs features of video
        :param audiopowers: audiopowers features of video
        :param verbose: option to display information
        """
        try:
            self.conn.execute(
                "INSERT INTO videos (name, duration, colorhists, colorhistdiffs, tempdiffs, audiopowers) VALUES ('" + name + "', " + str(
                    duration) + ", '" + colorhists + "', '" + colorhistdiffs + "', '" + tempdiffs + "', '" + audiopowers + "')");
        except sqlite.IntegrityError:
            log("IntegrityError: duplicate key \"" + name + "\"", verbose)

    def get_features(self, name):
        """
        retrieve features from database
        :param name: name of video
        :return: duration and array of features
        """
        rows = self.conn.execute("SELECT * from videos WHERE name = '" + name + "'")
        for row in rows:
            features_video = {'colorhists': json.loads(row[2]),
                              'tempdiffs': json.loads(row[3]),
                              'colorhistdiffs': json.loads(row[4]),
                              'audiopowers': json.loads(row[5]),
                              'mfccs': []}
            return row[1], features_video

    def get_video_names(self):
        """
        retrieve list of videos in database
        :return: list of videos in database
        """
        rows = self.conn.execute("SELECT name from videos")
        videos = []
        for row in rows:
            videos.append(row[0])
        return videos

    def build(self, videos_path, verbose=False):
        """
        fill database with videos and their features
        :param videos_path: paths of videos
        :param verbose: option to display information
        """
        videos = get_video_list(videos_path)
        videos_database = self.get_video_names()
        for video in videos:

            # Check if video is already in database
            name = ntpath.basename(video)
            if name in videos_database:
                log("Video features already in database for \"" + name + "\"", verbose)
                continue
            log("Creating database features for \"" + name + "\"", verbose)

            # Save audio of video
            audio_path = os.path.splitext(video)[0] + '.wav'
            save_audio(video, audio_path)

            # Compute features
            features = get_features(video, audio_path)

            # Convert feature arrays to string
            str_colorhists = pd.Series(features["colorhists"]).to_json(orient='values')
            str_colorhistdiffs = pd.Series(features["colorhistdiffs"]).to_json(orient='values')
            str_tempdiffs = pd.Series(features["tempdiffs"]).to_json(orient='values')
            str_audiopowers = pd.Series(features["audiopowers"]).to_json(orient='values')

            # Save features in database
            self.insert_features(name, get_duration(video), str_colorhists, str_colorhistdiffs, str_tempdiffs,
                                 str_audiopowers, verbose)
            self.conn.commit()