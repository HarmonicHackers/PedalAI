from __future__ import annotations

import os
from typing import List
import uuid

from track import Track
from session.track import Track


class Session:
    def __init__(self, path: str = "./pedalAi/sessions") -> None:
        self.tracks: List[Track] = []
        self.id = "session_{}".format(str(uuid.uuid4()))
        self.save_path = os.path.join(path, self.id)

    def save(self) -> None:
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        for track in self.tracks:
            track_path = os.path.join(self.save_path, track.name)
            with open(track_path, "wb") as f:
                f.write(track.contents)

    def add_track(self, track: Track) -> None:
        self.tracks.append(track)

    @staticmethod
    def load(session_id: str) -> Session:
        path = os.path.join("./pedalAi/sessions", session_id)
        session = Session(path)
        files = os.listdir(path)
        for file in files:
            track_path = os.path.join(path, file)
            with open(track_path, "rb") as f:
                t = Track(file, 0.0, "unknown", f.read())
                session.tracks.append(t)

        return session
