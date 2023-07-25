from cells import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size, win, animation_speed=0.01, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size = cell_size
        self.__win = win
        self.__animation_speed = animation_speed
        if seed is not None:
            random.seed(seed)
        # self.__cells is a list of lists of cells. Each inner list is a column of cells
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for col in range(self.__num_cols):
            self.__cells.append([])
            for row in range(self.__num_rows):
                x1 = self.__x1 + col * self.__cell_size
                y1 = self.__y1 + row * self.__cell_size
                x2 = x1 + self.__cell_size
                y2 = y1 + self.__cell_size
                self.__cells[col].append(Cell(x1, y1, x2, y2, self.__win))
        self.__draw_maze()
                
    def __draw_maze(self):
        for col in self.__cells:
            for cell in col:
                cell.draw()
                self.__animate()
        self.__break_entrance_and_exit()
        self.__break_walls_r(self.__cells[0][0])
        self.__reset_cells_visited()
        self.solve()

    def __animate(self):
        self.__win.redraw()
        time.sleep(self.__animation_speed)

    def __break_entrance_and_exit(self):
        # In each maze the entrace is the top wall of the top-left cell 
        # and the exit is the bottom wall of the bottom-right cell

        # Break the top wall of the top-left cell
        top_left_cell = self.__cells[0][0]
        top_left_cell.has_top_wall = False
        top_left_cell.draw()
        self.__animate()

        # Break the bottom wall of the bottom-right cell
        bottom_right_cell = self.__cells[-1][-1]
        bottom_right_cell.has_bottom_wall = False
        bottom_right_cell.draw()
        self.__animate()

    def __break_walls_r(self, cell):
        cell.is_visited = True
        while True:
            # Create a list to store the unvisited neighbours of the cell
            unvisited_neighbours = []

            # Get the neighbours of the cell
            neighbours = self.__get_neighbours(cell)

            # Iterate through the neighbours
            for neighbour in neighbours:
                # If the neighbour has not been visited, add it to the unvisited_neighbours list
                if not neighbour.is_visited:
                    unvisited_neighbours.append(neighbour)

            # If there are no unvisited neighbours, return
            if len(unvisited_neighbours) == 0:
                return

            # Choose a random unvisited neighbour
            random_neighbour = random.choice(unvisited_neighbours)

            # Break the wall between the cell and the random neighbour
            self.__break_wall(cell, random_neighbour)

            # Recursively call the __break_walls_r method with the random neighbour as the argument
            self.__break_walls_r(random_neighbour)

    def __get_neighbours(self, cell):
        # Create a list to store the neighbours
        neighbours = []

        # Get the row and column of the cell
        row = self.__get_row(cell)
        col = self.__get_col(cell)

        # If the cell is not in the first row, add the cell above it to the neighbours list
        if row > 0:
            neighbours.append(self.__cells[col][row - 1])
        # If the cell is not in the last row, add the cell below it to the neighbours list
        if row < self.__num_rows - 1:
            neighbours.append(self.__cells[col][row + 1])
        # If the cell is not in the first column, add the cell to the left of it to the neighbours list
        if col > 0:
            neighbours.append(self.__cells[col - 1][row])
        # If the cell is not in the last column, add the cell to the right of it to the neighbours list
        if col < self.__num_cols - 1:
            neighbours.append(self.__cells[col + 1][row])

        # Return the neighbours list
        return neighbours
    
    def __get_row(self, cell) -> int:
        # Get the column of the cell
        col = self.__get_col(cell)

        # Iterate through the cells in the column
        for row in range(self.__num_rows):
            # If the cell is found, return its row
            if self.__cells[col][row] == cell:
                return row
            
        # If the cell is not found, raise an AssertionError
        assert False, "Cell not found"
            
    def __get_col(self, cell) -> int:
        # Iterate through the columns
        for col in range(self.__num_cols):
            # Iterate through the cells in the column
            for row in range(self.__num_rows):
                # If the cell is found, return its column
                if self.__cells[col][row] == cell:
                    return col
                
        # If the cell is not found, raise an AssertionError
        assert False, "Cell not found"
                
    def __break_wall(self, cell1, cell2):
        # Get the row and column of cell1
        row1 = self.__get_row(cell1)
        col1 = self.__get_col(cell1)

        # Get the row and column of cell2
        row2 = self.__get_row(cell2)
        col2 = self.__get_col(cell2)

        # If cell1 is to the left of cell2
        if col1 < col2:
            # Break the right wall of cell1 and the left wall of cell2
            cell1.has_right_wall = False
            cell2.has_left_wall = False
        # If cell1 is to the right of cell2
        elif col1 > col2:
            # Break the left wall of cell1 and the right wall of cell2
            cell1.has_left_wall = False
            cell2.has_right_wall = False
        # If cell1 is above cell2
        elif row1 < row2:
            # Break the bottom wall of cell1 and the top wall of cell2
            cell1.has_bottom_wall = False
            cell2.has_top_wall = False
        # If cell1 is below cell2
        elif row1 > row2:
            # Break the top wall of cell1 and the bottom wall of cell2
            cell1.has_top_wall = False
            cell2.has_bottom_wall = False

        # Draw the walls
        cell1.draw()
        self.__animate()
        cell2.draw()
        self.__animate()
    
    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.is_visited = False

    def solve(self):
        # Create a list to store the cells that are part of the path
        path = []

        # Get the entrance cell
        entrance_cell = self.__cells[0][0]

        # Add the entrance cell to the path
        path.append(entrance_cell)

        # Call the __solve_r method with the entrance cell and the path as the arguments
        return self.__solve_r(entrance_cell, path)

    def __solve_r(self, cell, path):
        # This function will move through cells that dont have a path between and try to reach the exit
        # If we find a deadend it will retrace back to the last cell that had a path between and try to find another path
        # If we find the exit it will return True
        # If we find a deadend and there is no cell in the path that has a path between it will return False
        # It will draw the path while moving with the draw_move method

        # If the cell is the exit, return True
        if self.__is_exit(cell):
            return True
        
        # Get the neighbours of the cell
        neighbours = self.__get_neighbours_without_wall_between(cell)

        # Iterate through the neighbours
        for neighbour in neighbours:
            # If the neighbour is not in the path
            if neighbour not in path:
                # Add the neighbour to the path
                path.append(neighbour)

                # Draw the move from the cell to the neighbour
                cell.draw_move(neighbour)
                self.__animate()

                # Call the __solve_r method with the neighbour and the path as the arguments
                if self.__solve_r(neighbour, path):
                    return True

                # If the __solve_r method returns False, remove the neighbour from the path
                path.remove(neighbour)

                # Draw the move from the neighbour to the cell
                neighbour.draw_move(cell, True)
                self.__animate()

        # If the function has not returned True, return False
        return False
    
    
    def __is_exit(self, cell):
        # Get the row and column of the cell
        row = self.__get_row(cell)
        col = self.__get_col(cell)

        # If the cell is in the last column and the last row, return True
        if col == self.__num_cols - 1 and row == self.__num_rows - 1:
            return True
        
        # If the cell is not in the last column or the last row, return False
        return False

    def __get_neighbours_without_wall_between(self, cell):
        # Create a list to store the neighbours
        neighbours = []

        # Get the row and column of the cell
        row = self.__get_row(cell)
        col = self.__get_col(cell)

        # If the cell is not in the first row and the top wall of the cell is broken, add the cell above it to the neighbours list
        if row > 0 and not cell.has_top_wall:
            neighbours.append(self.__cells[col][row - 1])

        # If the cell is not in the last row and the bottom wall of the cell is broken, add the cell below it to the neighbours list
        if row < self.__num_rows - 1 and not cell.has_bottom_wall:
            neighbours.append(self.__cells[col][row + 1])

        # If the cell is not in the first column and the left wall of the cell is broken, add the cell to the left of it to the neighbours list
        if col > 0 and not cell.has_left_wall:
            neighbours.append(self.__cells[col - 1][row])

        # If the cell is not in the last column and the right wall of the cell is broken, add the cell to the right of it to the neighbours list
        if col < self.__num_cols - 1 and not cell.has_right_wall:
            neighbours.append(self.__cells[col + 1][row])

        # Return the neighbours list
        return neighbours
    