import sys
from os import system
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from hurry.filesize import *

from ui import Ui_trimage

class StartQT4(QMainWindow):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.ui = Ui_trimage()
    self.ui.setupUi(self)
    self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"),  self); # todo use standardKey Quit.
    # set recompress to false
    self.ui.recompress.setEnabled(False)
    self.imagelist = []

    # connect signals with slots
    QObject.connect(self.ui.addfiles, SIGNAL("clicked()"), self.file_dialog)
    QObject.connect(self.ui.recompress, SIGNAL("clicked()"), self.recompress_files)
    QObject.connect(self.quit_shortcut, SIGNAL("activated()"), qApp, SLOT('quit()'))
    QObject.connect(self.ui.processedfiles, SIGNAL("dragEnterEvent()"), self.file_drop)

  def file_drop(self):
    print "booya"

  def file_dialog(self):
    fd = QFileDialog(self)
    images = fd.getOpenFileNames(self,
                                 "Select one or more image files to compress",
                                 "", # directory
                                 "Image files (*.png *.gif *.jpg)")
    for image in images:
      self.compress_file(image)


  def enable_recompress(self):
    self.ui.recompress.setEnabled(True)


  def recompress_files(self):
    newimage = self.imagelist
    self.imagelist = []
    for image in newimage:
      self.compress_file(image[-1])


  def compress_file(self, filename):
    print filename
    oldfile = QFileInfo(filename);
    name = oldfile.fileName()
    oldfilesize = oldfile.size()

    if name.endsWith("jpg"):
      print "run jpegoptim"
      runfile = system('ls')

    elif name.endsWith("png"):
      runstr = 'optipng -force "' + str(filename) + '"'
      runfile = system(runstr)

    else:
      print "run something for gif"
      runfile = system('ls')


    if runfile == 0:
      newfile = QFile(filename)
      newfilesize = newfile.size()
      newfilesizestr = size(newfilesize, system=alternative)

      ratio = 100 - (float(newfilesize) / float(oldfilesize) * 100)
      ratiostr = "%.1f%%" % ratio

      self.imagelist.append((name, newfilesizestr, ratiostr, filename))
      self.update_table()

    else:
      print "uh. not good" #implement, something went wrong


  def update_table(self):
    tview = self.ui.processedfiles

    # set table model
    tmodel = tri_table_model(self,
                             self.imagelist,
                             [' Filename ', ' Size ', ' Compressed '])
    tview.setModel(tmodel)

    # set minimum size of table
    vh = tview.verticalHeader()
    vh.setVisible(False)

    # set horizontal header properties
    hh = tview.horizontalHeader()
    hh.setStretchLastSection(True)

    # set all row heights
    nrows = len(self.imagelist)
    for row in range(nrows):
        tview.setRowHeight(row, 25)
    tview.setColumnWidth(0,400)
    tview.setDragDropMode(QAbstractItemView.DropOnly)
    tview.setAcceptDrops(True)
    self.enable_recompress()


class tri_table_model(QAbstractTableModel):
  def __init__(self, parent, imagelist, header, *args):
    """
    mydata is list of tuples
    header is list of strings
    tuple length has to match header length
    """
    QAbstractTableModel.__init__(self, parent, *args)
    self.imagelist = imagelist
    self.header = header

  def rowCount(self, parent):
    return len(self.imagelist)

  def columnCount(self, parent):
    return len(self.header)

  def data(self, index, role):
    if not index.isValid():
      return QVariant()
    elif role != Qt.DisplayRole:
      return QVariant()
    return QVariant(self.imagelist[index.row()][index.column()])

  def headerData(self, col, orientation, role):
    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
      return QVariant(self.header[col])
    return QVariant()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
