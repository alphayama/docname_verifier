# Document Name Verifier

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


