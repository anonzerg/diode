# diode
program to find boltzmann's constant and planck's constant using arduino board.

# usage:

first create a python virtual environment:
```
python -m venv /path/to/new/virtual/environment
cd /path/to/new/virtual/environment
```
activate virtual environment on **Windows**:
```
Scripts\activate
```
on **Linux**:
```
source ./bin/activate
```
clone repo into virtual environment:
```
git clone https://github.com/anonzerg/diode.git
```
install required libraries:
```
pip install -r requirments.txt
```
connect your board to you pc using USB. read manual and connect diode and data pins according to images blow.
![circuit](/circuit.png)
launch arduino program and upload main.ino located at ./diode/main.ino
move to project directory and run program:
```
cd ./diode
python ./run.py
```

