from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.title("Maze Solver")
        self.__root.resizable(False, False)
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas.configure(bg="white")

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        print("Window closed")

    def close(self):
        self.__is_running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)
