#   Copyright [2018] [Marian Cingel]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# pip install pyserial
import serial
import time
import signal
import sys


class Time2Line(object):
    def __init__(self, serial):
        self._state = False
        self._serial = serial
        # preffer time_ns in python3.7
        self._time_fn = time.time_ns if hasattr(time, "time_ns") else time.time
        self._verbose = False
    @property
    def time_fn(self):
        return self._time_fn
    @time_fn.setter
    def time_fn(self, x):
        self._time_fn = time_fn
    @property
    def verbose(self):
        return self._verbose
    @verbose.setter
    def verbose(self, value):
        self._verbose = not not value
    def signal_handler(self, sig, frame):
        print("signal handled, wait ... ")
        self.stop()
    def stop(self):
        self._state = False
    def is_running(self):
        return self._state
    def capture(self, log_path):
        self._state = True
        with open(log_path, "w") as log_file:
            while (self.is_running()):
                line = self._serial.readline()
                if not line: continue
                start_time = self._time_fn()
                formatted = "{start_time} | {line}".format(
                    start_time=start_time,
                    line=line.decode("utf-8", errors='ignore') 
                )
                if (self._verbose):
                    print(formatted)
                log_file.write(formatted)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dummy benchmark tool that injects timestamp into every line of serial output")
    parser.add_argument("device", type=str, help="serial device in format '/dev/ttyUSB0' or 'COM5'")
    parser.add_argument("-b", "--baud", type=int, default=115200, help="baudrate, default 115200")
    parser.add_argument("-l", "--logfile", type=str, default="./capture_log.txt", help="log filename")
    parser.add_argument("-v", "--verbose", type=int, default="0", help="verbose/stdout mode")
    parser.add_argument("-t", "--read_t", type=int, default="1", help="read timeout [s], affects performance")
    args = parser.parse_args()

    print("Press CTRL + C to terminate and save log")

    # serial device/port instance
    serial_dev = serial.Serial()
    serial_dev.port = args.device
    serial_dev.baudrate = args.baud
    serial_dev.timeout = args.read_t
    serial_dev.open()

    # time2line instance
    time2line = Time2Line(serial_dev)
    time2line.verbose = args.verbose
    signal.signal(signal.SIGINT, time2line.signal_handler)
    time2line.capture(args.logfile)
    print("Captured in {logfile}".format(logfile=args.logfile))

