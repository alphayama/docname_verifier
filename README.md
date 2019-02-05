# Document Name Verifier

This is a small project that I worked upon while doing my internship. The organization had done OCR on some documents where the output was a PDF document with recognized text and the Registration no. of a document was their filename. However, some of the registeration nos. were recognized incorrectly, hence, the filename was wrong too. <br><br>
After observations, location of registration no. on the document was found to be in a particular region for a period of time. Using this information, image localization was performed to get a cropped area of first page of each document.<br><br>
This program takes a directory containing PDFs as input and then performs:<br>
1. Image localization to get the cropped area
2. User manually checks and corrects the registration no. if wrong
3. At a time, only 3 entries are shown. The documents are divided into batches each containing 3 files
4. Changes are saved after user moves on to next batch
5. The files are renamed and moved to a new folder. Localized images are also saved.

## Requirements
- Python 3
- Any OS that supports Python _3_ and following libraries.

### Python _3_  libraries
- PyQt5 <br>
- PyMuPDF
- Pillow (PIL)

Install using :    `pip install -u requirements.txt` <br><br>
_Note: It is recommended to use Python virtual environments like venv and conda environments_

## Run Program
General:<br>
`python docname_verif.py`
<br><br>
Linux and macOS may have Python 2 as default, then use:<br>
`python3 docname_verif.py`


## Main files in this repository
1. _docname_verif.pdf_ <br>
This is the main code. It contains the back-end of the program. <br><br>
2. _docver_gui.py_ <br>
Qt User Interface file (.ui) was converted to Python3 code using pyuic5. This utility converts .ui files to .py. This Python code serves as the front-end of the program.<br><br>
3. _docver_gui.ui_ <br>
Although not required by the program, it is included if UI needs to be changed using Qt Designer/Creator instead of modifying the python script.

## Problems
The program is a bit slow which was an unpleasant experience.


