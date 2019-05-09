## Project name
pyrat - python remote acess tool - client app.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Using](#using)
* [Thanks](#thanks)

## General info
During business trip, IT-Helpdesk (from company that I am working for) helped me to install some software on my business laptop (I have no admin privleges).  
I wondered, how this is possible, that they still can connect to my PC, even if I was behind two NAT's.   
The port 80 was the key.

This tool was created for training purposes only, never was and will be used as unwanted software (there is no hidding, autostart of script etc).

Main goals for client:

* as less as possible imported libraries with keeping the same functionality as first idea,  
* short code,  
* keeping data encoded, during transfering via port 80,  
* make script 'persistent' - if some problems with connection will occur, script kill itself, and start automatically next instance,  
* unhidden work - this code won't be like malicious software; code was written only for training.

## Technologies
Code was written as a Python 3 code.

Code was tested on following platforms:
* Windows 8.1 (PL-PL) (x64) with Python 3.7.1
* Windows 8.1 (EN-US) (x64) with Python 3.6.4
* Windows 7 (PL-PL) (x64) with Python 3.6.6

Used libraries:
* certifi==2018.4.16
* chardet==3.0.4
* idna==2.7
* requests==2.19.1
* urllib3==1.23

## Setup

Script was designed for running as client on Windows platform.
To use, you will only need to install required libraries and set variable of remote server (client.py, line 47):

```
home_host = 'http://yourserverip:yourport/'
```

Of course, if you will test this app locally, you need to keep original value:

```
home_host = 'http://127.0.0.1:8000'
```

Remember, you will need to setup and run server first! Otherwise, client will be unusable.

## Using

To run:

```
python client.py
```

There is nothing more to do, commands for client will be delivered by remote server (https://github.com/mrachuta/pyrat_server)

## Thanks

Thanks to my girlfriend for her patience when I was coding.  
Special thanks for user *npocmaka (Vasil Arnaudov)* for screen capture tool:  
https://github.com/npocmaka/batch.scripts/blob/master/hybrids/.net/c/screenCapture.bat
