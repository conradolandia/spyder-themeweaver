#!/usr/bin/env python3
"""Debug script to understand QDarkStyle QRC generation with proper directory structure."""

import os
import tempfile
from pathlib import Path

try:
    from qdarkstyle.utils.images import generate_qrc_file, compile_qrc_file
    from qdarkstyle.dark.palette import DarkPalette
    
    print("Testing QDarkStyle QRC generation with proper setup...")
    
    # Create a temporary directory 
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create the expected directory structure
        # Based on QDarkStyle, it expects to work in a directory with "rc" subfolder
        
        # Create dark variant directory
        dark_dir = tmpdir / "dark"
        dark_dir.mkdir()
        
        # Create rc directory inside dark
        rc_dir = dark_dir / "rc"
        rc_dir.mkdir()
        
        # Create some test PNG files
        test_files = ["arrow_down.png", "checkbox_checked.png", "window_close.png"]
        for filename in test_files:
            (rc_dir / filename).touch()
        
        print(f"Created directory structure:")
        print(f"  {tmpdir}")
        print(f"  └── dark/")
        print(f"      └── rc/")
        for f in test_files:
            print(f"          ├── {f}")
        
        # Create palette instance
        palette = DarkPalette()
        
        # Change to the dark directory - this might be what QDarkStyle expects
        old_cwd = os.getcwd()
        os.chdir(dark_dir)
        
        print(f"\\nChanged working directory to: {os.getcwd()}")
        print(f"Files in current rc/: {list((Path('.') / 'rc').iterdir())}")
        
        try:
            print("\\nGenerating QRC file...")
            generate_qrc_file(
                resource_prefix="qss_icons/dark",
                style_prefix="qdarkstyle/dark", 
                palette=palette
            )
            print("QRC generation succeeded!")
            
            # Check what files were created
            print(f"\\nFiles in dark dir after QRC generation:")
            for f in Path('.').rglob("*"):
                if f.is_file():
                    print(f"  {f}")
                    
            # Look for any .qrc files
            qrc_files = list(Path('.').glob("*.qrc"))
            print(f"\\nFound QRC files: {qrc_files}")
            
            if qrc_files:
                qrc_file = qrc_files[0]
                print(f"\\nContent of {qrc_file}:")
                print(qrc_file.read_text())
                
                # Now try to compile it
                print("\\nCompiling QRC file...")
                compile_qrc_file(
                    compile_for="qtpy",
                    qrc_path=".",  # Current directory
                    palette=palette
                )
                
                # Check for _rc.py files
                rc_py_files = list(Path('.').glob("*_rc.py"))
                print(f"\\nFound compiled Python files: {rc_py_files}")
                
            else:
                print("\\nNo QRC files found!")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            os.chdir(old_cwd)
            
        # Also test in the main tmpdir with different structure
        print("\\n" + "="*60)
        print("Testing with flat structure...")
        
        # Create rc directory at tmpdir level
        rc_dir_flat = tmpdir / "rc" 
        rc_dir_flat.mkdir()
        
        for filename in test_files:
            (rc_dir_flat / filename).touch()
            
        os.chdir(tmpdir)
        print(f"Changed to: {os.getcwd()}")
        
        try:
            generate_qrc_file(
                resource_prefix="qss_icons",
                style_prefix="qdarkstyle",
                palette=palette
            )
            
            qrc_files = list(Path('.').glob("*.qrc"))
            print(f"Found QRC files in flat structure: {qrc_files}")
            
            if qrc_files:
                print(f"Content of QRC file:")
                print(qrc_files[0].read_text()[:500] + "...")
                
        except Exception as e:
            print(f"Flat structure error: {e}")
            
        finally:
            os.chdir(old_cwd)
            
except ImportError as e:
    print(f"Cannot import QDarkStyle: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 