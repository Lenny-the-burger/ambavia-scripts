#!/usr/bin/env python3
"""
Script to read lines from a file and send them to a target window.
Usage: python line_sender.py <input_file>
"""

import sys
import time
import argparse
import pyautogui
import pyperclip
from typing import List

def get_window_titles() -> List[str]:
    """Get list of all open windows."""
    try:
        import pygetwindow as gw
        windows = gw.getAllWindows()
        return [w.title for w in windows if w.title.strip()]
    except ImportError:
        print("pygetwindow not available. Install with: pip install pygetwindow")
        return []

def select_target_window() -> str:
    """Interactive window selection."""
    windows = get_window_titles()
    
    if not windows:
        print("No windows found or pygetwindow not available.")
        print("You'll need to manually click on the target window after the countdown.")
        return ""
    
    print("\nAvailable windows:")
    for i, title in enumerate(windows, 1):
        print(f"{i}. {title}")
    
    while True:
        try:
            choice = input("\nSelect window number (or 0 to manually click): ")
            if choice == "0":
                return ""
            
            idx = int(choice) - 1
            if 0 <= idx < len(windows):
                return windows[idx]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def focus_window(window_title: str) -> bool:
    """Focus on the specified window."""
    if not window_title:
        return False
    
    try:
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            windows[0].activate()
            time.sleep(0.5)
            return True
    except ImportError:
        pass
    return False

def send_lines_to_window(file_path: str, delay: float = 0.5):
    """Read file and send each line to the target window."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not lines:
        print("File is empty.")
        return
    
    print(f"\nLoaded {len(lines)} lines from {file_path}")
    
    # Window selection
    target_window = select_target_window()
    
    if target_window:
        print(f"Target window: {target_window}")
        if not focus_window(target_window):
            print("Failed to focus window. Please click on the target window manually.")
    else:
        print("No window selected. Please click on the target window manually.")
    
    # Countdown
    print("\nStarting in...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Starting!")
    
    # Send lines
    for i, line in enumerate(lines, 1):
        line = line.rstrip('\n\r')  # Remove newline characters
        
        if not line.strip():  # Skip empty lines
            print(f"Line {i}: Skipping empty line")
            continue
        
        print(f"Line {i}: {line[:50]}{'...' if len(line) > 50 else ''}")
        
        # Copy to clipboard and paste
        pyperclip.copy(line)
        pyautogui.hotkey('ctrl', 'v')
        
        # Press Enter
        pyautogui.press('enter')
        
        # Wait before next line
        time.sleep(delay)
    
    print(f"\nCompleted! Sent {len([l for l in lines if l.strip()])} lines.")

def main():
    parser = argparse.ArgumentParser(description='Send file lines to target window')
    parser.add_argument('file', help='Input text file')
    parser.add_argument('-d', '--delay', type=float, default=0.1,
                        help='Delay between lines in seconds (default: 0.1)')
    
    args = parser.parse_args()
    
    # Safety check
    pyautogui.FAILSAFE = True
    print("FAILSAFE enabled: Move mouse to top-left corner to stop the script")
    
    send_lines_to_window(args.file, args.delay)

if __name__ == "__main__":
    main()