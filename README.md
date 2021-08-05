# Ping-to-Graph

Python script that opens output file from ping tool from windows

After data is loaded graphs are created and drawn 

It can be used to see anomalies in LAN network between PC and Router

Or it can show if there is any ping spikes between Your PC and Server/Site

Command to run in cmd

```ping google.com -n 350 > ping.txt```

```-n 350``` - "-n" means number of packets that will be sent for pinging (ie. -n 400)

```-t``` - "-t" means continous pinging of site exiting with CTRL+C

After its done place ping.txt in same folder as main.py

Just run *main.py* and two graphs will be created 
