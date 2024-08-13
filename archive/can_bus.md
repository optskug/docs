# What I've observed about ECU Security Key

I'm not great at reverse-engineering, but this is what *I've* seen.

**dec 2023 note**: web cabana has since been removed. you'll need to use desktop qt cabana now.

You can get here by going to Comma Connect, clicking on a drive, uploading all log files, and selecting "View in Cabana" after the files are uploaded:

<img width="471" alt="image" src="https://user-images.githubusercontent.com/5363/206864999-05da8720-a724-4316-a9b0-c0fab534935d.png">

Once in Cabana, click `Load DBC` and select `toyota_nodsu_pt_generated.dbc`. Filter the messages for `STEERING_LKA`. Click on one of the STEERING_LKA messages and change the message size to 8. If you see extremely high-entropy and random bytes on the last 4 bytes, then the vehicle likely has Toyota Security Key.

-----

![](https://user-images.githubusercontent.com/5363/91650158-ed5f5880-ea30-11ea-9b07-6e3dca7f8f83.gif)

* Bus 128 is like what OP would love to be sending. That is the old Toyota checksum scheme. It's a rather low FPS GIF with a rather low period but imagine the checksum being obviously steadily increasing due to the counter part of the message also steadily increasing but everything else pinned to `0x00`.
* Bus 2 is what we're seeing and that's from the camera right? The last four bytes are super high entropy looking.
* Bus 0: 🤷‍♂️, but I am also not sure if it matters.

-----

* No existing checksum algorithms were working.
* There is a 4 byte authentication code on the CAN message instead of the simple 1 byte checksum of past Toyotas.
* The same inputs result in different "checksum"/authentication code outputs.
* The messages are different between ignitions.
* The messages are different between vehicles.
