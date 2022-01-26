import os
from multiprocessing import Queue
from threading import Thread
from typing import List
from HandBrake.Command import Command 
from HandBrake.Media import Media
from CLI.Menu import Menu
from pprint import pprint
from HandBrake.ProcessHandler import ProcessHandler

p = ProcessHandler()


def configureMedia(file:str) :
    media = Media(file)
    command = Command(media)
    
    setAudioTracksAction = lambda track : command.audio.add(track)
    setSubtitleAction = lambda track :  command.subtitle.add(track)
    setEncoderAction = lambda enc : command.setEncoder(enc)
    setResolutionAction = lambda res : command.setResolution(res)
    setAudioTracks = Menu("Choose Subtitle to add", [(track.title, setAudioTracksAction, [track]) for track in media.audioTracks], runUntilExit=False )
    setSubtitleTracks = Menu("Choose Subtitle to add", [(track.title, setSubtitleAction, [track]) for track in media.textTrack], runUntilExit=False )
    setEncodingEngine = Menu(  "Choose Encoding Engine", [ (enc, setEncoderAction , [enc]) for enc in Command.ENCODERS ], runUntilExit=False)
    setResolution = Menu("Resolution", [ (res, setResolutionAction, [res]) for res in command.RESOLUTIONS], runUntilExit=False)

    encodingConfigMenu = Menu("Configure Encoder")
    encodingConfigMenu.addMenu("View Configuration", pprint, args=[command])
    encodingConfigMenu.addMenu("Subtitles Tracks", setSubtitleTracks.run)
    encodingConfigMenu.addMenu("Audio Tracks", setAudioTracks.run) 
    encodingConfigMenu.addMenu("Encoding Engine", setEncodingEngine.run)
    encodingConfigMenu.addMenu("Resolution", setResolution.run)

    mediaInfoMenu = Menu("Media Info")
    mediaInfoMenu.addMenu("View General Info", lambda : pprint(media))
    mediaInfoMenu.addMenu("View Video Track Info", lambda : pprint(media.videoTracks))
    mediaInfoMenu.addMenu("View Audio Track Info", lambda : pprint(media.audioTracks))
    mediaInfoMenu.addMenu("View Subtitle Info", lambda : pprint(media.textTrack))

    addItemToQueue = Menu("Add a new Job, Media : "+os.path.basename(file))
    addItemToQueue.addMenu("View Media Info", mediaInfoMenu.run)
    addItemToQueue.addMenu("View Encoding Configuration", encodingConfigMenu.run)
    addItemToQueue.addMenu("Add to queue", addItemToJobQueue, args=[command])

    addItemToQueue.run()

def ViewCurrentJob () :
    currentJob = p.getCurrentProcess()
    if not currentJob: print ("\n The current Job queue is empty add a new encoding job.")
    else : 
        print(f"The current running job is encoding file {currentJob.input} to {currentJob.output}")
        stat = p.getStats()
        if not stat is None  : 
            print(f"The progress of the job is : {stat[0]}% at an average {stat[1]} FPS and ETA {stat[2]}")

def viewJobQueue () :
    q = p.getQueuedProcess()
    if not len(q) :
        print("The Job Queue is empty !!")
    else :
        for i, job in enumerate(list(q)) : 
            print(i,job.input)

def viewCompletedJobQueue () : 
    q = p.getcompletedProcess()
    if not len(q) :
        print("No jobs yet completed !!")
    else :
        for i, job in enumerate(list(q)) : 
            print(i,job.input)
    
def addItemToJobQueue (command : Command) :
    p.addProcess(command)
    print("**Media has been queued for transcoding !**\n")

def chooseMedia (base:str="/mnt/media/Movies/") :
    m = Menu("Choose Media Direcotry :"+base, runUntilExit=False)
    if not base == "/" :
        m.addMenu("<--- Up a Folder", chooseMedia, args =[os.path.dirname(base)] )
    for file in os.listdir(base) :
        path = os.path.join(base, file)
        if os.path.isdir(path) :
            m.addMenu(file, chooseMedia, args=[path])
        elif os.path.isfile(path) :
            m.addMenu(file, configureMedia, args = [path])
    m.run()

handBrakeManager = Menu("HandBrakeManager")
handBrakeManager.addMenu("View the Current Encoding Proccess", ViewCurrentJob)
handBrakeManager.addMenu("View the job queue", viewJobQueue)
handBrakeManager.addMenu("View the completed job queue", viewCompletedJobQueue)
handBrakeManager.addMenu("Select media to add to queue", chooseMedia)

def runApp():
    p.run()
    handBrakeManager.run()  
    p.stop()