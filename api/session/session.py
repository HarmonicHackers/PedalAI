from __future__ import annotations

import os
from typing import List
import uuid

from session.track import Track
from pedalboard import Plugin
from pedalboard.io import AudioFile
import numpy as np
import pickle
from mistralai.models.chat_completion import ToolCall

DEAFAULT_SAMPLE_RATE = 44100
DEFAULT_NUM_CHANNELS = 2


class Session:
    def __init__(self, path: str = "./pedalAi/sessions", **kwargs) -> None:
        self.plugins: List[ToolCall] = []
        self.id = kwargs.get("session_id")
        if self.id is None:
            self.id = "session_{}".format(str(uuid.uuid4()))
        self.save_path = os.path.join(path, self.id)

    def save(self) -> None:
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        if self.original:
            with open(self.original.path, "wb") as f:
                f.write(self.original.contents)

        if self.last_modified:
            print("In here")
            with open(self.last_modified.path, "wb") as f:
                f.write(self.last_modified.contents)

        if len(self.plugins) > 0:
            with open(os.path.join(self.save_path, "plugins.pkl"), "wb") as f:
                pickle.dump(self.plugins, f)

    def add_track(self, track: Track) -> None:
        self.original = track

    def add_plugin(self, plugin: Plugin) -> None:
        self.plugins.append(plugin)

    @staticmethod
    def load(session_id: str) -> Session:
        path = os.path.join("./pedalAi/sessions", session_id)
        session = Session("./pedalAi/sessions", session_id=session_id)
        original_path = os.path.join(path, "original.wav")
        modified_path = os.path.join(path, "modified.wav")

        if os.path.exists(original_path):
            with open(original_path, "rb") as f:
                samples = f.read()

                original_track = Track(
                    "original",
                    0.0,
                    "",
                    samples,
                    original_path,
                )
                session.original = original_track

        if os.path.exists(modified_path):
            with open(modified_path, "rb") as f:
                samples = f.read()

                modified_track = Track(
                    "original",
                    0.0,
                    "",
                    samples,
                    modified_path,
                )
                print("if the next print prints, that's not the error")
                session.last_modified = modified_track
                print("next print")

        if os.path.exists(os.path.join(session.save_path, "plugins.pkl")):
            with open(
                os.path.join(session.save_path, "plugins.pkl"), "rb"
            ) as f:
                session.plugins = pickle.load(f)

        return session

    @property
    def last_modified(self) -> Track:
        return self._last_modified

    @last_modified.setter
    def last_modified(self, t: Track) -> None:
        self._last_modified = t

    @property
    def original(self) -> Track:
        return self._original

    @original.setter
    def original(self, t: Track) -> None:
        self._original = t

    def rollback(self) -> None:
        del self.plugins[-1]
