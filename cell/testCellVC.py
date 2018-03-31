import unittest, cellVC

# ---------------------------------------------------------------------
# Tests for CellViewerController 
# ---------------------------------------------------------------------

class TestVCCells(unittest.TestCase):
  
  def testCell_VC(self):
    """ general tests for Cell Viewer/Controllers """

# create a BaseCell and a Viewer/Controller
    c1 = cell.BaseCell('Cell 1')
    vc = Cell_VC(c1)
    
# check association and initial value of the viewer/controller string
    self.assertTrue( vc.cell is c1)
    self.assertEqual( str(vc), 'Cell 1')

# test setCell 
    c2 = cell.BaseCell('Cell 2')
    vc.setCell(c2)
    self.assertTrue( vc.cell is c2)
    self.assertEqual( str(vc), 'Cell 2')

# ---------------------------------------------------------------------
# Tests for IntegerCellViewerController 
# ---------------------------------------------------------------------
  def testIntegerCell_VC(self):
    """ tests specific to Integer Cell VC """

# create an IntegerCell and a Viewer/Controller
    c1 = cell.IntegerCell('Cell1')
    vc = cell.IntegerCell_VC(c1)
    
# check association and initial value of the viewer/controller string
    self.assertEqual( str(vc), '0')

# set up neighbors of c1
    c2 = cell.IntegerCell('Cell2', state=5)
    c3 = cell.IntegerCell('Cell3', state=10)
    c1.addNeighbor(c2)
    c1.addNeighbor(c3)
    
# two types of modification. Each should update the py string  
    vc.mutate()        # mutate according to Cells internal rules
    self.assertEqual( str(vc), '15')

    vc.update(state=50)             
    self.assertEqual( str(vc), '50')

# ---------------------------------------------------------------------
# Tests for BooleanCellViewer 
# ---------------------------------------------------------------------
  def testBooleanCell_VC(self):
    """ tests specific to Boolean Cell VC """

# create a boolean cell and a viewer/controller
    c1 = cell.BooleanCell('Cell1')
    vc = cell.BooleanCell_VC(c1)

# check association and initial value of the viewer/controller string
    self.assertEqual( str(vc),'-')

# two types of modification. Each should update the viewer/controller string  
    vc.mutate()     
    self.assertEqual( str(vc), '*')

    vc.update()             
    self.assertEqual( str(vc), '-')



if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestVCCells)
  unittest.TextTestRunner(verbosity=3).run(suite)