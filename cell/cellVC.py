# -----------------------------------------------------------------
# Cell Viewer / Controllers
# -----------------------------------------------------------------
from pubsub import pub
class Cell_VC(object):
    """ Simple Viewer/Controller of Cell """
  
    def __init__(self, cell):
      """ Associate this VC with a Cell """
      self.setCell(cell)
      pub.subscribe(self.refresh, 'Cell-Modified')    # register to listen for Cell-Modified events, and bind to a view refresh 
      self.refresh()
    
    def setCell(self, cell):
      """ Point the VC to a (different) cell """
      self.cell = cell
      self.refresh()
          
    def mutate(self):
      """ Provoke the underlying Cell to mutate """
      self.cell.mutate()
      pub.sendMessage('Cell-Modified')
#     
    def update(self, **kwargs):
      """ Change properties of the Cell """
      self.cell.update(**kwargs)
      pub.sendMessage('Cell-Modified')
# 
    def refresh(self):
      """ Update the display string associated with the underlying Cell state """
      self.strValue = self.cell.identity

    def __str__(self):
      """ Overridden by subclasses """
      return self.strValue 



class IntegerCell_VC(Cell_VC):
    """ Simple viewer/controller specific for IntegerCell"""
    def refresh(self):
      """ Set the display string to the (integer) state """
      self.strValue = str(self.cell.state)



class BooleanCell_VC(Cell_VC):
    """ Simple viewer/controller specific for BooleanCell"""
    def refresh(self):
      """ Set the display string depending on state of underlying cell """
      self.strValue = '*' if self.cell.state else '-'

