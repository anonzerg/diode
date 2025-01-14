# diode
program to find boltzmann's and planck's constant from diode and LED with Arduino board.

# usage:

first create a python virtual environment:  
replace /path/to/new/virtual/environment with whatever you want.  
on **Linux**:
```
python3 -m venv /path/to/new/virtual/environment
```
on **Windows**:
```
python -m venv C:\path\to\new\virtual\environment
```
activate virtual environment on **Windows**:
```
Scripts\activate
```
on **Linux** with bash or zsh:
```
source <venv>/bin/activate
```
clone repo into virtual environment:
```
git clone https://github.com/anonzerg/diode.git
```
install required libraries:
```
pip install -r requirments.txt
```
connect your board to you pc using USB.  
read manual and connect diode and data pins according to images blow.

![circuit](/circuit.png)

launch arduino program and upload main.ino located at ./diode/main.ino  
move to project directory and run program:
```
cd ./diode
python ./run.py
```

