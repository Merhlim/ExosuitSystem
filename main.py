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

        with open("authentication.json", "r") as authfile:
            self.auth = json.loads(authfile.read())

        sleep(2)

        self.authenticate("Enter password")

    def bootup(self):
        self.cad.lcd.clear()
        self.cad.lcd.blink_off()
        self.cad.lcd.backlight_on()
        self.cad.lcd.write("ExosuitOS V.PreA")
        self.cad.lcd.set_cursor(0,1)
        self.cad.lcd.write("Booting")
        self.cad.lcd.set_cursor(0,0)

    def authenticate(self, prompt):
        self.cad.lcd.clear()
        self.cad.lcd.write("Enter password")
        self.cad.lcd.set_cursor(0,1)
        password = ""

        while True:
            if self.cad.switches[0] == 1:
                password = password + "1"
                self.cad.lcd.write("*")

            elif self.cad.switches[1] == 1:
                password = password + "2"
                self.cad.lcd.write("*")

            elif self.cad.switches[2] == 1:
                password = password + "3"
                self.cad.lcd.write("*")

            elif self.cad.switches[3] == 1:
                password = password + "4"
                self.cad.lcd.write("*")

            elif self.cad.switches[4] == 1:
                break

            else:
                continue

        md5hash = hashlib.md5(password.encode("utf-8")).hexdigest()

        for user in self.auth["Authentication"]:
            if user["password"] == md5hash:
                self.user = user["username"]
                self.userpassword = user["password"]
                self.cad.lcd.clear()
                self.cad.lcd.set_cursor(0,0)
                self.cad.lcd.write("Welcome back")
                self.cad.lcd.set_cursor(0,1)
                self.cad.lcd.write(self.user)
                sleep(2)


if __name__ == "__main__":
    main()