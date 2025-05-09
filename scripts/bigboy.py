import csv, logging, os, signal, sys
from datetime import datetime, timedelta
from time import sleep
from sense_hat import SenseHat

# ─── Settings ────────────────────────────────────────────────────────────────
ROTATE_EVERY  = timedelta(minutes=30)   # change to timedelta(minutes=10) etc.
SAMPLE_PERIOD = 1                    # seconds between readings
LOG_DIR  = "logs"
DATA_DIR = "collectedData"
# ─────────────────────────────────────────────────────────────────────────────

sh = SenseHat()
sh.color.gain, sh.color.integration_cycles = 60, 64   # v2 tweaks

os.makedirs(LOG_DIR,  exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "logger.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def get_board_temp() -> float:
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read()) / 1000.0
    except Exception:
        logging.exception("Reading board temperature failed")
        return 0.0

def grab_row():
    try:
        o   = sh.get_orientation()
        acc = sh.get_accelerometer_raw()
        cmp = sh.get_compass_raw()
        gyr = sh.get_gyroscope_raw()
        return (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sh.get_temperature(),               # room
            get_board_temp(),                   # CPU
            sh.get_pressure(),
            sh.get_humidity(),
            acc["x"], acc["y"], acc["z"],
            o["yaw"], o["pitch"], o["roll"],
            cmp["x"], cmp["y"], cmp["z"],
            gyr["x"], gyr["y"], gyr["z"],
        )
    except Exception:
        logging.exception("Sensor read failed")
        return None

HEADER = (
    "timestamp,room_temp,board_temp,pressure,humidity,"
    "acc_x,acc_y,acc_z,yaw,pitch,roll,"
    "comp_x,comp_y,comp_z,gyro_x,gyro_y,gyro_z"
).split(",")

def new_csv():
    fn = datetime.now().strftime("data_%Y%m%d_%H%M%S.csv")
    fp = open(os.path.join(DATA_DIR, fn), "w", newline="")
    w  = csv.writer(fp)
    w.writerow(HEADER)
    logging.info("Started file %s", fn)
    return fp, w, datetime.now()

running = True
for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda *_: globals().__setitem__('running', False))

f, writer, opened = new_csv()
rows = 0

try:
    while running:
        if datetime.now() - opened >= ROTATE_EVERY:
            f.close()
            f, writer, opened = new_csv()
            rows = 0

        row = grab_row()
        if row:
            writer.writerow(row)
            rows += 1
            if rows % 60 == 0:        # flush once a minute
                f.flush()
        sleep(SAMPLE_PERIOD)
finally:
    f.close()
    logging.info("Logger stopped")
