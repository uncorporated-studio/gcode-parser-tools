from pygcode import Line

# Path to your G-code file
input_file = 'your_gcode_file.gcode'
output_file = 'modified_gcode.gcode'

def modify_gcode(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        keep_next_g1 = False

        for line in f_in:
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

# Run the function to modify G-code
modify_gcode(input_file, output_file)
