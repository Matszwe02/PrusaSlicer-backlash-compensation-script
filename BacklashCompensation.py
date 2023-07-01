import sys
import re

sourceFile=sys.argv[1]


dir_x_previous = -1
dir_y_previous = -1

x_current_str = 0
y_current_str = 0

backlash_x_distance = 0.05
backlash_y_distance = 0.05

backlash_speed = 60

current_move = ""


def calculate_backlash(next_move):
    global dir_x_previous, dir_y_previous, x_current_str, y_current_str, current_move
    
    if current_move == "":
        current_move = next_move
    
    # Extract the X and Y values from the move command using regular expressions
    
    for dir in current_move.split():
        if dir[0].upper() == "X":
            x_current_str = dir[1:]
        if dir[0].upper() == "Y":
            y_current_str = dir[1:]
    
    x_next_str = x_current_str    
    y_next_str = y_current_str
    
    for dir in next_move.split():
        if dir[0].upper() == "X":
            x_next_str = dir[1:]
        if dir[0].upper() == "Y":
            y_next_str = dir[1:]
    
    current_move = next_move
    
    is_valid_move = type(x_current_str) == str and type(y_current_str) == str
    
    
    x_next = float(x_next_str)
    y_next = float(y_next_str)
    x_current = float(x_current_str)
    y_current = float(y_current_str)    
    
    dir_x_next = 0
    dir_y_next = 0
    
    if x_next > x_current:
        dir_x_next = 1
    if x_next < x_current:
        dir_x_next = -1
    if y_next > y_current:
        dir_y_next = 1
    if y_next < y_current:
        dir_y_next = -1
    
    x_offset = 0
    y_offset = 0
    
    if dir_x_next == 1:
        x_offset = (backlash_x_distance / 2)
    if dir_x_next == -1:
        x_offset = -(backlash_x_distance / 2)
        
    if dir_y_next == 1:
        y_offset = (backlash_y_distance / 2)
    if dir_y_next == -1:
        y_offset = -(backlash_y_distance / 2)


    x_next += x_offset
    y_next += y_offset
    
    
    modified_command = next_move.replace(f"X{x_next_str}", f"X{x_next:.3f}")
    modified_command = modified_command.replace(f"Y{y_next_str}", f"Y{y_next:.3f}")
    
    # modified_command += f"; {x_next:.3f},{y_next:.3f} , {x_current:.3f},{y_current:.3f}, {is_valid_move}"
    
    if (dir_x_next != dir_x_previous or dir_y_next != dir_y_previous) and is_valid_move:
        backlash_move = f"G0 X{(x_current + x_offset):.3f} Y{(y_current + y_offset):.3f} F{backlash_speed * 60}; backlash"
        modified_command = backlash_move + "\n" + modified_command
    
    if modified_command[-1] != "\n":
        modified_command += "\n"
    
    if dir_x_next != 0:
        dir_x_previous = dir_x_next
    if dir_y_next != 0:
        dir_y_previous = dir_y_next
        
    return modified_command




# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
    

with open(sourceFile, "w") as f:
    for line in lines:
        
        parts = line.split(';', 1)
        if len(parts) > 0:
            
            command = parts[0].strip()

            if command:
                if re.search("G1 ", command) or re.search("G0 ", command):
                    line = calculate_backlash(command)
                
            
            
            f.write(line)
