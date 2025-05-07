# MCI-lab

# SSH - Remote access pi4

```
ssh pi4@192.168.88.253
```

## Navigate to targer directory

```
cd Desktop/day1
```

## Run script locally

## Start script via SSH

```
#Run script
python3 bigboy.py

#Run script in background
nohup python3 bigboy.py > out.log 2>&1 & disown
```

# View background script

```
ps -C python3 -o pid,etime,cmd | grep bigboy.py
```

# Upload script to pi4

```
rsync -avz ./bigboy.py pi4@192.168.88.253:~/Desktop/day1/

rsync -avz ./mqtt.py pi4@192.168.88.253:~/Desktop/day3/
```

# Copy data results to local machine

```
scp pi4@192.168.88.253:~/Desktop/day1/data.csv ./

#Copy all
scp -r pi4@192.168.88.253:~/Desktop/day1/collectedData/ ./collectedData
```

## Node-RED

# Start node-red TBC

# Access node-red

# Open browser

Admin panel :http://192.168.88.253:1880/

Final UI http://192.168.88.253:1880/ui
