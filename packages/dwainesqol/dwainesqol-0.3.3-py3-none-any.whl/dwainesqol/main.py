class msgbox:

    def __init__(self, title, message,typeOfBox):
        self.message = message
        self.title = title
        self.typeOfBox = typeOfBox


        import ctypes 


        if typeOfBox == "MB_OK":
            typeOfBox = 0x0
        
        elif typeOfBox == "MB_OKCXL":
            typeOfBox = 0x01

        elif typeOfBox == "MB_YESNOCXL":
            typeOfBox = 0x03
        
        elif typeOfBox == "MB_YESNO":
            typeOfBox = 0x04

        elif typeOfBox == "MB_HELP":
            typeOfBox = 0x4000

        elif typeOfBox == "ICON_EXCLAIM":
            typeOfBox = 0x30

        elif typeOfBox == "ICON_INFO":
            typeOfBox = 0x40

        elif typeOfBox == "ICON_STOP":
            typeOfBox = 0x10

            
        ctypes.windll.user32.MessageBoxW(0,message,title,typeOfBox)


class clipbored:
    def __init__(self, text):
        self.text = text
        import os
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)

class bsod:
    def __init__(self):
        from ctypes import windll
        from ctypes import c_int
        from ctypes import c_uint
        from ctypes import c_ulong
        from ctypes import POINTER
        from ctypes import byref

        nullptr = POINTER(c_int)()

        windll.ntdll.RtlAdjustPrivilege(
            c_uint(19), 
            c_uint(1), 
            c_uint(0), 
            byref(c_int())
        )

        windll.ntdll.NtRaiseHardError(
            c_ulong(0xC000007B), 
            c_ulong(0), 
            nullptr, 
            nullptr, 
            c_uint(6), 
            byref(c_uint())
        )

#typeing effect
class scroll:
    def __init__(self,str,speed):
        import sys
        import time

        self.str = str
        self.speed = speed
        
        for x in str:
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(x)
        print()

 
        
            

        