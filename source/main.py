#!/usr/bin/python
# -*- coding: utf-8 -*-


import aalib
import Image
import urllib2
from cStringIO import StringIO
import string
import webbrowser

import sys, os
from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        self.picturePath = ''
        self.style = "color:white; background-color:black; font-family:'Courier'; font-style:normal; "
        self.fontSize = 11
        self.initUI()
        
        
    def initUI(self):    
    
        
        loadb = QtGui.QPushButton(u'Načti obrázek', self)
        loadb.move(30, 5)
        loadb.pressed.connect(self.loadPicture)
        
        saveb = QtGui.QPushButton(u'Export do TXT', self)
        saveb.move(140, 5)
        saveb.resize(150,30)
        saveb.pressed.connect(self.exportToTXT)
        
        saveb = QtGui.QPushButton(u'Export do HTML', self)
        saveb.move(300, 5)
        saveb.resize(150,30)
        saveb.pressed.connect(self.exportToHTML)
        
        openb = QtGui.QPushButton(u'Zobrazit v prohlížeči', self)
        openb.move(460, 5)
        openb.resize(150,30)
        openb.pressed.connect(self.showInBrowser)
        
        button = QtGui.QPushButton(u'Zobraz original', self)
        button.move(500, 40)
        button.resize(150,30)
        button.pressed.connect(self.showOriginal)
        
        plus = QtGui.QPushButton(u'+', self)
        plus.move(220, 40)
        plus.pressed.connect(self.zoomIn)
        
        minus = QtGui.QPushButton(u'-', self)
        minus.move(320, 40)
        minus.pressed.connect(self.zoomOut)
        
        lbl1 = QtGui.QLabel(u'Šířka:', self)
        lbl1.move(15, 40)
        self.width = QtGui.QLineEdit(self)
        self.width.move(60, 40)
        self.width.resize(40,30)
        self.width.insert("50")
        self.width.textChanged.connect(self.renderPicture)
        
        
        lbl2 = QtGui.QLabel(u'Výška:', self)
        lbl2.move(120, 40)
        self.height = QtGui.QLineEdit(self)
        self.height.move(170, 40)
        self.height.resize(40,30)
        self.height.insert("30")
        self.height.textChanged.connect(self.renderPicture)
        
        self.picture = QtGui.QTextEdit(u'Malý tip: Pokud je obrázek při velkém rozlišení např: 800x200 znaků, moc tmavý,\
                                        tak si jej můžeš zobrazit v prohlížeči a pomocí ctrl+kolečko myši jej zesvětlíš', self)
        self.picture.move(30, 80)
        self.picture.resize( 700, 500 )
        self.picture.setStyleSheet("QTextEdit {"+self.style+"}")
        
        
        self.setGeometry(150, 150, 800, 600)
        self.setWindowTitle(u'Převodník obrázků na znaky')
        self.show()
        
    def showOriginal(self):
        if (self.picturePath != ''):
            image = Image.open(self.picturePath).show()
        
    def showInBrowser(self):
                        
        picture = string.replace(self.picture.toHtml(), "font-style:normal;", self.style)
        path = os.path.join(os.getcwd(), "temp", "picture.html")
        f = open(path,'w')
        f.write(picture)
        f.close()
        webbrowser.open(path,new=2)
        
    def exportToTXT(self):
        savePath = unicode(QtGui.QFileDialog.getSaveFileName(self, u'Ulož ASCII obrázek',
                        '.txt', self.tr("file (*.txt)")))
        
        f = open(savePath,'w')
        f.write(self.picture.toPlainText())
        f.close()
        
    def exportToHTML(self):
        
        savePath = unicode(QtGui.QFileDialog.getSaveFileName(self, u'Ulož ASCII obrázek jako HTML stránku',
                        '.html', self.tr("file (*.html)")))
                        
        picture = string.replace(self.picture.toHtml(), "font-style:normal;", self.style)
        
                        
        f = open(savePath,'w')
        f.write(picture)
        f.close()
        
        
        
    def zoomIn(self):
        self.picture.zoomIn()
        self.show()
        self.fontSize += 1
        
    def zoomOut(self):
        self.picture.zoomOut()
        self.show()
        self.fontSize -= 1
        
    def loadPicture(self):
        self.picturePath = unicode(QtGui.QFileDialog.getOpenFileName(self, u'Načti obrázek',
                        '', self.tr("Image files (*.bmp *.png *.jpg *.jpeg *.gif)")))
        self.renderPicture()
    
    def renderPicture(self):
        screen = aalib.AsciiScreen(width=int(self.width.text()), height=int(self.height.text()))
        image = Image.open(self.picturePath).convert('L').resize(screen.virtual_size)
        screen.put_image((0, 0), image)
        self.picture.setText(screen.render())
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
