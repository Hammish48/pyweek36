import time
import sys
version = (3, 10)

if sys.version_info[:2] < version:
    print("this game requires python 3.10")
    time.sleep(3)
    sys.exit()

try:
    import pygame
except ImportError as e:
    print("please download pygame")
    time.sleep(3)
    sys.exit()

try:
    import os
    import main
    import pathlib
    os.chdir(pathlib.Path(__file__).parent)
    main.main()
except Exception as e:
    print(e)
    time.sleep(3)