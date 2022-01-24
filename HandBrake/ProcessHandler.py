from  multiprocessing import Queue, Value, Array, Process
import queue as q
import subprocess as sp
import re
from typing import List, Tuple
from HandBrake.Command import Command
from HandBrake.Media import Media

class ProcessHandler : 

    def __init__(self) -> None:
        # These are queues with string data to communicate with the listener process
        self._commandQueue : Queue = Queue()
        self._completedCommandQueue : Queue = Queue()
        # These are list that are updated based on the queue for UI
        self.processList : List[Command] = list()
        self.completedProcessList : List[Command] = list()
        self.currentProccess : Command = None
        # This is a shared memory variable to check if a command is running
        self.isRunning : Value = Value("b", lock=True)
        self.isRunning.value = 0
        # This will signal the end of the process even if there are pending jobs
        self.endSig : Value = Value("b")
        self.endSig.value = 0
        # Current Encoding process stats
        self.FPS : Value = Value("f", lock=True)
        self.ETA : Array = Array("u", 9, lock=True)
        self.percent : Value = Value("f", lock=True)
    
    def addProcess(self, command : Command) :
        self._commandQueue.put_nowait(command.buildCommnad())
        self.processList.append(command)
    
    def stop(self) : 
        with self.endSig.get_lock() : self.endSig.value = 1
        self._commandQueue.close()

    def updateProcess(self) : 
        while not self._completedCommandQueue.empty() : 
            p = self._commandQueue.get()
            if p == self.processList[0].buildCommnad() : 
                self.completedProcessList(self.processList.pop(0))
            else : 
                print("Error !!", p, self.processList[0])

    def getcompletedProcess(self) -> List[Command]: 
        self.updateProcess()
        return self.completedProcessList

    def getQueuedProcess(self) -> List[Command]: 
        self.updateProcess()
        return self.processList
    
    def getCurrentProcess(self) -> List[Command] | None:
        if not self.isRunning.value : return None
        self.updateProcess() 
        return self.processList[0]
    
    def getStats (self) -> Tuple[float, float, str] : 
        with self.ETA.get_lock(), self.FPS.get_lock(), self.percent.get_lock() :
            return(self.percent.value, self.FPS.value, self.ETA[0:9])
    
    def listener(proccessQueue : Queue, completedProccess : Queue, endSig:Value, percent:Value, ETA:Array, FPS:Value, isRunning:Value ) -> None:
        # print("Listener Starting")
        
        while (endSig.value == 0) :
            # print("Loop started")
            # Try to get a job from the queue every one second
            try : command : str = proccessQueue.get(block=True, timeout=1)
            except q.Empty : continue
            print("Starting Job : "+command)
            process = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            with isRunning.get_lock() : isRunning.value = True
            line = ""
            while (process.poll() is None) :
                c : bytes = process.stdout.read(1)
                if c.hex() == "0d" :
                    # print(line)
                    matches = re.match(r'.*(\d+\.\d+)\s%.*ETA\s(\d+)h(\d+)m(\d+)s\)', line)
                    if matches :
                        m = matches.group().split(' ')
                        with percent.get_lock() : percent.value = float(m[5])
                        with FPS.get_lock() : FPS.value = float(m[10])
                        with ETA.get_lock() : ETA[0:9] =  m[13][0:9]
                    line = ""                        
                else : 
                    line += c.decode("utf-8")
            else : 
                print("OUt I go ...")
                with isRunning.get_lock() : isRunning.value = False
                proccessQueue.task_done()
                completedProccess.put_nowait(command)
     
    def run (self) :
        self.process = Process(target=ProcessHandler.listener, args=(self._commandQueue, self._completedCommandQueue, self.endSig, self.percent, self.ETA, self.FPS, self.isRunning)).start()



