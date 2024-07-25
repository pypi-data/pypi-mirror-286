"""
class163/music.py
Version: 0.1.1
Author: CooooldWind_
E-Mail: 3091868003@qq.com
Copyright @CooooldWind_ / Following GNU_AGPLV3+ License
"""

import time
import netease_encode_api as encode


class Music:
    def __init__(self, id: int) -> None:
        self.id = str(id)
        self.title = ""
        self.subtitle = ""
        self.trans_title = ""
        self.album = ""
        self.trans_album = ""
        self.artist: list[str] = []
        self.trans_artist: dict = {}
        self.publish_time = None
        self.__info_encode_data = {
            "c": str([{"id": self.id}]),
        }
        self.__lyric_encode_data = {
            "id": self.id,
            "lv": -1,
            "tv": -1,
        }
        self.raw_info: dict = {}
        self.sorted_info: dict = {}

    def get(self, session: encode.EncodeSession = encode.EncodeSession()) -> dict:
        self.raw_info = session.get_response(
            url="https://music.163.com/weapi/v3/song/detail",
            encode_data=self.__info_encode_data,
        )["songs"][0]
        self.title = self.raw_info["name"]
        self.album = self.raw_info["al"]["name"]
        self.publish_time = time.localtime(int(self.raw_info["publishTime"]) / 1000)
        self.publish_time = self.publish_time[0:3]
        if "alia" in self.raw_info:
            if len(self.raw_info["alia"]) > 0:
                self.subtitle = self.raw_info["alia"][0]
        if "tns" in self.raw_info:
            if len(self.raw_info["tns"]) > 0:
                self.trans_title = self.raw_info["tns"][0]
        if "tns" in self.raw_info["al"]:
            if len(self.raw_info["al"]["tns"]) > 0:
                self.trans_album = self.raw_info["al"]["tns"][0]
        for i in self.raw_info["ar"]:
            self.artist.append(i["name"])
            if "tns" in i:
                if len(i["tns"]) > 0:
                    self.trans_artist.update({str(i["name"]): i["tns"]})
        self.sorted_info.update(
            {
                "id": self.id,
                "title": self.title,
                "album": self.album,
                "artist": self.artist,
                "publish_time": self.publish_time,
                "subtitle": self.subtitle,
                "trans_title": self.trans_title,
                "trans_album": self.trans_album,
                "trans_artist": self.trans_artist,
            }
        )
        return self.sorted_info


def url_to_id(url: str) -> int:
    if url.find("&") != -1:
        return int(url[url.find("song?id=") + 8 : url.find("&")])
    else:
        return int(url[url.find("song?id=") + 8 :])
