import os
import struct

def read_uint32(file, offset):
    file.seek(offset)
    return struct.unpack('<I', file.read(4))[0]

def construct_header(entity_length, map_revision):
    header = bytearray()
    header.extend(struct.pack('<I', 0x00000014))  # Magic number
    header.extend(struct.pack('<I', 0))           # Zero
    header.extend(struct.pack('<I', 0))           # Zero  
    header.extend(struct.pack('<I', entity_length)) 
    header.extend(struct.pack('<I', map_revision))
    return header

def extract_entity_lump(bsp_path, output_dir):
    with open(bsp_path, 'rb') as bsp:
        # Get entity length from 0x0C
        entity_length = read_uint32(bsp, 0x0C)
        
        # Get map revision from 0x408
        map_revision = read_uint32(bsp, 0x408)
        
        # Get data offset from 0x08
        data_offset = read_uint32(bsp, 0x08)
        
        # Create header
        header = construct_header(entity_length, map_revision)
        
        # Read entity data from offset
        bsp.seek(data_offset)
        entity_data = bsp.read(entity_length)
        
        # Combine header and data
        lump_data = header + entity_data
        
        # Create output filename in target directory
        base_name = os.path.splitext(os.path.basename(bsp_path))[0]
        output_name = os.path.join(output_dir, f"{base_name}_l_0.lmp")
        
        # Write combined data
        with open(output_name, 'wb') as lmp:
            lmp.write(lump_data)

def main():
    # Calculate target directory path
    current_dir = os.path.abspath(os.path.dirname(__file__))
    target_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'hl2_complete', 'maps'))
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Process all BSP files in current directory
    for file in os.listdir('.'):
        if file.endswith('.bsp'):
            print(f"Extracting from {file}...")
            extract_entity_lump(file, target_dir)
            print(f"Saved to {target_dir}")

if __name__ == '__main__':
    main()