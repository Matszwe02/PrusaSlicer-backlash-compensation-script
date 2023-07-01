## Simple backlash compensation script


This script is in 'alpha' version and some bugs may appear. It's purpose is to test backlash on 3d printer that doesn't support firmware backlash compensation.
It'll be great if someone finds it useful and want to contribute / discuss about it!
Backlash amount possible to change in `backlash_x_distance` and `backlash_y_distance`, speed of applying backlash in mm/s in `backlash_speed`.

Implement it like this:

> C:\Users\`user`\AppData\Local\Programs\Python\Python310\python.exe D:\'script_path'\BacklashCompensation.py

If not using `Slic3r` type slicer, you may run it on a sliced gcode:

> Python ./BacklashCompensation.py ./3DBenchy.gcode