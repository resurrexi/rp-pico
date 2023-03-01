import uasyncio

from machine import Pin
from http import parse_http_request, parse_query_string
from wifi import connect

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div class="h-screen w-screen grid grid-cols-1 place-content-center">
    <form class="flex justify-center" action="./" method="post">
      <input type="text" name="state" value="{STATE}" hidden>
      <input type="submit" class="text-white bg-{COLOR}-700 hover:bg-{COLOR}-800 focus:ring-4 focus:ring-{COLOR}-300 font-medium rounded-lg text-5xl px-5 py-2.5 mr-2 mb-2 focus:outline-none" value="TURN {NEW_STATE}" />
    </form>
  </div>
</body>
</html>
"""


async def serve(reader, writer):
    print("Client connected")
    req_buffer = await reader.read(4096)
    req = parse_http_request(req_buffer)

    if req["method"] == "GET":
        state = "on" if led.value() == 1 else "off"
        new_state = "OFF" if state == "on" else "ON"
        color = "red" if state == "on" else "green"
    else:
        body = parse_query_string(req["body"])

        if body["state"] == "on":
            state = "off"
            new_state = "ON"
            color = "green"
            led.off()
        else:
            state = "on"
            new_state = "OFF"
            color = "red"
            led.on()

    response = HTML.format(STATE=state, NEW_STATE=new_state, COLOR=color)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    print("Connecting to wifi...")
    connect()

    print("Setting up webserver...")
    uasyncio.create_task(uasyncio.start_server(serve, "0.0.0.0", 80))
    while True:
        onboard.on()
        await uasyncio.sleep(0.25)
        onboard.off()
        await uasyncio.sleep(2)


try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
