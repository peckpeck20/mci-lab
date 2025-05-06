from sense_hat import SenseHat
from datetime import datetime
from time import sleep

sh = SenseHat()

# Adjustments for SensorHat v2
sh.color.gain = 60
sh.color.integration_cycles = 64

def get_board_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            return float(temp_str) / 1000.0
    except:
        return 0.0  # Return 0 if the temperature can't be read

def fetch_data():
    room_temperature = sh.get_temperature()
    board_temp = get_board_temperature()
    pressure = sh.get_pressure()
    humidity = sh.get_humidity()
    orientation = sh.get_orientation()
    compass = sh.get_compass_raw()
    acceleration = sh.get_accelerometer_raw()
    gyro = sh.get_gyroscope_raw()

    return [
        room_temperature, board_temp, pressure, humidity,
        acceleration["x"], acceleration["y"], acceleration["z"],
        orientation["yaw"], orientation["pitch"], orientation["roll"],
        compass["x"], compass["y"], compass["z"],
        gyro["x"], gyro["y"], gyro["z"]
    ]

if __name__ == "__main__":
    print("Running")

    with open("data.csv", "w") as out_file:
        out_file.write("timestamp,room_temperature,board_temp,pressure,humidity,"
                       "acc_x,acc_y,acc_z,orientation_yaw,orientation_pitch,orientation_roll,"
                       "compass_x,compass_y,compass_z,gyro_x,gyro_y,gyro_z\n")

    with open("data.csv", "a") as out_file:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = fetch_data()
            data.insert(0, timestamp)
            data_string = ",".join(map(str, data)) + "\n"
            out_file.write(data_string)
            sleep(1)
