import sys
import subprocess
from time import sleep
import pifacecad

UPDATE_PERIOD = 5
GET_IP_CMD = "hostname --all-ip-addresses | awk '{print $1}'"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep 'Mem' | awk '{print $3}'"

cad = pifacecad.PiFaceCAD()

temperature_symbol = pifacecad.LCDBitmap(
    [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
memory_symbol = pifacecad.LCDBitmap(
    [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
temp_symbol_index, memory_symbol_index = 0, 1


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]


def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]


def get_my_free_mem():
    total_mem = run_cmd(TOTAL_MEM_CMD)
    total_mem = float(total_mem)
    used_mem = run_cmd(USED_MEM_CMD)
    used_mem = float(used_mem)
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)


def wait_for_ip():
    ip = ""
    while len(ip) <= 0:
        sleep(1)
        ip = get_my_ip()
        if cad.switches[4].value == 1:
            return None
    return ip


def show_sysinfo():
    tick = 0.0
    while True:
        if tick == 5.0:
            cad.lcd.clear()
            cad.lcd.set_cursor(0, 0)
            cad.lcd.write("IP:" + get_my_ip())
            cad.lcd.set_cursor(0, 1)
            cad.lcd.write_custom_bitmap(temp_symbol_index)
            cad.lcd.write(":" + str(get_my_temp()) + "C ")

            cad.lcd.write_custom_bitmap(memory_symbol_index)
            cad.lcd.write(":" + get_my_free_mem())
            tick = 0.0

        if cad.switches[4].value == 1:
            cad.lcd.clear()
            break

        sleep(0.5)
        tick = tick + 0.5


def start():
    cad.lcd.clear()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.store_custom_bitmap(temp_symbol_index, temperature_symbol)
    cad.lcd.store_custom_bitmap(memory_symbol_index, memory_symbol)
    cad.lcd.backlight_on()
    cad.lcd.write("Waiting for IP..")
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write("Button 4 to exit")
    ip = wait_for_ip()
    if ip != None:
        show_sysinfo()
