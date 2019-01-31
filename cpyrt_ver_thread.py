import os
import sys

import fitz
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

# Qt GUI python script
from cpyrt_gui import Ui_MainWindow


#ImageWidget class: Used for displaying image in QTableWidget table cell
class ImageWidget(QtWidgets.QLabel):

    def __init__(self,imagePath, parent=None):
        super(ImageWidget, self).__init__(parent)
        pic = QtGui.QPixmap(imagePath)
        self.setPixmap(pic)

class PdfToImg(QtCore.QThread):

    sig=pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self,parent=None)

    def pdf_to_image(self):
        ctr=-1	#iterator to count image files and use them as row no.
        curr_file=''    #current file path
        self.ui.tableWidget.setCursor(QtCore.Qt.BusyCursor)
        self.ui.progressBar.setMaximum(len(os.listdir(self.filename)))
        for files in os.listdir(self.filename):
            if files.split('.')[1]=='pdf':
                ctr+=1
                doc=fitz.open(self.filename+'/'+files)
                for img in doc.getPageImageList(0):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:       # this is GRAY or RGB
                        pix.writePNG(self.filename+"/pg1_temp.png")
                    else:               # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.writePNG(self.filename+"/pg1_temp.png")
                        pix1 = None
                    pix = None
                image=Image.open(self.filename+'/pg1_temp.png')
                image=image.resize((850,1400),Image.ANTIALIAS) 
                year=files.split('.')[0].split('=')[1].split('-')[0].split('(')[0]
                year=int(year)
                if year<=59:
                    box=[350,120,680,420]
                elif year<=63:
                    box=[380,360,620,580]
                elif year<=70:
                    box=[390,150,610,370]
                elif year<=72:
                    box=[320,350,740,460]       #[left,top,right,bottom]
                elif year<=81:
                    box=[370,160,720,460]
                elif year>=84 and year<=90:
                    box=[390,120,750,460]
                elif year==91:
                    box=[400,290,730,600]
                elif year>=96 and year<=2013:
                    box=[410,160,600,310]                          
                elif year>=2014 and year<=2017:
                    box=[400,340,660,500]
                else:                           
                    box=[400,160,730,460]
                curr_file=self.filename+"/temp.png"
                image.crop(box).resize((300,200), Image.ANTIALIAS).save(curr_file)
                print(ctr) 
                curr_img = ImageWidget(curr_file)
                self.ui.tableWidget.insertRow(ctr)
                self.ui.tableWidget.setRowHeight(ctr,200)
                self.ui.tableWidget.setCellWidget(ctr, 0, curr_img)
        self.ui.tableWidget.unsetCursor()
        #clean up temporary files  
        os.remove(self.filename+'/pg1_temp.png')
        os.remove(curr_file)
        print('Complete!') #back-end console output

#MainWindow class: The GUI is defined in this class
class MainWindow(QtWidgets.QMainWindow):
    
    sig=pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()    #Qt window object
        self.ui.setupUi(self)
        self.setWindowTitle('Copyright Verifier')   #set window title
        self.filename=''

        #set column width of table
        self.ui.tableWidget.setColumnWidth(0,300)
        self.ui.tableWidget.setColumnWidth(1,200)
        self.ui.tableWidget.setColumnWidth(2,200)
        #Set progress bar value to 0
        self.ui.progressBar.setValue(0)
        #Exit program
        self.ui.actionExit.triggered.connect(self.close)
        #Open folder
        self.ui.actionOpen.triggered.connect(self.file_open_folder)
        #Show version
        self.ui.actionVersion.triggered.connect(self.info_version)

        # self.ui.tableWidget.setItem(0,0,QtWidgets.QTableWidgetItem(filename))

    def file_open_folder(self):  #open folder function
        directory=QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.Directory)
        self.filename=directory.getExistingDirectory()
        if self.filename:
            self.pdf2img=PdfToImg()
            self.connect(self.pdf2img,QtCore.SIGNAL('self.pdf2img.pdf_to_image()'),self.pdf2img.pdf_to_image())
            self.pdf2img.start()


    def info_version(self):
        QtWidgets.QMessageBox.about(self,"Version","Version 1.0.0")

    

#Main code
app = QtWidgets.QApplication([])
application = MainWindow() 
application.show()
sys.exit(app.exec())
