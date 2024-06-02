from collections import deque
import wx
import time

MAX_VALUE = 0x7fffffff

temp_map = [[]]

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def init_map(maze_size):
    temp_map = [[0 for y in range(maze_size + 2)] for x in range(maze_size + 2)]
    for i in range(len(temp_map)):
        temp_map[i][0] = temp_map[i][len(temp_map)-1] = 1
    for i in range(len(temp_map[0])):
        temp_map[0][i] = temp_map[len(temp_map[0]) - 1][i] = 1
    return temp_map

def dfs(maze, begin, end, w, h, dc):
    n, m = len(maze), len(maze[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    path = []

    dx = [1, 0, -1, 0]  # 四个方向
    dy = [0, 1, 0, -1]

    def search(x, y):
        if x == end.x and y == end.y:
            path.append(Point(x, y))
            return True

        if not (0 <= x < n and 0 <= y < m) or maze[y][x] == 1 or visited[x][y]:
            return False

        visited[x][y] = True
        path.append(Point(x, y))
        dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
        dc.DrawRectangle(int((y - 1) * w), int((x - 1) * h), int(w), int(h))
        time.sleep(0.05)

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if search(nx, ny):
                return True

        path.pop()
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.DrawRectangle(int((y - 1) * w), int((x - 1) * h), int(w), int(h))
        return False

    search(begin.x, begin.y)

    if path:
        for point in path:
            dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))  # 将路径绘制为绿色以区分
            dc.DrawRectangle(int((point.y - 1) * w), int((point.x - 1) * h), int(w), int(h))
        return True
    return False

def start(maze_size, w, h, dc):
    maze = temp_map
    begin = Point(1, 1)
    end = Point(maze_size, maze_size)
    return dfs(maze, begin, end, w, h, dc)
