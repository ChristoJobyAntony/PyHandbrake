import re
from subprocess import Popen
import subprocess
import threading
from time import sleep
from typing import Dict, List,  Tuple, Set
import os

from HandBrake.AudioTrack import AudioTrack
from HandBrake.Media import Media
from HandBrake.TextTrack import TextTrack

class HandBrakeCLI : 
    COMMAND = "/usr/bin/HandBrakeCLI"
    ENCODERS :Tuple[str]= ("x264", "x264_10bit", "nvenc_h264", "x265", "x265_10bit", "x265_12bit", "nvenc_h265", "mpeg4", "mpeg2") 
    RESOLUTIONS :Tuple [int] =  [720, 1080, 1440, 2160]

    def __init__(self, media:Media, outFile:str="Encoded") -> None:

        self.proccess : Popen = None
        self.percent : float = None
        self.avgFPS : float = None
        self.ETA : str = None

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
        configurations = {
            "--verbose" : self.verbose,
            "--input" : self._formatPath(self.input),
            "--output" : self._formatPath(self.output),
            "--format" : self.format,
            "--encoder" : self.encoder,
            "--quality" : self.quality,
            "--audio" : self.audio,
            "--subtitle" : self.subtitle,
            "--width" : self.media.width,
            "--height" : self.media.height
        } 
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
    
    def buildFlags (self) -> List[str] :
        configurations = {
            "--verbose" : self.verbose,
            "--input" : self._formatPath(self.input),
            "--output" : self._formatPath(self.output),
            "--format" : self.format,
            "--encoder" : self.encoder,
            "--quality" : self.quality,
            "--audio" : self.audio,
            "--subtitle" : self.subtitle,
            "--width" : self.media.width,
            "--height" : self.media.height
        } 
        os.path.splitdrive
        flags = []
        for flag, value in configurations.items() :
            if value == None : 
                continue 
            elif type(value) == set : 
                value = ", ".join(map(lambda x : str(x.id), value))
            elif type(value) != str :
                value = str(value)
            flags.append(flag)
            flags.append(value)
        return flags

    def isRunning (self) -> bool :
        if self.proccess : 
            return True if self.proccess.poll() is None  else False
        return False

    def listener(self, buffer=1) -> None :
        if self.proccess :
            line = ""
            while (True) :
                c : bytes = self.proccess.stdout.read(1)
                if c.hex() == "0d" :
                    # print(line)
                    matches = re.match(r'.*(\d+\.\d+)\s%.*ETA\s(\d+)h(\d+)m(\d+)s\)', line)
                    if matches :
                        m = matches.group().split(' ')
                        self.percent = float(m[5])
                        self.avgFPS = float(m[10])
                        self.ETA = m[13]
                    line = ""                        
                else : 
                    line += c.decode("utf-8")
        print("Listener Exiting", self.isRunning())
 
    def run(self) -> None:
        # args = [self.COMMAND] + self.buildFlags()
        self.proccess = Popen(self.buildCommnad(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self.listener).start()
 

if __name__ == "__main__" :
    media = Media("/mnt/media/Movies/English/Snatch (2000)/Snatch.mp4")
    command = HandBrakeCLI(media)
    print(command.buildCommnad())
    command.run()
    while (command.isRunning()) :
        print("Running ...")
        if command.ETA and command.percent and command.avgFPS :
            print(f"Completion : {command.percent}% Processing at {command.avgFPS} ETA {command.ETA}")
        sleep(1)



