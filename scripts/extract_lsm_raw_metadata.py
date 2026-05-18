"""
Extract metadata from original LSM files for thesis Chapter 2
"""
import numpy as np
from pathlib import Path
from tifffile import TiffFile
import pandas as pd
from datetime import datetime

BASE = Path("/baldig/bioprojects2/dikshans/chemores/data")

FILES = [
    # (short_name, group, full_path)
    # --- Original files  ---
    ("CNTL-MB231",  "Control",        BASE / "original_files/CNTL-MB231.lsm"),
    ("TAMO-MB231",  "Chemoresistant", BASE / "original_files/TAMO-MB231.lsm"),

    # --- Testset: more control recordings ---
    ("CNTL_75uM_p1","Control",        BASE / "testset/CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p1.lsm"),
    ("CNTL_75uM_p2","Control",        BASE / "testset/CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p2.lsm"),
    ("CNTL_75uM_p3","Control",        BASE / "testset/CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p3.lsm"),
    ("CNTL_75uM_p4","Control",        BASE / "testset/CNTL_75uM_CNTL_15uM_2025_10_09__12_22_04__p4.lsm"),

    # --- New batch: more chemoresistant recordings ---
    ("TAMO_p1",     "Chemoresistant", BASE / "new_batch/TAMO-TAMO_CNTL_CNTL-TAMO_2025_11_16__12_46_08__p1.lsm"),
    ("TAMO_p2",     "Chemoresistant", BASE / "new_batch/TAMO-TAMO_CNTL_CNTL-TAMO_2025_11_16__12_46_08__p2.lsm"),
]

def extract_lsm_metadata(file_path):
    """Extract comprehensive metadata from LSM file."""
    
    if not file_path.exists():
        print(f"  ✗ File not found: {file_path}")
        return None
    
    try:
        with TiffFile(file_path) as tif:
            series = tif.series[0]
            shape = series.shape
            
            # Parse shape: typically (tiles, timepoints, channels, height, width) or (tiles, channels, height, width)
            if len(shape) == 5:
                n_tiles, n_timepoints, n_channels, height, width = shape
            elif len(shape) == 4:
                n_tiles, n_channels, height, width = shape
                n_timepoints = 1
            else:
                n_tiles = shape[0]
                n_timepoints = "?"
                n_channels = "?"
                height, width = "?", "?"
            
            # File size
            size_gb = file_path.stat().st_size / 1e9
            
            # LSM metadata - safely access nested structure
            lsm_meta = {}
            if hasattr(tif, 'lsm_metadata'):
                try:
                    lsm_meta = tif.lsm_metadata if isinstance(tif.lsm_metadata, dict) else {}
                except:
                    lsm_meta = {}
            
            # Try to extract channel information - safely
            ch_names = []
            n_channels_actual = 0
            try:
                if isinstance(lsm_meta, dict) and 'ChannelColors' in lsm_meta:
                    cc = lsm_meta['ChannelColors']
                    if isinstance(cc, dict) and 'ColorNames' in cc:
                        ch_names = cc['ColorNames']
                        n_channels_actual = len(ch_names)
            except:
                pass
            
            # Try to get timestamps
            acquisition_time = 'N/A'
            try:
                if isinstance(lsm_meta, dict) and 'DimensionTime' in lsm_meta:
                    dt = lsm_meta['DimensionTime']
                    if isinstance(dt, dict) and 'Date' in dt:
                        acquisition_time = dt['Date']
            except:
                pass
            
            # Try to extract laser/detector info
            imaging_setup = {}
            laser_info = {}
            try:
                if isinstance(lsm_meta, dict):
                    if 'ImagingSetup' in lsm_meta:
                        imaging_setup = lsm_meta['ImagingSetup'] if isinstance(lsm_meta['ImagingSetup'], dict) else {}
                    if 'LaserInfo' in lsm_meta:
                        laser_info = lsm_meta['LaserInfo'] if isinstance(lsm_meta['LaserInfo'], dict) else {}
            except:
                pass
            
            metadata = {
                'file_name': file_path.name,
                'file_path': str(file_path),
                'size_GB': round(size_gb, 2),
                'n_tiles': n_tiles,
                'n_timepoints': n_timepoints,
                'n_channels': n_channels_actual if n_channels_actual > 0 else n_channels,
                'image_height': height,
                'image_width': width,
                'acquisition_time': acquisition_time,
                'has_channel_metadata': len(ch_names) > 0,
            }
            
            if ch_names:
                metadata['channel_names'] = ch_names
            
            return metadata
    
    except Exception as e:
        print(f"  ✗ Error reading {file_path.name}: {e}")
        return None

# Extract metadata for all files
print("="*100)
print("RAW LSM FILE METADATA EXTRACTION (8 files)")
print("="*100)

results = []
for name, group, path in FILES:
    print(f"\nProcessing: {name} ({group})")
    print(f"  Path: {path.name}")
    
    meta = extract_lsm_metadata(path)
    if meta:
        meta['file_label'] = name
        meta['group'] = group
        results.append(meta)
        print(f"  ✓ Tiles: {meta['n_tiles']}")
        print(f"  ✓ Timepoints: {meta['n_timepoints']}")
        print(f"  ✓ Channels: {meta['n_channels']}")
        print(f"  ✓ Image size: {meta['image_width']}×{meta['image_height']}")
        print(f"  ✓ File size: {meta['size_GB']} GB")
        if meta['acquisition_time'] != 'N/A':
            print(f"  ✓ Acquisition time: {meta['acquisition_time']}")

# Create summary table
if results:
    df = pd.DataFrame(results)
    
    print("\n" + "="*100)
    print("RAW LSM METADATA SUMMARY")
    print("="*100)
    
    display_cols = ['file_label', 'group', 'n_tiles', 'n_timepoints', 'n_channels', 
                    'image_width', 'image_height', 'size_GB']
    available_cols = [c for c in display_cols if c in df.columns]
    
    print(df[available_cols].to_string(index=False))
    
    # Overall statistics
    print("\n" + "="*100)
    print("ACQUISITION SESSIONS")
    print("="*100)
    print("\nSession 1 (ORIGINAL):")
    orig = df[df['file_label'].isin(['CNTL-MB231', 'TAMO-MB231'])]
    print(f"  Files: {len(orig)}")
    print(f"  Total tiles: {orig['n_tiles'].sum()}")
    print(f"  Timepoints per file: {orig['n_timepoints'].iloc[0]}")
    print(f"  Channels: {orig['n_channels'].iloc[0]}")
    print(f"  Total size: {orig['size_GB'].sum():.1f} GB")
    
    print("\nSession 2 (75µM Control):")
    s75 = df[df['file_label'].str.startswith('CNTL_75uM')]
    print(f"  Files: {len(s75)}")
    print(f"  Total tiles: {s75['n_tiles'].sum()}")
    print(f"  Timepoints per file: {s75['n_timepoints'].iloc[0]}")
    print(f"  Channels: {s75['n_channels'].iloc[0]}")
    print(f"  Total size: {s75['size_GB'].sum():.1f} GB")
    print(f"  Acquisition date: 2025-10-09 12:22:04")
    
    print("\nSession 3 (TAMO New):")
    tamo = df[df['file_label'].str.startswith('TAMO_p')]
    print(f"  Files: {len(tamo)}")
    print(f"  Total tiles: {tamo['n_tiles'].sum()}")
    print(f"  Timepoints per file: {tamo['n_timepoints'].iloc[0]}")
    print(f"  Channels: {tamo['n_channels'].iloc[0]}")
    print(f"  Total size: {tamo['size_GB'].sum():.1f} GB")
    print(f"  Acquisition date: 2025-11-16 12:46:08")
    
    # Save to CSV
    output_path = Path('/home/emartinl/chemores/results/raw_lsm_metadata_summary.csv')
    df.to_csv(output_path, index=False)
    print(f"\n✓ Full metadata saved to: {output_path}")
    
    # Save channel names if available
    if 'channel_names' in df.columns and df['channel_names'].iloc[0]:
        print("\n" + "="*100)
        print("SPECTRAL CHANNELS (from first file)")
        print("="*100)
        ch_names = df['channel_names'].iloc[0]
        for i, name in enumerate(ch_names):
            print(f"  [{i:2d}] {name}")
