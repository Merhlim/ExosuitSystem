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

    def get_my_ip():
        return main.run_cmd(main.GET_IP_CMD)[:-1]

    def get_my_temp():
        return main.run_cmd(main.GET_TEMP_CMD)[5:9]

    def get_my_free_mem():
        total_mem = float(main.run_cmd(main.TOTAL_MEM_CMD))
        used_mem = float(main.run_cmd(main.USED_MEM_CMD))
        mem_perc = used_mem / total_mem
        return "{:.1%}".format(mem_perc)

    def wait_for_ip():
        main.ip = ""
        while len(main.ip) <= 0:
            sleep(1)
            main.ip = main.get_my_ip()
            if main.cad.switches[4].value == 1:
                main.ip = None

    def show_sysinfo():
        while True:
            main.cad.lcd.clear()
            main.cad.lcd.write("IP:{}\n".format(main.get_my_ip()))

            main.cad.lcd.write_custom_bitmap(main.temp_symbol_index)
            main.cad.lcd.write(":{}C ".format(main.get_my_temp()))

            main.cad.lcd.write_custom_bitmap(main.memory_symbol_index)
            main.cad.lcd.write(":{}".format(main.get_my_free_mem()))
            main.sleep(main.UPDATE_INTERVAL)
            if main.cad.switches[4].value == 1:
                main.cad.lcd.clear()
                break

    def start():
        main.cad.lcd.clear()
        main.cad.lcd.blink_off()
        main.cad.lcd.cursor_off()
        main.cad.lcd.store_custom_bitmap(main.temp_symbol_index, main.temperature_symbol)
        main.cad.lcd.store_custom_bitmap(main.memory_symbol_index, main.memory_symbol)
        main.cad.lcd.backlight_on()
        main.cad.lcd.write("Waiting for IP..")
        main.cad.lcd.set_cursor(0,1)
        main.cad.lcd.write("Button 4 to exit")
        main.wait_for_ip()
        if main.ip != None:
            main.show_sysinfo()
