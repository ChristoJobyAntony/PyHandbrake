class TextTrack : 
    def __init__(self, trackId:int, track) -> None:
        self.id = trackId
        self.title = track.title
        self.language = track.language
        self.default = True if track.default == 'Yes' else False
    
    def __repr__(self) -> str:
         return "Subtitle Track \n\t"+"\n\t".join([f"{k}: {v}" for k, v in self.__dict__.items()])