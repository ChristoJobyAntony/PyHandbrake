# PyHandBrake

## Preface
### Note
This is a not an alterative to HandBrakeCLI application rather an library to abstract HandbrakeCLI with python and thus requires the installation of the application. 
<br><br>
The aim of this project is to abstract HandbrakeCLI and to handle the application programmatically using python. Thus allowing to automate transcoding tasks or handle them through web interfaces.
<br><br>
Currently this project includes a basic CLI application to configure and queue transcoding tasks to HandBrakeCLI through a simple Menu Interface.
<br>

## Prerequisites
While this application is in theory multi-platform it is still require some critical dependencies.
1. HandBrakeCLI - This app needs the HandbrakeCLI command line application installed and isn't bundled with the this app.
   
2. PyMediaInfo - To parse media and their properties we will use a python library that is wrapper for the MediaInfo library.

## An Overview

This application usually works in three layers : 
1. ### The HandbrakeCLI subprocess. 
   Spawned using the python subprocess module this is where the actual transcoding takes place and the encoding stats are piped to the listener process.

2. ### The Listener Process : 
   This is an intermediate layer between the main process and the HandbrakeCLI layer, it handles the incoming jobs, spawns them and extracts the realtime encoding stats form from the STDOUT pipe.

3. ### The Main Process : 
   This is where you can run any of the programming logic of your desire be it a command line interface or a web application.
   




