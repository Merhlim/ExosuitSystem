import pifacecad
import hashlib
import os
import json
from time import sleep

class main:

    cad = pifacecad.PiFaceCAD()


    def __init__(self):
        self.cad.init_board()
        self.bootup()
        self.scan_data_files()
        sleep(2)

        if self.authenticate("Enter password") == False:
            self.reset_cad_display()
            self.cad.lcd.write("Access Denied")
            #os.system("reboot")
            exit()

        self.run_module("sysinfo")

    def scan_data_files(self):
        with open("authentication.json", "r") as authfile:
            self.auth = json.loads(authfile.read())
        with open("data.json","r") as datafile:
            self.data = json.loads(datafile.read())

    def run_module(self,modulename):
        module = __import__("modules."+modulename)
        module.main.start()
        self.reset_cad_display()

    def reset_cad_display(self):
        self.cad.lcd.clear()
        self.cad.lcd.blink_off()
        self.cad.lcd.backlight_on()
        self.cad.lcd.set_cursor(0, 0)

    def bootup(self):
        self.reset_cad_display()
        self.cad.lcd.write("ExosuitOS V.PreA")
        self.cad.lcd.set_cursor(0,1)
        self.cad.lcd.write("Booting")
        self.cad.lcd.set_cursor(0,0)

    def authenticate(self, prompt):
        self.reset_cad_display()
        self.cad.lcd.write("Enter password")
        self.cad.lcd.set_cursor(0,1)
        password = ""

        while True:
            if self.cad.switches[0].value == 1:
                password = password + "1"
                self.cad.lcd.write("*")
                sleep(0.2)

            elif self.cad.switches[1].value == 1:
                password = password + "2"
                self.cad.lcd.write("*")
                sleep(0.2)

            elif self.cad.switches[2].value == 1:
                password = password + "3"
                self.cad.lcd.write("*")
                sleep(0.2)

            elif self.cad.switches[3].value == 1:
                password = password + "4"
                self.cad.lcd.write("*")
                sleep(0.2)

            elif self.cad.switches[4].value == 1:
                break

            else:
                continue

        md5hash = hashlib.md5(password.encode("utf-8")).hexdigest()

        for user in self.auth["Authentication"]:
            if user["password"] == md5hash:
                self.user = user["username"]
                self.userpassword = user["password"]
                self.reset_cad_display()
                self.cad.lcd.write("Welcome back")
                self.cad.lcd.set_cursor(0,1)
                self.cad.lcd.write(self.user)
                sleep(2)
                return True
        return False


if __name__ == "__main__":
    main()