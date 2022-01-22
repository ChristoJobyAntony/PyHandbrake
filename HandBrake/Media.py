from typing import Dict, List
from pymediainfo import MediaInfo
from pprint import pprint
from HandBrake.AudioTrack import AudioTrack
from HandBrake.TextTrack import TextTrack
from HandBrake.VideoTrack import VideoTrack
import os


class Media :
  
    def __init__(self, file) -> None:

        self.textTrack:List[TextTrack] = []
        self.audioTracks:List[AudioTrack] = []
        self.videoTracks:List[VideoTrack] = []
        
        if os.path.isfile(file):
            media_object = MediaInfo.parse(file)
            if int(media_object.tracks[0].count_of_video_streams) > 0 :
                self._log("File Loaded")
                self.mediaObject : MediaInfo = media_object
            else :
                raise Exception("File given has no video track")
        else :
            raise Exception("File not Found !")
        
        scannedAudioTracks = 1
        scannedTextTracks = 1
        scannedVideoTracks = 1
        for track in media_object.tracks : 
            if track.track_type == "General" : 
                self._loadGeneral(track)
            elif track.track_type == "Video" : 
                self.videoTracks.append(VideoTrack(scannedVideoTracks, track))
                scannedVideoTracks += 1
            elif track.track_type == "Audio" : 
                self.audioTracks.append(AudioTrack(scannedAudioTracks, track))
                scannedAudioTracks += 1
            elif track.track_type == "Text" : 
                self.textTrack.append(TextTrack(scannedTextTracks, track))
                scannedTextTracks += 1
        
        self.height : int = self.videoTracks[0].height
        self.width : int = self.videoTracks[0].width

    def __repr__(self) -> str:
        info = {
            "Path": self.path,
            "Duration" : self.duration,
            "Video Streams" : self.count_of_video_streams,
            "Audio Streams" : self.count_of_audio_streams,
            "Text Streams" : self.count_of_text_streams,

        }
        return "Media File :" + self.fileName + "\n\t" +  "\n\t".join(f"{k} => {v}" for k, v in info.items())
    
    def _loadGeneral (self, track) -> None :
        self.fileName : str = track.file_name_extension
        self.path : str = track.complete_name
        self.extension :str = track.file_extension
        self.count_of_audio_streams : int | None= int(track.count_of_audio_streams) if track.count_of_audio_streams else None 
        self.count_of_text_streams : int | None = int(track.count_of_text_streams) if track.count_of_text_streams else None
        self.count_of_video_streams : int = int(track.count_of_video_streams)
        self.duration : int = int(track.duration)
        self.frame_rate : float = float(track.frame_rate)

    def _log(self, string) -> None :
        print(f"VideoObject : {string}")
    
    def getJSON(self) -> str: 
        return self.mediaObject.to_data()
 
def wait () :
    pass
if __name__ == "__main__" :
    media = "/mnt/media/Movies/English/Soul (2020)/Soul.mkv"
    mediaInfo = Media(media)
    pprint(mediaInfo.__dict__)
    # pprint(mediaInfo.getJSON())
