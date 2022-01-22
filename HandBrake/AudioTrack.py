

class AudioTrack:
    def __init__(self,trackId:int,  track:any) -> None:
        self.id = trackId
        self.channels :int  = int(track.channel_s)
        self.default : bool = True if track.default == 'Yes' else False
        self.title : str = track.title
        self.langauge : str = track.language

    def __repr__(self) -> str:
        return "Audio Track \n\t"+"\n\t".join([f"{k}: {v}" for k, v in self.__dict__.items()])
        