# :chart_with_downwards_trend: Ping-to-Graph :chart_with_upwards_trend:

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


Requierments: 
```numpy==1.21.1```
```matplotlib==3.4.2```


![Example](https://i.ibb.co/BtXfC0w/Screenshot-2021-08-06-082521.jpg)
