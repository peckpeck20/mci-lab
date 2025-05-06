from sense_hat import SenseHat
from datetime import datetime
from time import sleep

sh = SenseHat()

# Adjustments for SensorHat v2
sh.color.gain = 60
sh.color.integration_cycles = 64

def display_warning(message, color):
    # Display a scrolling message on the LED matrix
    sh.show_message(message, text_colour=color)

def fetch_data():
        # display_warning("Hello Big BoI :D",(0, 255, 255))
        temperature = sh.get_temperature()
        pressure = sh.get_pressure()
        humidity = sh.get_humidity()
        red, green, blue, clear = sh.colour.colour
        orientation = sh.get_orientation()
        compass = sh.get_compass_raw()
        acceleration = sh.get_accelerometer_raw()
        gyro = sh.get_gyroscope_raw()

        return [temperature, pressure, humidity, \
                acceleration["x"], acceleration["y"], \
                acceleration["z"], orientation["yaw"], \
                orientation["pitch"], orientation["roll"], \
                compass["x"], compass["y"], compass["z"], \
                gyro["x"], gyro["y"], gyro["z"], \
                red, green, blue, clear]


if __name__ == "__main__":

        with open("data.csv", "w") as out_file:
                out_file.write("temperature,pressure,humidity,acc_x,acc_y,acc_z,orientation_yaw,orientation_pitch,orientation_roll,compass_x,compass_y,compass_z,gyro_x,gyro_y,gyro_z,red,green,blue,clear\n")

        with open("data.csv", "a") as out_file:
                while True:
                        data = fetch_data()
                        data = [str(value) for value in data]
                        data_string = ",".join(data)+"\n"
                        out_file.write(data_string)
                        sleep(2)
        print("finised")