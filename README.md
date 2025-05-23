# MCI-lab

# Setup ENV

```
python3 -m venv venv
source venv/bin/activate
pip install pandas
```

# SSH - Remote access pi4

```
ssh pi4@192.168.88.253
```

## Navigate to targer directory

```
cd Desktop/day1
```

## Start script via SSH

```
#Run script
python3 bigboy.py

#Run script in background
nohup python3 bigboy.py > out.log 2>&1 & disown
```

# Verify if script is running in the background

```
ps -C python3 -o pid,etime,cmd | grep bigboy.py
```

# Stop script

```
pkill -f bigboy.py
```

# Upload script to pi4

```
rsync -avz ./bigboy.py pi4@192.168.88.253:~/Desktop/day1/

rsync -avz ./mqtt.py pi4@192.168.88.253:~/Desktop/day3/
```

# Copy data results to local machine

```
rsync -avz --ignore-existing pi4@192.168.88.253:~/Desktop/day1/collectedData/ ./collectedData/
```

# Combine collected data into 1 dataset

```
python3 combineData.py

```

## Node-RED

# Start node-red TBC

# Access node-red

# Open browser

Admin panel :http://192.168.88.253:1880/

Final UI http://192.168.88.253:1880/ui
