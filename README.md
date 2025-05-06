# MCI-lab

# SSH - Remote access pi4

```
ssh pi4@192.168.88.253
```

## Navigate to targer directory

```
cd Desktop/day1
```

## Run script

```
python3 bigboy.py
```

# Upload script to pi4

```
rsync -avz ./bigboy.py pi4@192.168.88.253:~/Desktop/day1/
```

# Copy data results to local machine

```
scp pi4@192.168.88.253:~/Desktop/day1/data.csv ./

```

## Node-RED

# Start node-red TBC

# Access node-red

# Open browser

Admin panel :http://192.168.88.253:1880/

Final UI http://192.168.88.253:1880/ui
