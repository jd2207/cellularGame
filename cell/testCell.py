import unittest, cell


class TestCells(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for BaseCell 
# ---------------------------------------------------------------------
  def setUp(self):
    self.cell1 = cell.BaseCell('Cell 1')
    self.cell2 = cell.BaseCell('Cell 2')

  def testBaseCellCreation(self):
    """ test constructor """  
    self.assertEqual(self.cell1.dump(), 'Cell 1<0> A: None D: None N: None')
    self.assertEqual(str(self.cell1), 'Cell 1<0>')
    self.assertEqual(self.cell1.generation, 0)
    self.assertEqual(self.cell1.neighbors, [])
    self.assertEqual(self.cell1.ancestor, None)
    self.assertEqual(self.cell1.descendant, None)
    self.assertEqual(self.cell2.dump(), 'Cell 2<0> A: None D: None N: None')
    self.assertEqual(str(self.cell2), 'Cell 2<0>')

  def testBaseCellAddNeighbors(self):
    """ test adding neighbors """  
    cell3 = cell.BaseCell('Cell 3')
    [ cell3.addNeighbor(c) for c in (self.cell1, self.cell2) ]
    self.assertEqual(cell3.dump(), "Cell 3<0> A: None D: None N: ['Cell 1<0>', 'Cell 2<0>']")
  
  def testBaseCellCloneUpdate(self):
    cell4 = self.cell1.clone()
    cell5 = self.cell2.clone('Cell 5')

    self.assertFalse(self.cell1 is cell4)
    self.assertNotEqual(self.cell1, cell4)
    self.assertEqual(cell4.dump(), 'Cell 1<1> A: Cell 1<0> D: None N: None')
    self.assertTrue( cell4.ancestor is self.cell1 )
    self.assertTrue( self.cell1.descendant is cell4 )
    self.assertEqual( cell4.generation, 1 )

    self.assertFalse(self.cell2 is cell5)
    self.assertNotEqual(self.cell2, cell5)
    self.assertEqual(self.cell2.dump(), 'Cell 2<0> A: None D: Cell 5<1> N: None')
    self.assertEqual(cell5.dump(), 'Cell 5<1> A: Cell 2<0> D: None N: None')
    self.assertTrue( cell5.ancestor is self.cell2 )
    self.assertTrue( self.cell2.descendant is cell5 )
    self.assertEqual( cell5.generation, 1 )
  
    # test nextGen()
    cell6 = cell5.nextGen('Cell 6')
    self.assertTrue( cell6.ancestor is cell5 )
    self.assertTrue( cell5.descendant is cell6 )
    self.assertEqual( cell6.generation, 2 )
    self.assertEqual(cell6.dump(), 'Cell 6<2> A: Cell 5<1> D: None N: None')
    
# ---------------------------------------------------------------------
# Tests for IntegerCell 
# ---------------------------------------------------------------------
  def testIntegerCell(self):
    """ tests specific to IntegerCell """
    c1 = cell.IntegerCell("Cell 1")         # default state
    c2 = cell.IntegerCell('Cell 2', 1)
    c3 = cell.IntegerCell('Cell 3', 5)
    c4 = cell.IntegerCell('Cell 4', 10)
    
    self.assertEqual(str(c1), '0')
    self.assertEqual(str(c2), '1')

    [ c4.addNeighbor(c) for c in (c1,c2,c3) ]
    
    c4.mutate()                          # new state depends on neighbor state
    self.assertEqual(c4.state, 6)

    c4.update(state=100)                 # directly change state 
    self.assertEqual(c4.state, 100)
    
    c1.state = 10
    c5 = c4.nextGen('Cell 5')            # nextGen includes a mutate()
    self.assertEqual(c5.state, 16)
    
# ---------------------------------------------------------------------
# Tests for BooleanCell 
# ---------------------------------------------------------------------
  def testBooleanCell(self):
    """ tests specific to BooleanCell """
    c1 = cell.BooleanCell("Cell 1")         # default False
    c2 = cell.BooleanCell('Cell 2', True)
    
    self.assertFalse(c1.state)
    self.assertEqual(str(c2), 'True')

    c1.mutate()                    # in this case mutate() should perform a toggle on the boolean
    self.assertTrue(c1.state)

    c2.update()                    # update also means toggle for BooleanCells 
    self.assertFalse(c2.state)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCells)
  unittest.TextTestRunner(verbosity=3).run(suite)
