#!/usr/bin/env python
"""
Script to merge multiple HDF5 demo files.
Each input file contains demo_1 to demo_N, and the output will have
sequentially numbered demos (e.g., 4 files with 20 demos each -> demo_1 to demo_80)
"""

import h5py
import argparse
import os
from collections import OrderedDict


def merge_demo_files(input_files, output_file):
    """
    Merge multiple HDF5 demo files into a single file with unique demo numbers.
    
    Args:
        input_files: List of paths to input HDF5 files
        output_file: Path to output HDF5 file
    """
    print(f"Merging {len(input_files)} demo files...")
    
    # Create output file
    with h5py.File(output_file, 'w') as f_out:
        demo_counter = 0
        total_demos = 0
        
        # Process each input file
        for file_idx, input_file in enumerate(input_files):
            print(f"\nProcessing file {file_idx + 1}/{len(input_files)}: {input_file}")
            
            with h5py.File(input_file, 'r') as f_in:
                # Get all demo keys (demo_0, demo_1, etc.)
                demo_keys = [key for key in f_in['data'].keys() if key.startswith('demo')]
                demo_keys = sorted(demo_keys, key=lambda x: int(x.split('_')[1]))
                
                print(f"  Found {len(demo_keys)} demos")
                
                # Copy each demo with new numbering
                for demo_key in demo_keys:
                    demo_counter += 1
                    new_demo_name = f"demo_{demo_counter}"
                    
                    # Copy the entire demo group
                    f_in.copy(f'data/{demo_key}', f_out, f'data/{new_demo_name}')
                    
                total_demos += len(demo_keys)
        
        # Copy metadata from first file if it exists
        print("\nCopying metadata from first file...")
        with h5py.File(input_files[0], 'r') as f_first:
            # Copy attributes
            if 'data' in f_first:
                for attr_name, attr_value in f_first['data'].attrs.items():
                    f_out['data'].attrs[attr_name] = attr_value
            
            # Update total number of demos
            f_out['data'].attrs['total'] = total_demos
    
    print(f"\n✓ Successfully merged {total_demos} demos into {output_file}")
    print(f"  Output contains: demo_1 to demo_{total_demos}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple HDF5 demo files with sequential numbering"
    )
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input HDF5 demo files to merge'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output HDF5 file path'
    )
    
    args = parser.parse_args()
    
    # Verify input files exist
    for input_file in args.input_files:
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            return 1
    
    # Check if output file already exists
    if os.path.exists(args.output):
        response = input(f"Output file {args.output} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return 0
    
    merge_demo_files(args.input_files, args.output)
    return 0


if __name__ == '__main__':
    exit(main())

