""" Module for Cell classes and associated simple viewer/controllers """

import copy

class BaseCell(object):
  """ Parent class of all Cell classes 
      Has a mandatory identity object, and a list of neighbors (typically instances of the same class)
  
      A Cell may be modified in two manners:
        - change internal properties of the instance directly - see update() method 
        - change internal properties of the instance depending on the existing properties of the Cell - see mutate() method 
        
      Hence Child class override update() and mutate() methods 

      A new generation of a cell can made (see nextGen() ) whereby a copy of cell is made which uses mutate() method  

      The modify() method must used by Cell Controllers to ensure that Cell Viewers 
      can be updated (via pypubsub message).   
  
  Usage:
  >>> import Cell
  >>> c1 = Cell.BaseCell('Cell 1')
  >>> c2 = Cell.BaseCell('Cell 2')
  >>> c3 = Cell.BaseCell('Cell 3')
  >>> [ c3.addNeighbor(c) for c in (c1,c2) ]
  >>> print c3
  "Cell 3" is descended from None. Neighbors @: "Cell 1", "Cell 2",'
  >>> c4 = c1.nextGen('Cell 4')
  >>> print c4
  "Cell 4" is descended from "Cell 1". No neighbors.'
  >>> c5 = self.c3.nextGen('Cell 5')
  >>> print c5
  '"Cell 5" is descended from "Cell 3". Neighbors @: "Cell 1", "Cell 2",'
  
  """
  def __init__(self, identity):
    self.identity = identity
    self.neighbors = []
    self.ancestor = None
    self.descendant = None
    self.generation = 0
    
  def addNeighbor(self, cell):
    """ Append a new cell to the list of neighbors of this cell """
    self.neighbors.append(cell)
    
  def mutate(self):
    """ Overridden by descendants - rules for cell self-modification"""
    pass
  
  def update(self, **kwargs):
    """ Overridden by descendants - general method for modifying cell """
    pass

  def clone(self, identity=None):
    """ Make a (shallow) copy of self and (optionally) change the identity """
    new = copy.copy(self)
    new.generation += 1
    new.identity = identity if identity else self.identity
    new.ancestor = self              # record the ancestor cell of this new cell
    self.descendant = new            # record that this new cell is a child of the old one 
    return new

  def nextGen(self, identity=None):
    """ Create a cloned copy of self, and mutate according to the rules of this class"""
    new = self.clone(identity)
    new.mutate()
    return new

  def identityString(self):
    """ used by __str__() and for debug """
    return '%s<%i>' % (str(self.identity), self.generation)

  def __str__ (self):
    return self.identityString()
  
  def dump(self):
    s = self.identityString()\
        + ' A: ' + ( self.ancestor.identityString() if self.ancestor else 'None' ) \
        + ' D: ' + ( self.descendant.identityString() if self.descendant else 'None' )
    s += ' N: '
    if len(self.neighbors) > 0: 
      s += str( [ cell.identityString() for cell in self.neighbors ] )
    else:
      s += 'None'
    return s


class IntegerCell(BaseCell):
  """ A simple Cell that has an integer value
      It's nextGen() method returns a cell with value equal to the sum of the cells present neighbors  

Usage:
>>> import Cell
>>> c1 = Cell.IntegerCell( 'Cell 1')  # state=0
>>> c2 = Cell.IntegerCell( 'Cell 2', state=1)
>>> c3 = Cell.IntegerCell( 'Cell 3', state=2)
>>> c4 = Cell.IntegerCell( 'Cell 4', state=3)
>>> [ c4.addNeighbor(c) for c in (c1,c2,c3) ]
>>> c5 = c4.nextGen('cell 5')
>>> print c5
"Cell 5" is descended from "Cell 4". Neighbors @: "Cell 1", "Cell 2", "Cell 3", State: 3  
  """ 
  def __init__(self, identity, state=0):
    super(IntegerCell,self).__init__(identity)
    self.state = state

  def mutate(self):
    """ sets the Cell state """
    self.state = sum ( cell.state for cell in self.neighbors )  # set the state to sum of neighbors """
  
  def update(self, state=0):
    """ sets the Cell state """
    self.state = state

  def __str__(self):
    return str(self.state)
    
  def dump(self):
    """ print out current state """
    return super(IntegerCell, self).dump() + 'State: %i'+str(self)



class BooleanCell(IntegerCell):
  """ A simpler version of Integer cell where state is a boolean value
      mutate() and update() both toggle the cell state
      
Usage:
>>> import Cell
>>> c1 = Cell.BooleanCell( 'Cell 1') 
>>> c2 = Cell.BooleanCell( 'Cell 2', True)
>>> print c1,c2
>>> (c3, c4) = (c1.nextGen(), c2.nextGen())
>>> print c3,c4

  """
  def mutate(self):
    """ toggles the state """
    self.state = not self.state

  def update(self):
    """ toggles the state """
    self.state = not self.state
  
  
  
if __name__ == '__main__':
  print "For tests use module 'testCell'"
 
