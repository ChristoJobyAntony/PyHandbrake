from time import sleep
from CLI.app import runApp

runApp()

# from HandBrake.Command import Command
# from HandBrake.Media import Media
# from HandBrake.ProcessHandler import ProcessHandler

# command1 = Command(media=Media("/mnt/media/Movies/English/Dune (2021)/Dune (2021).mp4"))
# command2 = Command(media=Media("/mnt/media/Movies/English/Dune (2021)/Dune (2021).mp4"))
# p = ProcessHandler()
# p.addProcess(command1)
# p.addProcess(command2)
# p.run()
# # print(p.isRunning.value())
# while True : 
#     # input()
#     sleep(1)
#     # print("Job Queue: ", p.getQueuedProcess() )
#     if (p.getCurrentProcess()) : print(p.getStats())
