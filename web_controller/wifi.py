import network
import time

from secrets import SSID, WIFI_PW


def connect(ssid=SSID, psk=WIFI_PW):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, psk)

    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print("waiting for connection...")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("wifi connection failed")
    else:
        ip = wlan.ifconfig()[0]
        print(f"connected to {ip}")
        return ip
