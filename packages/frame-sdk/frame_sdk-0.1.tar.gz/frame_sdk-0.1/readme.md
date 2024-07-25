# frame-sdk-python
The Python SDK for the Frame from @brilliantlabsAR

## Install

```sh
pip3 install frame-sdk
```

## Documentation

Check out [the docs](https://docs.brilliant.xyz/frame/building-apps/) for complete guidance on everything you can do with the Frame.

## Examples

Here's a simple example of how to use the Frame SDK to display text, take a photo, and more.

```python
import asyncio
from frame_sdk import Frame


async def main():
    # the with statement handles the connection and disconnection to Frame
    async with Frame() as f:
        # you can access the lower-level bluetooth connection via f.bluetooth, although you shouldn't need to do this often
        print(f"Connected: {f.bluetooth.is_connected()}")

        # let's get the current battery level
        print(f"Frame battery: {await f.get_battery_level()}%")

        # let's write (or overwrite) the file greeting.txt with "Hello world".
        # You can provide a bytes object or convert a string with .encode()
        await f.files.write_file("greeting.txt", b"Hello world")

        # And now we read that file back.
        # Note that we should convert the bytearray to a string via the .decode() method.
        print((await f.files.read_file("greeting.txt")).decode())
        
        # run_lua will automatically handle scripts that are too long for the MTU, so you don't need to worry about it.
        # It will also automatically handle responses that are too long for the MTU automatically.
        await f.run_lua("frame.display.text('Hello world', 50, 100);frame.display.show()")

        # evaluate is equivalent to f.run_lua("print(\"1+2\"), await_print=True)
        # It will also automatically handle responses that are too long for the MTU automatically.
        print(await f.evaluate("1+2"))

        # take a photo and save to disk
        await f.display.show_text("Taking photo...", 200, 150)
        await f.camera.save_photo("frame-test-photo.jpg")
        await f.display.show_text("Photo saved!", 200, 150)
        # or with more control
        await f.camera.save_photo("frame-test-photo-2.jpg", autofocus_seconds=3, quality=f.camera.HIGH_QUALITY, autofocus_type=f.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED)
        # or get the raw bytes
        photo_bytes = await f.camera.take_photo(autofocus_seconds=1)

        # Show the full palette
        width = 640 // 4
        height = 400 // 4
        for color in range(0, 16):
            tile_x = (color % 4)
            tile_y = (color // 4)
            await f.display.draw_rect(tile_x*width+1, tile_y*height+1, width, height, color)
            await f.display.write_text(f"{color}", tile_x*width+width//2+1, tile_y*height+height//2+1)
        await f.display.show()
        await asyncio.sleep(5)

        # scroll some long text
        await f.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")

        # display battery indicator and time as a home screen
        batteryPercent = await f.get_battery_level()
        # select a battery fill color from the default palette based on level
        color = 2 if batteryPercent < 20 else 6 if batteryPercent < 50 else 9
        # specify the size of the battery indicator in the top-right
        batteryWidth = 150
        batteryHeight = 75
        # draw the endcap of the battery
        await f.display.draw_rect(640-32,40 + batteryHeight//2-8, 32, 16, 1)
        # draw the battery outline
        await f.display.draw_rect_filled(640-16-batteryWidth, 40-8, batteryWidth+16, batteryHeight+16, 8, 1, 15)
        # fill the battery based on level
        await f.display.draw_rect(640-8-batteryWidth, 40, int(batteryWidth * 0.01 * batteryPercent), batteryHeight, color)
        # write the battery level
        await f.display.write_text(f"{batteryPercent}%", 640-8-batteryWidth, 40, batteryWidth, batteryHeight, Alignment.MIDDLE_CENTER)
        # write the time and date in the center of the screen
        await f.display.write_text(datetime.datetime.now().strftime("%-I:%M %p\n%a, %B %d, %Y"), align=Alignment.MIDDLE_CENTER)

    print("disconnected")



asyncio.run(main())

```

## Tests

To run the unit tests, ensure you have pytest installed:

```sh
pip3 install pytest
```

With a Frame device in range, run:

```sh
python3 -m pytest tests/*
```