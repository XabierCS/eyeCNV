import sys
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
import pandas as pd
import sys
import numpy as np
import os
from PyQt5.QtGui import QImage
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg

from subprocess import Popen, PIPE

def bgzip(filename):
    """Call bgzip to compress a file."""
    Popen(['bgzip', '-f', filename])

def tabix_index(filename,
        preset="gff", chrom=1, start=4, end=5, skip=0, comment="#"):
    """Call tabix to create an index for a bgzip-compressed file."""
    Popen(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
        '-S', skip, '-c', comment])

def tabix_query(filename, chrom, start, end):
    """Call tabix and generate an array of strings for each line it returns."""
    query = '{}:{}-{}'.format(chrom, start, end)
    process = Popen(['tabix', '-f', filename, query], stdout=PIPE)
    for line in process.stdout:
        yield line.strip().split()


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))


wkdir=str(sys.argv[1])+'/'

file_name = wkdir+'visual_output_'
cnv_calls= wkdir+str(sys.argv[2])
loci_coordinates= wkdir+str(sys.argv[3])
keyFile = wkdir+str(sys.argv[4])
LRRtype = str(sys.argv[5])

print(cnv_calls)
print(loci_coordinates)

# Main Window
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.lociX="None"
        self.fname =0
        self.setWindowTitle('DeepEye')
        #self.setStyleSheet("background:rgb(100, 255, 102);")
        self.setStyleSheet("background:rgb(101, 157, 189);")

        self.outerLayout = QGridLayout()
        self.leftLayout = QVBoxLayout()
        self.RightLayout = QGridLayout()
        self.panel = QGridLayout()
        
        self.grid = QGridLayout()
       
        
        self.df= pd.read_csv(cnv_calls,sep='\t',header=0)
        self.keyFile = pd.read_csv(keyFile, sep='\t', header=0)
        self.coordinatesLoci=   pd.read_csv(loci_coordinates, sep='\t',header=0)
	###### start #######
        #### Project Name ####
        self.lbl0= QLabel("",self)
        # label1
        #self.lbl1= QLabel("Project Name",self)

        self.lbl1= QLabel("Name of the Project",self)


        #self.lbl1.setToolTip("Name for the output file")
        self.lbl1.setStyleSheet('color: white')

        # textBox1
        self.txt1= QLineEdit(self)

        # Add Button for loci
        self.lociButton = QPushButton("Select Loci")

        self.lociButton.clicked.connect(self.on_pushButton_clicked)
        self.input1 = QLineEdit()

        # Add Button for selecting file
        #self.preProjButton = QPushButton("Previous Project")

        #self.preProjButton.clicked.connect(self.on_preProjButton)

        #### Condition #### True,false,Unknow or ALL
        # label2
        self.CondL= QLabel("Condition",self)
        self.CondL.setStyleSheet('color: white')

        # text Combo box
        self.CondC= QComboBox(self)
        self.CondC.addItems(["---", "True","False","Unknown","False&Unknown","ALL"])
        self.CondC.activated[str].connect(self.condition)
        
        #### Type #### Deletion, Duplication or Both
        self.TypeL= QLabel("Type",self)
        self.TypeL.setStyleSheet('color: white')

        # text Combo box
        self.TypeC= QComboBox(self)
        self.TypeC.addItems(["---", "deletion","duplication","both"])
        self.TypeC.activated[str].connect(self.type)


        #bstart
        self.bstart = QPushButton('start', self)
        self.bstart.setToolTip('<b>start</b> CNV visualization')
        self.bstart.clicked.connect(self.start)
        self.bstart.setStyleSheet("background-color:rgb(218, 173, 134)")


        #### Panel button 
        
        #True
        self.bTrue = QPushButton('True', self)
        self.bTrue.clicked.connect(self.true)

        #False
        self.bFalse = QPushButton('False', self)
        self.bFalse.clicked.connect(self.false)

        #Unknown
        self.bUnknown = QPushButton('Unknown', self)
        self.bUnknown.clicked.connect(self.unknown)
       
        # Letmedoit
        self.bError = QPushButton('Error', self)
        self.bError.clicked.connect(self.error)


        # Letmedoit
        self.bLetme = QPushButton('Let me do it', self)
        self.bLetme.clicked.connect(self.letme)




        #bPrevious
        self.bPrev= QPushButton('< Prev', self)
        self.bPrev.clicked.connect(self.prev)

        #bNext
        self.bNext= QPushButton('Next >', self)
        self.bNext.clicked.connect(self.next)



        self.lbl2= QLabel("Graphical interface",self)
        self.leftLayout.addWidget(self.lbl1)
        self.leftLayout.addWidget(self.txt1)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.txt1)
        #self.leftLayout.addWidget(self.preProjButton)
        self.leftLayout.addWidget(self.lociButton)
        self.leftLayout.addWidget(self.input1)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.CondL)
        self.leftLayout.addWidget(self.CondC)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.TypeL)
        self.leftLayout.addWidget(self.TypeC)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.bstart)
        
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.lbl0)
        self.leftLayout.addWidget(self.lbl0)
        self.panel.addWidget(self.bTrue,1,1)
        self.panel.addWidget(self.bFalse,0,1)
        self.panel.addWidget(self.bUnknown,2,1)
        self.panel.addWidget(self.bError,3,1)
        self.panel.addWidget(self.bLetme,4,1)
        self.panel.addWidget(self.bPrev,1,0)
        self.panel.addWidget(self.bNext,1,2)
        
        self.leftLayout.addLayout(self.panel)

        self.leftLayout.addWidget(self.lbl2)
        self.leftLayout.addStretch()
        #self.leftLayout.setVerticalSpacing(1)

        ##### Ploting Layout #####

        self.pixmap = QPixmap('meta/theme1.jpg')
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.RightLayout.addWidget(self.label)

        self.outerLayout.addLayout(self.leftLayout,0,0) # Nesting layout
        self.outerLayout.addLayout(self.RightLayout,0,1) # Nesting layout
        #self.RightLayout.setColumnStretch(0,1)
        self.setLayout(self.outerLayout)  
    

    ### Functions ###

    def mergePath (self,working, pathX):
      ''' Function to map and get full paths for raw intensity files
          working: path for working directory
          pathX: relative path of raw intensity files'''
      for pathX1 in pathX:
        if pathX1 in working:
          break
      pos=working.index(pathX1)
      pathFullp=working[:pos]+pathX[1:]
      pathFull='/'.join(pathFullp)
      return(pathFull)


    def getCNVarray(self,cnv):
      print( 'Sample to Query:')
      print(cnv)
      sampleX=cnv
      #chrX= cnv.chr.replace('chr', '')
      chrX= cnv.chr
      startX= cnv.start
      stopX= cnv.end
      # map the id to file path
      idX=(cnv.sample_ID)
      print('chr CNV:')
      print(chrX)

      cnvSample=self.keyFile.loc[self.keyFile['sample_ID'].isin([idX])]
      print("Mapped cnvSample Key file:")
      print(cnvSample)
      pathFull= cnvSample.file_path_tabix.tolist()[0]
      #wd=os.getcwd()
      #wd2=wd.split('/')
      #path2=sampleName.split('/')
      #print('########Path 2 is:')
      #print(path2)
      #pathFull=self.mergePath(wd2,path2)
      print(pathFull)

      try: 
        SampleRaw = pd.DataFrame(tabix_query(pathFull,str(chrX), 0, int(250e6))) # To get the entire chr
        print('Sample with succesfull tabix file: '+ pathFull)
        SampleRaw = SampleRaw.astype(float) # Deal with NaN by changing type to float
      except:
        print('Cannot print sample')
        print('Error file'+pathFull)
        self.plotError()
      
      if LRRtype == 'GC_NO':
        SampleRaw=SampleRaw.rename({0:'chr',1:'Pos',2:'Pos2',3:'LRR',4:'BAF',5:'LRRt'},axis=1)
		

      if LRRtype == 'GC_YES':
        SampleRaw=SampleRaw.rename({0:'chr',1:'Pos',2:'Pos2',3:'LRRt',4:'BAF',5:'LRR'},axis=1)
		
      SampleRaw=SampleRaw.dropna(axis=0, thresh=1) # Remove rows with any columns with NaN
      print('testing............')
      print(SampleRaw)      
      SampleRaw.Pos=SampleRaw.Pos.astype(float)
      cnvRegion=SampleRaw.loc[SampleRaw['Pos'].isin(range(startX,stopX))]
      print('pass1')
      cnvRegion[['Status']]=1
      extend= (1000-cnvRegion.shape[0])//2
      print('pass2')
      pre=SampleRaw.loc[SampleRaw['Pos']<startX].tail(extend)
      pos=SampleRaw.loc[SampleRaw['Pos']>stopX].head(extend)
      pre[['Status']]=0
      pos[['Status']]=0
      print('pass3')
      cnvArray=pd.concat([pre,cnvRegion,pos])
      cnvArray= cnvArray.reset_index() 
      print(list(cnvArray.Pos))
      print('pass4')
      cnvArray[['locus']]= str(cnv.locus)
      cnvArray.loc[(cnvArray.LRR == 'NaN'),'LRR']='0'
      cnvArray.loc[(cnvArray.BAF == 'NaN'),'BAF']='0'
      print('pass5')
      print(cnvArray[["LRR", "BAF"]] )
      cnvArray[["LRR", "BAF"]] = cnvArray[["LRR", "BAF"]].apply(pd.to_numeric)
      print('pass6')
      cnvArray.loc[(cnvArray.LRR > 1),'LRR']=0.99
      print('pass7')
      cnvArray.loc[(cnvArray.LRR < -1.5),'LRR']= -1.5
      print('pass8')
      print('xabi test 1')
      print(cnvArray)
      return(cnvArray)



    # Button to access loci 
    def on_pushButton_clicked(self):
        self.w2 = Loci_options()
        self.input1.setText(self.lociX)
        self.w2.show()


    def on_preProjButton(self):
        print('Selecting own project')
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"")[0]
        print(self.fname)



    def newLoci(self):
        self.input1.setText(self.lociX)

    def type(self, text):
        self.selected_type = text

    def condition(self, text):
        self.selected_condition = text

    def type(self, text):
        self.selected_type = text

    def plotError(self):
        self.outerLayout.itemAt(1).itemAt(1).widget().deleteLater()
        self.outerLayout.itemAt(1).itemAt(2).widget().deleteLater()
        self.pixmap = QPixmap('meta/error1.jpg')
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap.scaled(900,600))
        self.RightLayout.addWidget(self.label)

    def PlotSample(self,cnvArray,start1=False):# ew=self.df2.loc[1]
        self.cnvX= cnvArray
        locusX= self.cnvX['locus'].iloc[0]
        locusXcoor= self.coordinatesLoci.loc[self.coordinatesLoci['locus']== locusX]
        region=self.cnvX.loc[self.cnvX['Pos'].isin(range(locusXcoor['start'].iloc[0],locusXcoor['end'].iloc[0]))]
        
        regionMin=locusXcoor.start.astype(float)
        regionMax=locusXcoor.end.astype(float)
        LRR= self.cnvX.LRR.to_numpy().astype(float)
        BAF= self.cnvX.BAF.to_numpy().astype(float)
        

  
        # CNV reg
        cnvReg= self.cnvX.loc[self.cnvX['Status'].isin([1])]
        cnvRegIndx=cnvReg.index.tolist()
        cnvRegPos= cnvReg.Pos.to_numpy().astype(float)
        self.cnvRegPos=cnvRegPos
        LRRreg= cnvReg.LRR.to_numpy().astype(float)
        BAFreg= cnvReg.BAF.to_numpy().astype(float)

        # CNV out
        cnvOut= self.cnvX.loc[self.cnvX['Status'].isin([0])]
        cnvOutIndx=cnvOut.index.tolist()
        cnvOutPos= cnvOut.Pos.to_numpy().astype(float)
        LRROut= cnvOut.LRR.to_numpy().astype(float)
        BAFOut= cnvOut.BAF.to_numpy().astype(float)
        #self.pixmap = QPixmap('/home/xavcal/recurrent_cnvs/people/misc/DeepEye/DeepEye_v2/meta/eye2.jpg')
        #self.label = QLabel(self)
        #self.label.setPixmap(self.pixmap)


        if start1==False:
          # Remove intro image 

          for i in (range(self.outerLayout.itemAt(1).count())): 
            self.outerLayout.itemAt(1).itemAt(i).widget().deleteLater()
          #self.outerLayout.itemAt(1).itemAt(0).widget().deleteLater() 
          # Create & add Progress Bar
          self.pbar = QProgressBar(self)
          self.pbar.setValue(0)
          self.pbar.setGeometry(30, 40, 200, 25)
          self.RightLayout.addWidget(self.pbar)


        if start1==True:
          # Remove old widgets: previous plot and label

          for i in (range(1,self.outerLayout.itemAt(1).count())): 
            self.outerLayout.itemAt(1).itemAt(i).widget().deleteLater()

          #self.outerLayout.itemAt(1).itemAt(1).widget().deleteLater()
          #self.outerLayout.itemAt(1).itemAt(2).widget().deleteLater()
          # Update meta data
          self.pbar.setValue(int(100*(self.x/self.last))) # Progression bar
        
        # Create X-th CNV plot
        self.obj1 = pg.PlotWidget()

        self.obj1.plotItem.setMouseEnabled(y=False)
        self.obj1.showGrid(x=True, y=True, alpha=0.4)
        minV= np.nanmin(LRR) # select min value for plotting limints
           
        # Draw rectangle for locus area
        #r = pg.QtGui.QGraphicsRectItem(regionMin,minV-0.1, regionMax-regionMin, 2.3-minV) # Add rectangle where loci is
        r = pg.QtGui.QGraphicsRectItem(regionMin,minV-0.1, regionMax-regionMin, 2.3-minV) # Add rectangle where loci is
        
        r.setPen(pg.mkPen((115, 216, 153))) # Color for the rectangle
        self.obj1.addItem(r)
        self.obj1.resize(2000, 4000)
          
        # Plot intensity values
        self.obj1.plot(cnvOutPos,BAFOut+1, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(40, 20, 255, 200) ) # Out BAF
        self.obj1.plot(cnvOutPos,LRROut, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(40, 20, 255, 200))    # Out LRR
        self.obj1.plot(cnvRegPos,BAFreg+1, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(204, 51, 0, 220) )  # Incnv BAF
        self.obj1.plot(cnvRegPos,LRRreg, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(204, 51, 0, 220))     # Incnv LRR
        self.obj1.setYRange(minV, 2.05, padding=0) # plot winwod limits 
        self.obj1.setXRange(cnvRegPos[0]-2e6, cnvRegPos[-1]+2e6, padding=0) # plot winwod limits 
        #reg = pg.LinearRegionItem()
        #reg.setZValue(100)
        #self.obj1.addItem(reg, ignoreBounds=True)
        # Counter
        stringX= str(self.df2.Visual_Output.shape[0])
        self.lbl1= QLabel(str(self.x+1)+ ' out of '+ stringX+' Samples --- CNV type: '+str(self.df2.CN[self.x])+ ' -- locus: '+self.df2.locus[self.x],self)   # Create label
        self.lbl1.setStyleSheet("background-color: rgb(237, 245, 225)")
        self.RightLayout.addWidget(self.lbl1)   # Add label
        self.RightLayout.addWidget(self.obj1)  # Add plot     
        self.RightLayout.setColumnStretch(0,10)
        #reg.sigRegionChanged.connect(self.update)




    def start(self):
        

        if self.fname ==0:
	        #1 
	        self.path_save=file_name+self.txt1.text()+'.txt'
	        selectedLoci= pd.read_csv('loci_Sel.txt',sep='\t',header=None)
	        selectedLoci= selectedLoci.iloc[:,0].tolist()
	        #df2=self.df.query('locus in @selectedLoci')


	        typee= [self.selected_type]
	        if typee[0]== "both":
	            typee=[1,3]
	        if typee[0]=='deletion':
	        	typee=[1]
	        if typee[0]=='duplication':
	        	typee=[3]


	        condition= (self.selected_condition)
	        if condition=="True":
	            condition=['1']
	        if condition=="False":
	            condition=['2']
	        if condition=="Unknown":
	            condition=['3']
	        if condition=="ALL":
	            condition=['1','2','3']
	        if condition=="False&Unknown":
	            condition=['2','3']
	       
	        condition=list(map(int, condition))

	        self.x= 0
	        #self.df2= self.df.loc[self.df['locus'].isin(selectedLoci) & self.df['Visual'].isin(condition) & self.df['Type'].isin(typee)]
	        self.df2= self.df.loc[self.df['locus'].isin(selectedLoci) & self.df['CN'].isin(typee)]
	        self.df2=self.df2.reset_index()
	        self.df2[['Visual_Output']]=-9
	        self.last= self.df2.shape[0]
	        print('Dataframe to check for CNVs:')
	        print(self.df2)

	        
        if self.fname !=0:
          self.path_save=self.fname
          self.df= pd.read_csv(self.fname,sep='\t',header=0)
          self.df2a= self.df.loc[self.df['Visual_Output']== -9]
          self.df2b= self.df.loc[self.df['Visual_Output']!= -9]
          self.df2 = pd.concat([self.df2b,self.df2a])
          self.df2=self.df2.reset_index()
          self.last= self.df2.shape[0]
          self.x=  self.df2b.shape[0]



        #2. Tabix first sample 
        print(self.df2.loc[self.x])
        self.cnvX= self.getCNVarray(self.df2.loc[self.x])
        print('Check first array for ploting:')
        print(self.cnvX)

        #3. Plot first sample
        self.PlotSample(self.cnvX)

    def Iter(self):
        #1. Move to next sample
        self.x= self.x + 1
        self.df2.to_csv(self.path_save, sep='\t')
        #2. write to data frame TODO 
        if self.x == self.last:
           
          
           self.pbar.setValue(int(100*(self.x/self.last))) # Progression bar
           # Remove old widgets: previous plot and label
           self.outerLayout.itemAt(1).itemAt(1).widget().deleteLater()
           self.outerLayout.itemAt(1).itemAt(2).widget().deleteLater()
           self.pixmap = QPixmap('meta/bye2.jpg')
           os.system('rm -R loci_Sel.txt')
           self.label = QLabel(self)
           self.label.setPixmap(self.pixmap.scaled(900,600))
           self.RightLayout.addWidget(self.label)
           # 2a.1. Plot bye image
        if self.x != self.last: 
           # 2b.1. Tabix xth sample 
           self.cnvX= self.getCNVarray(self.df2.loc[self.x])
           print('Check samples data frame')
           print(self.df2)
           # 2b.2. Plot xth sample
           self.PlotSample(self.cnvX, start1=True)


    def true(self):
        self.df2.Visual_Output[self.x]=1
        self.Iter()

    def false(self):
        self.df2.Visual_Output[self.x]=2
        self.Iter()

    def unknown(self):
        self.df2.Visual_Output[self.x]=3
        self.Iter()

    def error(self):
        self.df2.Visual_Output[self.x]=-7
        self.Iter()

    def letme(self):
        # Yea
        self.bYea = QPushButton('Yeah', self)
        self.bYea.clicked.connect(self.yea)

        self.reg = pg.LinearRegionItem()
        self.reg.setZValue(100)
        #self.obj1.setXRange(10, 110, padding=0)

        self.reg = pg.LinearRegionItem(values=(self.cnvRegPos[0],self.cnvRegPos[-1]))
        self.obj1.addItem(self.reg, ignoreBounds=True)
        self.panel.addWidget(self.bYea,4,1)
        self.bYea.clicked.connect(self.bYea.deleteLater)
        #self.df2.Visual_Output[self.x]=3
        #self.Iter()

    def yea(self):
        self.reg.setZValue(10)
        minX, maxX = self.reg.getRegion()
        minX, maxX = int(minX), int(maxX)
        print('update loop')
        print(minX, maxX)
        print(self.cnvX)
        print('Checking old self.df2:')
        print(self.df2)
        yeaCNV=pd.DataFrame([self.df2.loc[self.x]])
        yeaCNV[["start", "end"]] = yeaCNV[["start", "end"]].apply(pd.to_numeric)
        yeaCNV.start=minX
        yeaCNV.end=maxX
        yeaCNV.Visual_Output=1
        
        print(yeaCNV)
        self.df2 = pd.concat([self.df2.iloc[:(self.x+1)],yeaCNV, self.df2.iloc[(self.x+1):]]).reset_index(drop=True)
        self.df2=self.df2.reset_index(drop=True)
        self.df2[["start", "end"]] = self.df2[["start", "end"]].apply(pd.to_numeric)
        #self.df2.loc[self.x] = yeaCNV  # adding a row
        #self.df2.index = self.df2.index + 1  # shifting index
        #self.df2 = self.df2.sort_index()  # sorting by index
        self.last= self.df2.shape[0]
        self.df2.Visual_Output[self.x]=-8
        print('Checking new self.df2:')
        print(self.df2)
        self.x=self.x+1
        print('Delete button')
        
        self.Iter()

    def prev(self):
        self.x=self.x -2
        self.Iter()

    def next(self):
        self.Iter()

    def displayInfo(self,loci):
        #self.input1.setText('Xabi')
        #self.grid.addWidget(self.input1)
        print(self.newLoci())
        print(loci)
        self.lociX=loci
        #self.show()

  

# Loci Window
class Loci_options(QWidget):
    def __init__(self, parent=None):
        super(Loci_options, self).__init__(parent)
        self.MainWIndow = Window()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.setStyleSheet("background:rgb(251, 238, 193);")
        self.mainWindow = Window()
        df= pd.read_csv(cnv_calls,sep='\t',header=0)
        loci=df.locus.unique()
        self.loci=loci
        rows=round(1+(len(loci)//2)*0.4)
        columns=round(1+(len(loci)//2)*0.6)+1
        if len(loci)==1:
        	rows=2
        	columns=2
        positions = [(i, j) for i in range(rows) for j in range(columns)]

        for position, name in zip(positions, loci):
            if name == '':
                continue
            self.checkbox = QCheckBox(name)
            self.checkbox.setCheckState(Qt.Unchecked)
            self.grid.addWidget(self.checkbox, *position)

        self.setWindowTitle('Loci')

 
        self.label  = QLabel("   ")
        self.button = QPushButton("Query Loci")
        self.button.clicked.connect(self.ButtonClicked)
        self.button.clicked.connect(self.passingInformation)

        self.grid.addWidget(self.label,*positions[-2])
        self.grid.addWidget(self.button,*positions[-1])
  

    def ButtonClicked(self):
        self.checked_list = []

        for i in range(self.grid.count()):
            chBox = self.grid.itemAt(i).widget()
            if(isinstance(chBox,QCheckBox)):
            	if chBox.isChecked():
            	    self.checked_list.append(chBox.text())
        print(self.checked_list)
        os.system('rm -R loci_Sel.txt') # remove file with  
        with open('loci_Sel.txt', 'a') as the_file:
          the_file.write('\n'.join(self.checked_list))
          the_file.write("\n")
        #return(checked_list)
        self.close()

    def passingInformation(self):
        #self.mainWindow.input1.setText(np.array2string(self.loci))
        self.mainWindow.txt1.setText('Xabiiier')
        self.mainWindow.displayInfo(self.loci)




GUI = None
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())
