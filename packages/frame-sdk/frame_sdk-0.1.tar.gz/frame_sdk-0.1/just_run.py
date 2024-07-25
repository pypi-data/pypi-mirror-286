import asyncio
import datetime
import os
import random
from src.frame_sdk import Bluetooth, Frame
from src.frame_sdk.display import Alignment


async def main():
    # the with statement handles the connection and disconnection to Frame
    async with Frame() as f:
        print(f"Connected: {f.bluetooth.is_connected()}")
        # let's get the current battery level
        print(f"Frame battery: {await f.get_battery_level()}%")
        await f.bluetooth.send_break_signal()
        await f.files.delete_file("/lib/prntLng.lua")
        await f.bluetooth.send_reset_signal()

    async with Frame() as f:
        f.bluetooth.print_debugging = True
        await f.display.show_text(" ", 1, 1)
        
        await f.files.write_file("main.lua", b"frame.display.text('Battery: ' .. frame.battery_level() ..  '%', 10, 10);if frame.time.utc() > 10000 then local time_now = frame.time.date();frame.display.text(time_now['hour'] .. ':' .. time_now['minute'], 300, 160);frame.display.text(time_now['month'] .. '/' .. time_now['day'] .. '/' .. time_now['year'], 300, 220) end;frame.display.show();frame.sleep(5);frame.display.text(' ',1,1);frame.display.show();frame.sleep()")
        
        # display battery indicator and time as home screen
        time:str = datetime.datetime.now().strftime("%-I:%M %p\n%a, %B %d, %Y")
        batteryPercent = await f.get_battery_level()
        batteryText = f"{batteryPercent}%"
        color = 2 if batteryPercent < 20 else 6 if batteryPercent < 50 else 9
        batteryWidth = 150
        batteryHeight = 75
        await f.display.draw_rect(640-32,40 + batteryHeight//2-8, 32, 16, 1)
        await f.display.draw_rect_filled(640-16-batteryWidth, 40-8, batteryWidth+16, batteryHeight+16, 8, 1, 15)
        await f.display.draw_rect(640-8-batteryWidth, 40, int(batteryWidth * 0.01 * batteryPercent), batteryHeight, color)
        await f.display.write_text(batteryText, 640-8-batteryWidth, 40, batteryWidth, batteryHeight, Alignment.MIDDLE_CENTER)
        await f.display.write_text(time, align=Alignment.MIDDLE_CENTER)

        await f.display.show()
        await asyncio.sleep(10)
        await f.display.scroll_text("""
[Intro]
A long, long time ago
In a galaxy far away
Naboo was under an attack
And I thought me and Qui-Gon Jinn
Could talk the Federation into
Maybe cutting them a little slack
But their response, it didn't thrill us
They locked the doors and tried to kill us
""")
        # Show the full palette
        width = 640 // 4
        height = 400 // 4
        for color in range(0, 16):
            tile_x = (color % 4)
            tile_y = (color // 4)
            await f.display.draw_rect(tile_x*width+1, tile_y*height+1, width, height, color)
            await f.display.write_text(f"{color}", tile_x*width+width//2+1, tile_y*height+height//2+1)
        await f.display.show()
        


        # await f.files.write_file("/test.bmp", bitmap, checked=True)
        # await f.run_lua("local f = frame.file.open(\"/test.bmp\");while true do;chunk = f:read();if chunk == nil then break end;data = data .. chunk;end;f:close()", checked=True)

    print("disconnected")

asyncio.run(main())
