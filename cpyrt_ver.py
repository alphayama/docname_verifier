from PyQt5 import QtWidgets,QtCore, uic,QtGui
import sys,os
import fitz
from PIL import Image
from shutil import copy2

# Qt GUI python script
from cpyrt_gui import Ui_MainWindow

#ImageWidget class: Used for displaying image in QTableWidget table cell
class ImageWidget(QtWidgets.QLabel):

    def __init__(self,imagePath, parent=None):
        super(ImageWidget, self).__init__(parent)
        pic = QtGui.QPixmap(imagePath)
        self.setPixmap(pic)

#MainWindow class: The GUI is defined in this class
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()    #Qt window object
        self.ui.setupUi(self)
        self.setWindowTitle('Copyright Verifier')   #set window title
        self.dir_name=''
        self.ui.nextButton.setEnabled(False)
        #set column width of table
        self.ui.tableWidget.setColumnWidth(0,300)
        self.ui.tableWidget.setColumnWidth(1,200)
        self.ui.tableWidget.setColumnWidth(2,200)
        #Exit program
        self.ui.actionExit.triggered.connect(self.closeEvent)
        #Open folder
        self.ui.actionOpen.triggered.connect(self.file_open_folder)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"),self).activated.connect(self.file_open_folder)
        #Show version
        self.ui.actionVersion.triggered.connect(self.info_version)
        #Save File
        self.ui.actionSave_Changes.triggered.connect(self.next_batch)
        # Save and load next batch
        self.ui.nextButton.clicked.connect(self.next_batch)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"),self).activated.connect(self.next_batch)
    
    #this function increments batch no.
    def next_batch(self):
        self.save_transfer()
        for i in reversed(range(self.ui.tableWidget.rowCount())):
            self.ui.tableWidget.removeRow(i)
        self.batch_no+=1
        if self.batch_no>=len(self.batches):
            self.ui.nextButton.setEnabled(False)
            QtWidgets.QMessageBox.information(self,"Finished","This was the last batch. \nChanges were saved")
        else:
            self.pdf_to_image()
        
    #   This function opens a folder which contains the files
    #   and also divides the pdf files into batches
    def file_open_folder(self):  #open folder function
        directory=QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.Directory)
        self.dir_name=directory.getExistingDirectory()
        if self.dir_name:
            self.file_list=os.listdir(self.dir_name)
            self.pdf_list=[]
            for files in os.listdir(self.dir_name):
                if files.split('.')[1]=='pdf':
                    self.pdf_list.append(files)
            self.batches = [self.pdf_list[x:x+3] for x in range(0, len(self.pdf_list), 3)]
            self.batch_no=0
            self.ui.nextButton.setEnabled(True)
            self.pdf_to_image()
            
    #version information
    def info_version(self):
        QtWidgets.QMessageBox.about(self,"Version","Version 1.0.0")

    #this function uses pymupdf library to open PDFs and convert their first page to image.
    #image localization is performed
    def pdf_to_image(self):
        self.p2i_iter=-1	#iterator to count image files and use them as row no.
        curr_img=''    #current file path
        self.ui.tableWidget.setCursor(QtCore.Qt.BusyCursor)
        for files in self.batches[self.batch_no]:
            self.p2i_iter+=1
            doc=fitz.open(self.dir_name+'/'+files)
            for img in doc.getPageImageList(0):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG(self.dir_name+"/pg1_temp.png")
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(self.dir_name+"/pg1_temp.png")
                    pix1 = None
                pix = None
            image=Image.open(self.dir_name+'/pg1_temp.png')
            image=image.resize((850,1400),Image.ANTIALIAS) 
            year=files.split('.')[0].split('=')[1].split('-')[0].split('(')[0]
            year=int(year)
            if year<=59:
                self.box=[350,120,680,420]
            elif year<=63:
                self.box=[380,360,620,580]
            elif year<=70:
                self.box=[390,150,610,370]
            elif year<=72:
                self.box=[320,350,740,460]       #[left,top,right,bottom]
            elif year<=81:
                self.box=[370,160,720,460]
            elif year>=84 and year<=90:
                self.box=[390,120,750,460]
            elif year==91:
                self.box=[400,290,730,600]
            elif year>=96 and year<=2013:
                self.box=[410,160,600,310]                          
            elif year>=2014 and year<=2017:
                self.box=[400,340,660,500]
            else:                           
                self.box=[400,160,730,460]
            #self.box=[350,120,750,600]
            self.new_dir=self.dir_name+'/../'+self.dir_name.split('/')[-1]+'_corrected'
            if not os.path.exists(self.new_dir):
                os.mkdir(self.new_dir)
            curr_img=self.new_dir+"/regno_"+files.split('.')[0]+".png"
            image.crop(self.box).resize((300,200), Image.ANTIALIAS).save(curr_img)
            self.out_img_fname(curr_img,files.split('.')[0],self.p2i_iter)
        self.no_of_files=self.p2i_iter+1	    #saves no. of files
        self.ui.tableWidget.unsetCursor()

    #outputs localized regions and filenames to tabel cells
    def out_img_fname(self,img_path,file_name,iter):
        image = ImageWidget(img_path)
        self.ui.tableWidget.insertRow(iter)
        self.ui.tableWidget.setRowHeight(iter,200)
        self.ui.tableWidget.setCellWidget(iter, 0, image)
        self.ui.tableWidget.setItem(iter,1,QtWidgets.QTableWidgetItem(str(file_name)))
        self.ui.tableWidget.setItem(iter,2,QtWidgets.QTableWidgetItem(str(file_name)))

    #saves and transfers files
    def save_transfer(self):
        for i in range(0,self.no_of_files):
            copy2(self.dir_name+'/'+self.batches[self.batch_no][i],self.new_dir+"/"+self.ui.tableWidget.item(i,2).text()+'.pdf')
            os.remove(self.dir_name+'/'+self.batches[self.batch_no][i])
            
    def closeEvent(self,event):
        os.remove(self.dir_name+'/pg1_temp.png')
        event.accept()

#Main code
app = QtWidgets.QApplication([])
application = MainWindow() 
application.show()
sys.exit(app.exec())