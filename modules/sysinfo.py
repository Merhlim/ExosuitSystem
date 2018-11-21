import sys
import subprocess
from time import sleep
import pifacecad

class main:

    UPDATE_INTERVAL = 60 * 5  # 5 mins
    GET_IP_CMD = "hostname --all-ip-addresses"
    GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
    TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
    USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"

    cad = pifacecad.PiFaceCAD()

    temperature_symbol = pifacecad.LCDBitmap(
        [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
    memory_symbol = pifacecad.LCDBitmap(
        [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
    temp_symbol_index, memory_symbol_index = 0, 1

    def run_cmd(cmd):
        return subprocess.check_output(cmd, shell=True).decode('utf-8')

    def get_my_ip(self):
        return self.run_cmd(self.GET_IP_CMD)[:-1]

    def get_my_temp(self):
        return self.run_cmd(self.GET_TEMP_CMD)[5:9]

    def get_my_free_mem(self):
        total_mem = float(self.run_cmd(self.TOTAL_MEM_CMD))
        used_mem = float(self.run_cmd(self.USED_MEM_CMD))
        mem_perc = used_mem / total_mem
        return "{:.1%}".format(mem_perc)

    def wait_for_ip(self):
        self.ip = ""
        while len(self.ip) <= 0:
            sleep(1)
            self.ip = self.get_my_ip()
            if self.cad.switches[4].value == 1:
                self.ip = None

    def show_sysinfo(self):
        while True:
            self.cad.lcd.clear()
            self.cad.lcd.write("IP:{}\n".format(self.get_my_ip()))

            self.cad.lcd.write_custom_bitmap(self.temp_symbol_index)
            self.cad.lcd.write(":{}C ".format(self.get_my_temp()))

            self.cad.lcd.write_custom_bitmap(self.memory_symbol_index)
            self.cad.lcd.write(":{}".format(self.get_my_free_mem()))
            self.sleep(self.UPDATE_INTERVAL)
            if self.cad.switches[4].value == 1:
                self.cad.lcd.clear()
                break

    def start(self):
        self.cad.lcd.clear()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()
        self.cad.lcd.store_custom_bitmap(self.temp_symbol_index, self.temperature_symbol)
        self.cad.lcd.store_custom_bitmap(self.memory_symbol_index, self.memory_symbol)
        self.cad.lcd.backlight_on()
        self.cad.lcd.write("Waiting for IP..")
        self.cad.lcd.set_cursor(0,1)
        self.cad.lcd.write("Button 4 to exit")
        self.wait_for_ip()
        if self.ip != None:
            self.show_sysinfo()
