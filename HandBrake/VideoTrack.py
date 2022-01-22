class VideoTrack : 
    def __init__(self, trackId:int, track) -> None:
        self.id :int = trackId
        self.height : int = track.height
        self.width : int = track.width
        self.format : str = track.format
        self.bitDepth : int = track.bit_depth
    
    def __repr__(self) -> str:
        return  "Video Track \n\t"+"\n\t".join([f"{k}: {v}" for k, v in self.__dict__.items()])