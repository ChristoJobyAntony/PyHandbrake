import os
from queue import Queue
import threading
from typing import List
from HandBrake.HandBrakeCLI import HandBrakeCLI 
from HandBrake.Media import Media
from CLI.Menu import Menu
from pprint import pprint
# 0549971012
base = "/"
jobQueue : Queue[HandBrakeCLI] = Queue()
currentJob : HandBrakeCLI = None
running = True

def runJobs () :
    while (running) : 
        global currentJob
        job = jobQueue.get(block=True)
        if not job : 
            currentJob = None
            break
        print("Starting job :", job.input)
        job.run()
        currentJob = job
        while (currentJob.isRunning()) :
            pass
t = threading.Thread(target=runJobs)

def configureMedia(file:str) :
    media = Media(file)
    command = HandBrakeCLI(media)
    
    setAudioTracksAction = lambda track : command.audio.add(track)
    setSubtitleAction = lambda track :  command.subtitle.add(track)
    setEncoderAction = lambda enc : command.setEncoder(enc)
    setResolutionAction = lambda res : command.setResolution(res)
    setAudioTracks = Menu("Choose Subtitle to add", [(track.title, setAudioTracksAction, [track]) for track in media.audioTracks] )
    setSubtitleTracks = Menu("Choose Subtitle to add", [(track.title, setSubtitleAction, [track]) for track in media.textTrack] )
    setEncodingEngine = Menu(  "Choose Encoding Engine", [ (enc, setEncoderAction , [enc]) for enc in HandBrakeCLI.ENCODERS ])
    setResolution = Menu("Resolution", [ (res, setResolutionAction, [res]) for res in command.RESOLUTIONS])

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
    if currentJob == None:
        print ("\n The current Job queue is empty add a new encoding job.")
    else : 
        # if currentJob.isRunning() : 
        print(f"The current running job is encoding file {currentJob.input} to {currentJob.output}")
        if currentJob.percent and currentJob.avgFPS and currentJob.ETA : 
            print(f"The progress of the job is : {currentJob.percent}% at an averag {currentJob.avgFPS} FPS with an ETA {currentJob.ETA}")

def viewJobQueue () :
    if jobQueue.empty () :
        print("The Job Queue is empty !!")
    else :
        for i, job in enumerate(list(jobQueue.queue)) : 
            print(i,job.input)

def addItemToJobQueue (command : HandBrakeCLI) :
    print("**Media has been queued for transcoding !**\n")
    jobQueue.put_nowait(command)

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

def stopProgram () :
    global running
    if running or t.is_alive() : 
        running = False
        jobQueue.put_nowait(None)
        t.join()
        print("Program exited gracefully")
        quit()


handBrakeManager = Menu("HandBrakeManager")
handBrakeManager.addMenu("View the Current Encoding Proccess", ViewCurrentJob)
handBrakeManager.addMenu("View the job queue", viewJobQueue)
handBrakeManager.addMenu("Select media to add to queue", chooseMedia)
handBrakeManager.addMenu("Stop the program", stopProgram)

def runApp():
    t.start()
    handBrakeManager.run()
    stopProgram()