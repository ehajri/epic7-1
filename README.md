## Directions by [/u/Aicilia](https://www.reddit.com/r/EpicSeven/comments/bv2hkx/ocr_gear_exporter_installation_guide_courtesy_of/) for Windows

My friend /u/max030994 also made a live version of this and a video explaining it here: https://www.youtube.com/watch?v=z_-mKcHoWwg

**Step 1**: You will only be able to use this OCR file in conjunction with screenshots of your gear. The screenshots are most easily taken in an emulator. You must set the emulator resolution to 2200x1080. LDPlayer supports this resolution, others may as well. To be clear, your compter screen doesn't need to be 2200x1080, just the emulator settings

When taking the screenshots be sure to tap on each piece of gear before screenshotting. Do not hover/hold down your finger on each one, as the placement of the item box is different between tapping and holding.

**Step 2**: Download and Install Python 3.6.1 - https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe

Important: Before you click install now, be sure that Python 3.6 is in your PATH variable

**Step 3**: Download and Install Tesseract-OCR - https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0.20190526.exe

**Step 4**: Open CMD prompt. (search -> run -> cmd)

``python -m pip install --upgrade pip``

``pip install pillow``

``pip install pytesseract``

``pip3 install opencv-python``

``pip install matplotlib``

Run each line in succession. If you get a error like 'python is not recognized', you might have forgotten to check the box when installing python, in which case, please look up how to add python to PATH or uninstall/reinstall)

**Step 5**: Download and extract the files in this repository. When you're done, click into the folder where you'll find two folders (e7 and screenshots) and two files.

Right click e7_ocr_gear_2200x1080.py and open with Notepad.
1. Make sure that ``C:/Program Files (x86)/Tesseract-OCR/tesseract`` is indeed the install location of your tesseract, if not, change that line (pytesseract.pytesseract.tesseract_cmd).
2. Similarly, change the line under it (TESSDATA_PREFIX) to match the folder location.
3. Change the next line (PATH_SCREENSHOTS) to match the location that you extracted the files from the repository. The default assumes it is on your desktop.
4. Save and exit.

After that, you add your 2200x1080 screenshots into the screenshots folder. There is an example image in there so that you know how to take it. Just open your inventory up and click the item and then take a screenshot. Make sure you delete the example screenshot so you don't find it in the optimizer.

**Step 6**: Double click on e7_ocr_gear_2200x1080.py to run it. It will go through each image, showing the current count as it goes. Once it finishes, it will export a json to the e7 folder with the name 'endure.json' and automatically close itself.

**Step 7**: Download the latest version of the optimizer here: https://github.com/Zarroc2762/E7-Gear-Optimizer/releases

Then, you simply import the json into the optimizer, add the heroes you want to optimize your gear for, and proceed.
