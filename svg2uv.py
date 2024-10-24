import xml.etree.ElementTree as ET
import pandas as pd
import re

# Path to your SVG file
input_svg_file = 'drawing.svg'

# SVG dimensions for conversion to UV coordinates
svg_width = 500
svg_height = 500

# Parse the SVG file
tree = ET.parse(input_svg_file)
root = tree.getroot()

# Define the SVG namespace (usually required for SVG files)
namespace = {'svg': 'http://www.w3.org/2000/svg'}

# List to store the line data and set to track unique lines
lines_data = []
unique_lines = set()

# Regular expression to match path commands in the format 'M x y L x y'
line_pattern = re.compile(r'M\s*(-?\d+\.?\d*)\s*(-?\d+\.?\d*)\s*L\s*(-?\d+\.?\d*)\s*(-?\d+\.?\d*)')

# Find all path elements in the SVG
for path in root.findall('.//svg:path', namespace):
    d_attr = path.get('d')
    
    # Use regex to extract the coordinates from the path's d attribute
    match = line_pattern.match(d_attr)
    if match:
        # Convert pixel coordinates to UV coordinates
        start_x, start_y, end_x, end_y = map(lambda x: round(float(x)), match.groups())
        start_x_uv = start_x / svg_width
        start_y_uv = start_y / svg_height
        end_x_uv = end_x / svg_width
        end_y_uv = end_y / svg_height
        
        # Create a tuple representing the line to check for uniqueness
        line_tuple = (start_x_uv, start_y_uv, end_x_uv, end_y_uv)
        
        # Add to the list only if the line hasn't been added before
        if line_tuple not in unique_lines:
            unique_lines.add(line_tuple)  # Add to set to track uniqueness
            lines_data.append({
                'start_x': start_x_uv,
                'start_y': start_y_uv,
                'end_x': end_x_uv,
                'end_y': end_y_uv
            })

# Convert the list to a DataFrame
df = pd.DataFrame(lines_data)

# Save the DataFrame to a CSV file with headers included
output_csv_file = 'line_coordinates_uv.csv'
df.to_csv(output_csv_file, index=False, header=True)
