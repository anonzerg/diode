# diode
program to find boltzmann's and planck's constant from diode and LED with Arduino board.

# usage:

first clone repo and `cd` into it:
```
$ git clone https://github.com/anonzerg/diode.git
$ cd diode
```
then create a python virtual environment:  
pay attention to `python3` when you want to create a virtual environment.  
after activating, you can just use `python`.  
on **Linux**:
```
$ python3 -m venv .venv
```
on **Windows**:
```
PS> python -m venv .venv
```
activate virtual environment on **Windows**:
```
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
PS> .venv\Scripts\activate
```
on **Linux** with bash or zsh:
```
$ source <venv>/bin/activate
```
install required libraries:
```
$ pip install -r requirments.txt
```
connect your board to you pc using USB.  
read manual and connect diode and data pins according to images blow.

![circuit](/complementary_materials/circuit.png)

launch arduino program and upload main.ino located at ./diode/main.ino  
finally run program:
```
$ python ./run.py
```

