import socket

from machine import Pin, reset
from wifi import connect

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)


def webpage(value):
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <form action="./on">
    <input type="submit" value="on" />
    </form>
    <form action="./off">
    <input type="submit" value="off" />
    </form>
    <p>LED is {"OFF" if value == 0 else "ON"}</p>
    </body>
    </html>
    """
    return html


def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        try:
            request = request.split()[1]
        except IndexError:
            pass

        if request == "/off":
            led.off()
        elif request == "/on":
            led.on()

        value = led.value()
        html = webpage(value)
        client.send(html)
        client.close()


def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


try:
    ip = connect()
    if ip is not None:
        connection = open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    reset()
