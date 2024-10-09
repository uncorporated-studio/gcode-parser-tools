import os
from pygcode import Line

# Path to your G-code file
input_file = 'test.gcode'
output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}-{os.path.splitext(os.path.basename(__file__))[0]}.gcode"

def modify_gcode(input_file, output_file):
    # Read all lines from the input file
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
    
    # Keep the first three lines and the last line
    start_lines = lines[:3]
    end_line = lines[-1]
    
    with open(output_file, 'w') as f_out:
        # Write the first three lines without modification
        f_out.writelines(start_lines)
        
        keep_next_g1 = False

        # Process only the middle section (4th to second-to-last line) for modification
        for line in lines[3:-1]:
            gcode_line = Line(line)
            
            # Check for G0 (rapid move)
            if 'G0' in line:
                f_out.write(line)
                keep_next_g1 = True
            # Keep only the first G1 after a G0
            elif 'G1' in line and keep_next_g1:
                f_out.write(line)
                keep_next_g1 = False
            # Always keep Z5.00 (if necessary for your tool)
            elif 'Z5.00' in line:
                f_out.write(line)

        # Write the last line from the original file without modification
        f_out.write(end_line)

# Run the function to modify G-code with specified file names and line retention
modify_gcode(input_file, output_file)