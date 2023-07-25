import unittest
from maze import Maze
from cells import Cell
from window import Window

class TestMaze(unittest.TestCase):
    def setUp(self):
        self.win = Window(500, 500)
        self.maze = Maze(0, 0, 5, 5, 10, self.win, animation_speed=0)

    def tearDown(self):
        self.win.close()

    def test_create_cells(self):
        self.assertEqual(len(self.maze._Maze__cells), 5)
        for col in self.maze._Maze__cells:
            self.assertEqual(len(col), 5)
            for cell in col:
                self.assertIsInstance(cell, Cell)

    def test_draw_maze(self):
        # This test is difficult to automate, but we can at least check that it doesn't raise any exceptions
        self.maze._Maze__draw_maze()

    def test_entrance_and_exit(self):
        self.assertFalse(self.maze._Maze__cells[0][0].has_top_wall)
        self.assertFalse(self.maze._Maze__cells[-1][-1].has_bottom_wall)

if __name__ == "__main__":
    unittest.main()