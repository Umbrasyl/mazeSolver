from lines import Line, Point

class Cell:
    def __init__(self, x1, y1, x2, y2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.is_visited = False
        self.__window = window

    def draw(self):
        if self.has_left_wall:
            self.__window.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "black")
        else:
            self.__window.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "white")
        if self.has_right_wall:
            self.__window.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "black")
        else:
            self.__window.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "white")
        if self.has_top_wall:
            self.__window.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "black")
        else:
            self.__window.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "white")
        if self.has_bottom_wall:
            self.__window.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "black")
        else:
            self.__window.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "white")

    def get_center(self):
        return Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)

    def draw_move(self, to_cell, undo=False):
        # This method will be used to draw a path from self to to_cell
        # The path will be drawn using the centers of cells
        if undo:
            color = "gray"
        else:
            color = "red"
        self.__window.draw_line(Line(self.get_center(), to_cell.get_center()), color)
