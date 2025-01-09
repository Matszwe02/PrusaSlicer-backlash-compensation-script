# UPDATE 2025-01-09: This repository is now archived due to switching workflow to GcodeTools
[GcodeTools repo](https://github.com/Matszwe02/GcodeTools)

So here is an example implementation of that script using `GcodeTools`.

It doesn't work well, but it is here to show how it can be easily done.

Maybe sometimes I'll add backlash compensation method into GcodeTools directly, idk, let me know if it will be useful.

```py
from gcode_tools import Gcode, GcodeTools, Vector, Block
import sys

backlash_x = 0.1
backlash_y = 0.1
backlash_speed = 1200

input_file = sys.argv[1]
output_file = input_file

gcode = Gcode().from_file(input_file)
gcode.order()
dir = Vector()
last_dir = Vector()

out_gcode: Gcode = gcode.new()
for i in gcode:
    dist = i.move.distance().vector_op(Vector.zero(), lambda a, b: a, 0)
    if dist.X > gcode.config.step: dir.X = backlash_x/2
    if dist.X < -gcode.config.step: dir.X = -backlash_x/2
    if dist.Y > gcode.config.step: dir.Y = backlash_y/2
    if dist.Y < -gcode.config.step: dir.Y = -backlash_y/2
    
    if dir != last_dir:
        i_orig = i.prev.as_origin() or Block()
        i_orig.move.translate(dir)
        i_orig.move.speed = backlash_speed
        out_gcode.g_add(i_orig)
        last_dir = dir.copy()
    i.move.translate(dir)
    out_gcode.g_add(i)
out_gcode.write_file(output_file)
```

## Simple backlash compensation script


This script is in 'alpha' version and some bugs may appear. It's purpose is to test backlash on 3d printer that doesn't support firmware backlash compensation.
It'll be great if someone finds it useful and want to contribute / discuss about it!
Backlash amount possible to change in `backlash_x_distance` and `backlash_y_distance`, speed of applying backlash in mm/s in `backlash_speed`.

Implement it like this:

```sh
 C:\Users\\`user`\AppData\Local\Programs\Python\Python310\python.exe D:\\`script_path`\BacklashCompensation.py
```

If not using `Slic3r` type slicer, you may run it on a sliced gcode:

```sh
Python ./BacklashCompensation.py ./3DBenchy.gcode
```
