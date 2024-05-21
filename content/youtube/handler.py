import os
import random
from typing import Literal

import pytube

from content.youtube.channel import Channel
from utilities.config.folder import PERSISTENT_FOLDER

class YoutubeHandler:
    LONG_VIDEOS = [
        "https://www.youtube.com/watch?v=7ghSziUQnhs",
        "https://www.youtube.com/watch?v=n_Dv4JMiwK8",
        "https://www.youtube.com/watch?v=intRX7BRA90",
        "https://www.youtube.com/watch?v=JPjwv8RHhMY",
        "https://www.youtube.com/watch?v=Mc-ktOtdTuM",
        "https://www.youtube.com/watch?v=_2O8X4CveYc",
        "https://www.youtube.com/watch?v=HZzr0C4qWhI",
        "https://www.youtube.com/watch?v=qHl7jfArp0o",
        "https://www.youtube.com/watch?v=8rN8KIgxSUQ",
        "https://www.youtube.com/watch?v=NIrktt51HnU",
        "https://www.youtube.com/watch?v=lfbzKpcLeC4",
        "https://www.youtube.com/watch?v=TxSM27sVz4k",
        "https://www.youtube.com/watch?v=1rJBP0jz95M",
        "https://www.youtube.com/watch?v=CwTbFjC2yJE",
        "https://www.youtube.com/watch?v=1TrzGpd8kaI",
        "https://www.youtube.com/watch?v=NjvFF2Kvx1U",
        "https://www.youtube.com/watch?v=s9Zsfiik6RU",
        "https://www.youtube.com/watch?v=93S5-ZgdqJc",
        "https://www.youtube.com/watch?v=bSW5PYtoiGo",
        "https://www.youtube.com/watch?v=6XEj_bPkR4I",
        "https://www.youtube.com/watch?v=pN5KfSJf7no",
        "https://www.youtube.com/watch?v=kGEMLiBqpSc",
        "https://www.youtube.com/watch?v=gOZ9Vwwbilo",
        "https://www.youtube.com/watch?v=mPFCxDCs5Z8",
        "https://www.youtube.com/watch?v=SjNl8GNUchA",
        "https://www.youtube.com/watch?v=LRSAaFO22Xw",
        "https://www.youtube.com/watch?v=ziqRk4pUktY",
        "https://www.youtube.com/watch?v=D6x1YIZw_uA",
        "https://www.youtube.com/watch?v=d3FDDkQZu5I",
        "https://www.youtube.com/watch?v=wqOtnconzes",
        "https://www.youtube.com/watch?v=zpbrNdh0IKg",
        "https://www.youtube.com/watch?v=-g7qkB-Q7v4",
        "https://www.youtube.com/watch?v=3BjdTLxPo1w",
        "https://www.youtube.com/watch?v=8PGY3etmwxA",
        "https://www.youtube.com/watch?v=NXwqIIBCasg",
        "https://www.youtube.com/watch?v=cERG4Ha-FVs",
        "https://www.youtube.com/watch?v=9sWuAYWqVnQ",
        "https://www.youtube.com/watch?v=SuOtIGAK3tc",
        "https://www.youtube.com/watch?v=rzvsWD-M2Es",
        "https://www.youtube.com/watch?v=WJ6DSjcliag",
        "https://www.youtube.com/watch?v=KIkLfwqMIao",
        "https://www.youtube.com/watch?v=OU0oblHibqo",
        "https://www.youtube.com/watch?v=ouv1XgPQ12M",
        "https://www.youtube.com/watch?v=jus4fTiOBIM",
        "https://www.youtube.com/watch?v=tzJsp2pVBg8",
        "https://www.youtube.com/watch?v=SuBO612mYDY",
        "https://www.youtube.com/watch?v=4bPHCyBqlhc",
        "https://www.youtube.com/watch?v=WAXVz7txvy4",
        "https://www.youtube.com/watch?v=9aPZtv8jBFY",
        "https://www.youtube.com/watch?v=MSJtsUGQMmk",
        "https://www.youtube.com/watch?v=Q8752Il3df8",
        "https://www.youtube.com/watch?v=vlSc8qXAhGM",
        "https://www.youtube.com/watch?v=A_XFy3Epb0s",
        "https://www.youtube.com/watch?v=avOnoKzcDP8",
        "https://www.youtube.com/watch?v=qYDL3TQvaRY",
        "https://www.youtube.com/watch?v=Xs6Ma95JXS0",
        "https://www.youtube.com/watch?v=jdrp1u8a4r8",
        "https://www.youtube.com/watch?v=CsvA46HeZ4I",
        "https://www.youtube.com/watch?v=wTfzaN1N52g",
        "https://www.youtube.com/watch?v=IRsngqbLbUo",
        "https://www.youtube.com/watch?v=pa9Bg2ulFWc",
        "https://www.youtube.com/watch?v=nO60GGzk9e4",
        "https://www.youtube.com/watch?v=Bay97DNgZBM",
        "https://www.youtube.com/watch?v=MVaMnwKULoA",
        "https://www.youtube.com/watch?v=8ixWIXGNCHY",
        "https://www.youtube.com/watch?v=I0sjZI2zmyk",
        "https://www.youtube.com/watch?v=TrPPP_qfYTc",
        "https://www.youtube.com/watch?v=8tjy3FnjaWc",
        "https://www.youtube.com/watch?v=mS5twjTrScU",
        "https://www.youtube.com/watch?v=UjcCpOb_-NE",
        "https://www.youtube.com/watch?v=-W07mtfxQfg",
        "https://www.youtube.com/watch?v=MDa5gvIn65Q",
        "https://www.youtube.com/watch?v=tobXVq6nDRk",
        "https://www.youtube.com/watch?v=TYrZWX87v7E",
        "https://www.youtube.com/watch?v=U5ScJQXrszo",
        "https://www.youtube.com/watch?v=PYM8V0SI53I",
        "https://www.youtube.com/watch?v=aKOO421B0X4",
        "https://www.youtube.com/watch?v=S7HquTz9afg",
        "https://www.youtube.com/watch?v=1d3MwW2FioI",
        "https://www.youtube.com/watch?v=hpvVv2L-_8M",
        "https://www.youtube.com/watch?v=wbcqoG5EbPs",
        "https://www.youtube.com/watch?v=S3ToLS-751I",
        "https://www.youtube.com/watch?v=q0TUzSv-6vc",
        "https://www.youtube.com/watch?v=6YGWlCeWt_Y",
        "https://www.youtube.com/watch?v=MgqiaTNq4_s",
        "https://www.youtube.com/watch?v=jYt9rZd4H_A",
        "https://www.youtube.com/watch?v=oPOpzvxwEqM",
        "https://www.youtube.com/watch?v=7C8Eu9tsoYg",
        "https://www.youtube.com/watch?v=wrl_aDnTG7Y",
        "https://www.youtube.com/watch?v=mNv7BywyQdA",
        "https://www.youtube.com/watch?v=CC7HJ5JFilw",
        "https://www.youtube.com/watch?v=P8jg85nFQgc",
        "https://www.youtube.com/watch?v=0mwLUOZUFys",
        "https://www.youtube.com/watch?v=Tykw5LFdR0A",
        "https://www.youtube.com/watch?v=59fDKF4dAMQ",
        "https://www.youtube.com/watch?v=7y3NdFSLg3k",
        "https://www.youtube.com/watch?v=aaUFUGBo0e0",
        "https://www.youtube.com/watch?v=YvJTUZ0A4qQ",
        "https://www.youtube.com/watch?v=urpDgytNiEk",
        "https://www.youtube.com/watch?v=u87c--Fc01M",
        "https://www.youtube.com/watch?v=HOIXyiVpyE0",
        "https://www.youtube.com/watch?v=iZ5ymTZhOtE",
        "https://www.youtube.com/watch?v=zzH6PUKUqFg",
        "https://www.youtube.com/watch?v=7u8PNtxKkKk",
        "https://www.youtube.com/watch?v=2ltD2DRVJTU",
        "https://www.youtube.com/watch?v=UUn8y_zxs5g",
        "https://www.youtube.com/watch?v=MFhjZSqmRsk",
        "https://www.youtube.com/watch?v=d06t-56fFIo",
        "https://www.youtube.com/watch?v=lf8Hs4s7OpQ",
        "https://www.youtube.com/watch?v=ayG137kZvEg",
        "https://www.youtube.com/watch?v=YqDCh3Lu0uA",
        "https://www.youtube.com/watch?v=3f6jRvSj6_o",
        "https://www.youtube.com/watch?v=H5yo4BUpEEs",
        "https://www.youtube.com/watch?v=0Q2RlgtziVg",
        "https://www.youtube.com/watch?v=x5eaUGv05Bg",
        "https://www.youtube.com/watch?v=vTlHrunBrQM",
    ]

    MONEY_VIDEOS = [
        {
            "type": "playlist",
            "url": "https://www.youtube.com/watch?list=PLfLNWzHn9MZDbWyDEEjrkCEkTu5jGi1hn"
        }
    ]

    MUSIC = [
        "https://www.youtube.com/watch?v=BEXL80LS0-I",
        "https://www.youtube.com/watch?v=-oJOVDULGTA",
        "https://www.youtube.com/watch?v=LJbQCBURv9o",
        "https://www.youtube.com/watch?v=AHG5Fo1opjw",
        "https://www.youtube.com/watch?v=eQ4jhCSjaVk",
        "https://www.youtube.com/watch?v=CBUApqSxMlY",
        "https://www.youtube.com/watch?v=zYgqJ9tAqzQ",
        "https://www.youtube.com/watch?v=TdTbhggtWx0",
        "https://www.youtube.com/watch?v=05LFs0ZI2m0",
        "https://www.youtube.com/watch?v=2k6KruZj59c",
        "https://www.youtube.com/watch?v=-rkecS6RtkI",
        "https://www.youtube.com/watch?v=yFrbRkQvuqs",
        "https://www.youtube.com/watch?v=dmCqaaquYZ4",
        "https://www.youtube.com/watch?v=n97GVCY6xwQ",
        "https://www.youtube.com/watch?v=Zg4pneS2n1g",
        "https://www.youtube.com/watch?v=SjfyBLXzatk",
        "https://www.youtube.com/watch?v=gTicbHRUlA0",
        "https://www.youtube.com/watch?v=-rfclZgwT90",
        "https://www.youtube.com/watch?v=qvJG4ejpn2w",
        "https://www.youtube.com/watch?v=qSQCK9cU2qQ",
        "https://www.youtube.com/watch?v=nnZ4RzDTMP4",
        "https://www.youtube.com/watch?v=w3OPXw25u7A",
        "https://www.youtube.com/watch?v=DTQWvsGh-rs",
        "https://www.youtube.com/watch?v=-UKqA9jt240",
        "https://www.youtube.com/watch?v=CnDi8L0EtAQ",
        "https://www.youtube.com/watch?v=G6M7X9a9dMM",
        "https://www.youtube.com/watch?v=8XDVQ4o3AMY",
        "https://www.youtube.com/watch?v=_uWLGifxc8g",
        "https://www.youtube.com/watch?v=JUqMlGxb78s",
        "https://www.youtube.com/watch?v=sFrjE3mNROM",
        "https://www.youtube.com/watch?v=lwyb745kJvI",
        "https://www.youtube.com/watch?v=NE5B9Synx2k",
        "https://www.youtube.com/watch?v=g2DJw8Zp2EY",
        "https://www.youtube.com/watch?v=7VsBTUP3ojo",
        "https://www.youtube.com/watch?v=H7GRd4C28N4"
    ]

    def _get_youtube_video_id(self, url: str):
        k = lambda x: x.split("=")[0]
        v = lambda x: x.split("=")[1]

        return {k(kv): v(kv) for kv in url.split("?")[1].split("&")}['v']
    
    def get_money_videos(self):
        videos: list[str] = []
        for money_content in self.MONEY_VIDEOS:
            if money_content['type'] == 'playlist':
                playlist = pytube.Playlist(money_content['url'])
                videos.extend(map(lambda video: video.watch_url, playlist.videos))
            else:
                videos.append(money_content['url'])

        return videos
    
    def random_link(self):
        return random.choice(self.LONG_VIDEOS)

    def get_video_title(self, video_url: str):
        return pytube.YouTube(video_url).title

    def random(self, length: Literal["short", "medium", "long"]="long", _retries=5) -> str:
        video_url = self.random_link()

        try:
            return self.download(video_url)
        except:
            if _retries:
                return self.random(length, _retries-1)
            
            raise TimeoutError("timeout for downloading a random video")
    
    def random_song(self) -> str:
        video_url = random.choice(self.MUSIC)

        try:
            return self.download(video_url, mp3=True)
        except:
            return self.random_song()


    def download(self, url, mp3: bool=False, output_folder=PERSISTENT_FOLDER) -> str:
        extension = 'mp4'
        video_id = self._get_youtube_video_id(url)
        
        filename = f"{video_id}.{extension}"
        
        full_path = os.path.join(output_folder, filename)
        if os.path.exists(full_path):
            print("YouTube video already downloaded, skipping")
            return full_path
        
        print("Baixando para caminho:", full_path)
        youtube = pytube.YouTube(url)
        
        video = youtube.streams.get_audio_only() if mp3 else youtube.streams.get_highest_resolution()

        assert video is not None
        
        video.download(output_folder, filename)

        return full_path
    
    def channel(self, channel_url: str):
        return Channel(channel_url)