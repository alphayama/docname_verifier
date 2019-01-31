import fitz
from PIL import Image
import os


#doc = fitz.open("file2.pdf")
# for i in range(len(doc)):
#     for img in doc.getPageImageList(i):
#         xref = img[0]
#         pix = fitz.Pixmap(doc, xref)
#         if pix.n < 5:       # this is GRAY or RGB
#             pix.writePNG("p%s-%s.png" % (i, xref))
#         else:               # CMYK: convert to RGB first
#             pix1 = fitz.Pixmap(fitz.csRGB, pix)
#             pix1.writePNG("p%s-%s.png" % (i, xref))
#             pix1 = None
#         pix = None
path='/home/alphrho/Documents/sample_copyright_files/cats/8490/'
for files in os.listdir(path):
    if files.split('.')[1]=='pdf':
        doc=fitz.open(path+files)
        for img in doc.getPageImageList(0):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                # pix.writePNG(path+"pg1_temp.png")
                image=pix.getPNGData()
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                # pix1.writePNG(path+"pg1_temp.png")
                image=pix1.getPNGData()
                pix1 = None
            pix = None
        # image=Image.open(path+'pg1_temp.png')
        image=image.resize((850,1400),Image.ANTIALIAS) #.save(files.split('.')[0]+".png")
        year=files.split('.')[0].split('=')[1].split('-')[0].split('(')[0]
        #print(year)  
        year=int(year)
        #crop=(300,100)
        #print(year," , ",year//10)
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
        #     crop=(300,300)
        image=image.crop(box).resize((330,300), Image.ANTIALIAS) #.save(path+"regno_"+files.split('.')[0]+".png")
print('Complete!')

