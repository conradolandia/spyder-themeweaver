#!/usr/bin/env python3
"""Debug script to understand QDarkStyle QRC generation."""

import os
import tempfile
from pathlib import Path

try:
    from qdarkstyle.utils.images import generate_qrc_file, compile_qrc_file
    from qdarkstyle.dark.palette import DarkPalette
    
    print("Testing QDarkStyle QRC generation...")
    
    # Create a temporary directory 
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create some fake rc files
        rc_dir = tmpdir / "rc"
        rc_dir.mkdir()
        
        # Create a few fake PNG files
        for i in range(3):
            (rc_dir / f"test{i}.png").touch()
        
        print(f"Created test directory: {tmpdir}")
        print(f"RC directory: {rc_dir}")
        print(f"Files in rc/: {list(rc_dir.iterdir())}")
        
        # Create palette instance
        palette = DarkPalette()
        
        print(f"Palette ID: {palette.ID}")
        print(f"Working directory: {os.getcwd()}")
        
        # Try to generate QRC file
        print("\\nGenerating QRC file...")
        try:
            generate_qrc_file(
                resource_prefix="qss_icons/dark",
                style_prefix="qdarkstyle/dark", 
                palette=palette
            )
            print("QRC generation succeeded!")
            
            # Check what files were created
            print(f"\\nFiles in tmpdir after QRC generation:")
            for f in tmpdir.rglob("*"):
                if f.is_file():
                    print(f"  {f.relative_to(tmpdir)}")
                    
        except Exception as e:
            print(f"QRC generation failed: {e}")
            import traceback
            traceback.print_exc()
            
        # Also try with different parameters
        print("\\n" + "="*50)
        print("Trying with current directory...")
        
        # Change to the tmpdir
        old_cwd = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            generate_qrc_file(
                resource_prefix="qss_icons/dark",
                style_prefix="qdarkstyle/dark",
                palette=palette
            )
            print("QRC generation in tmpdir succeeded!")
            
            # Check what files were created
            print(f"\\nFiles after second attempt:")
            for f in tmpdir.rglob("*"):
                if f.is_file():
                    print(f"  {f.relative_to(tmpdir)}")
                    
        except Exception as e:
            print(f"QRC generation in tmpdir failed: {e}")
            
        finally:
            os.chdir(old_cwd)
            
except ImportError as e:
    print(f"Cannot import QDarkStyle: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 