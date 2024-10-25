pip install pyinstaller

save all .py in a folder/package
Via2YOlo
    - main.py
    - via2yolo.py
    - utils.py
    - assets (optional)
no icon
pyinstaller --onefile --windowed main.py

with icon
pyinstaller --onefile --windowed --icon=assets/logo.ico main.py
