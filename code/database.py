import json
import ntpath
import sqlite3 as sqlite

import pandas as pd

from code.util.features import get_features, get_video_list
from code.util.log import log
from code.util.video import get_duration


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
            "CREATE TABLE IF NOT EXISTS videos (name TEXT PRIMARY KEY NOT NULL, duration INT NOT NULL, colorhists TEXT);")

    def insert_features(self, name, duration, colorhists, verbose=False):
        """
        initializes database
        :param name: name of database file
        :param duration: duration of video
        :param colorhists: colorhists features of video
        :param verbose: option to display information
        """
        try:
            self.conn.execute(
                "INSERT INTO videos (name, duration, colorhists) VALUES ('" + name + "', " + str(
                    duration) + ", '" + colorhists + "')");
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
            features_video = {'colorhists': json.loads(row[2])}
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

            # Compute features
            features = get_features(video)

            # Convert feature arrays to string
            str_colorhists = pd.Series(features["colorhists"]).to_json(orient='values')

            # Save features in database
            self.insert_features(name, get_duration(video), str_colorhists, verbose)
            self.conn.commit()
