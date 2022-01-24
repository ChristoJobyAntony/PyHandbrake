from concurrent.futures import process
import multiprocessing as mp
from subprocess import Popen
from time import sleep
from typing import Dict, List,  Tuple, Set
import os

from HandBrake.AudioTrack import AudioTrack
from HandBrake.Media import Media
from HandBrake.TextTrack import TextTrack

class Command : 
    COMMAND = "/usr/bin/HandBrakeCLI"
    ENCODERS :Tuple[str]= ("x264", "x264_10bit", "nvenc_h264", "x265", "x265_10bit", "x265_12bit", "nvenc_h265", "mpeg4", "mpeg2") 
    RESOLUTIONS :Tuple [int] =  [720, 1080, 1440, 2160]

    def __init__(self, media:Media, outFile:str="Encoded") -> None:

        self.proccess : Popen = None
        self.percent : float = mp.Value("f", lock=True)
        self.avgFPS : float = mp.Value("f" ,lock=True)
        self.ETA : str = mp.Array("u",9, lock=True)

        self.verbose : int = 1
        self.media = media
        self.width:set(int) = self.media.width
        self.height = self.media.height
        self.input = self.media.path
        self.output : str = os.path.join(os.path.dirname(self.input), outFile)+"."+self.media.extension
        self.format :str = "av_mp4"
        self.encoder : str = self.ENCODERS[3]
        self.quality : int = 22
        self.audio : Set[AudioTrack] = set()
        self.subtitle : Set[TextTrack] = set()

        self.config =  {
            "--verbose" : lambda : self.verbose,
            "--input" : lambda : self._formatPath(self.input),
            "--output" : lambda : self._formatPath(self.output),
            "--format" : lambda :  self.format,
            "--encoder" : lambda : self.encoder,
            "--quality" : lambda : self.quality,
            "--audio" : lambda : self.audio,
            "--subtitle" : lambda : self.subtitle,
            "--width" : lambda : self.width,
            "--height" : lambda : self.height
        }
    
    def __repr__(self) -> str:
        return "HandBrakeCLI Command \n\t" + "\n\t".join([f"{k} : {v()}" for k, v in self.config.items()])

    def setEncoder (self, enc:str) -> None : 
        if enc in self.ENCODERS : self.encoder = enc
        else : raise("Invalid Encoder being set")
    
    def setResolution (self, height:int, width:int=None) -> None:
        if width is None :
            ratio = self.media.width / self.media.height
            width = int(ratio * height)
            self.width = width
            self.height = height
            print(self.width, self.height)
        else : 
            self.width = width
            self.height = height
    
    def _formatPath (self, path : str) -> str : 
        quoteWhiteSpace = lambda x :  '"'+x+'"' if " " in x else x
        return os.sep + os.path.join(*map(quoteWhiteSpace, path.split(os.sep)))
    
    def buildCommnad (self) -> str : 
        os.path.splitdrive
        command = "HandBrakeCLI  "
        for flag, value in self.config.items() :
            value = value()
            if value == None : 
                continue 
            elif type(value) == set : 
                value = ", ".join(map(lambda x : str(x.id), value))
            elif type(value) != str :
                value = str(value)
            command += flag + " "+ value + " "
        return command 

if __name__ == "__main__" :
    media = Media("/mnt/media/Movies/English/Snatch (2000)/Snatch.mp4")
    command = Command(media)
    print(command.buildCommnad())
    command.run()
    while (command.isRunning()) :
        print("Running ...")
        if command.ETA and command.percent and command.avgFPS :
            print(f"Completion : {command.percent}% Processing at {command.avgFPS} ETA {command.ETA}")
        sleep(1)
