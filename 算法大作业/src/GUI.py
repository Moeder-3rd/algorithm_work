# -*- coding: utf-8 -*-

import time  # 引入time模块
import wx
import sys, os
import random
import dfs
import bfs

APP_TITLE = u'深度&广度优先迷宫问题演示'


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    maze_init = False
    maze_size = 0
    w = 0
    h = 0

    def __init__(self):
        '''构造函数'''

        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((900, 600))  # 增加窗口大小以容纳更多按钮
        self.Center()

        # 以下可以添加各类控件
        self.preview = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        self.preview.SetBackgroundColour(wx.Colour(0, 0, 0))
        dfs_btn = wx.Button(self, -1, u'深度优先遍历', size=(100, -1))
        bfs_btn = wx.Button(self, -1, u'广度优先遍历', size=(100, -1))
        maze_btn = wx.Button(self, -1, u'生成迷宫', size=(100, -1))
        clear_paths_btn = wx.Button(self, -1, u'清除路径', size=(100, -1))
        clear_paths_btn.Bind(wx.EVT_BUTTON, self.clear_paths)
        self.tip1 = wx.StaticText(self, -1, u'', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)
        self.tip2 = wx.StaticText(self, -1, u'选择迷宫尺寸', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)
        self.check1 = wx.RadioButton(self, -1, "10", pos=(50, 20), size=(50, 10))
        self.check2 = wx.RadioButton(self, -1, "20", pos=(100, 20), size=(50, 10))
        self.check3 = wx.RadioButton(self, -1, "50", pos=(150, 20), size=(50, 10))
        self.tip3 = wx.StaticText(self, -1, u'起点为左上角红色块\n终点为右下角红色块', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)

        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(dfs_btn, 0, wx.ALL, 10)
        sizer_right.Add(bfs_btn, 0, wx.ALL, 10)
        sizer_right.Add(maze_btn, 0, wx.ALL, 10)
        sizer_right.Add(clear_paths_btn, 0, wx.ALL, 10)
        sizer_right.Add(self.tip1, 0, wx.ALL, 10)
        sizer_right.Add(self.tip2, 0, wx.ALL, 10)
        sizer_right.Add(self.check1, 0, wx.ALL, 10)
        sizer_right.Add(self.check2, 0, wx.ALL, 10)
        sizer_right.Add(self.check3, 0, wx.ALL, 10)
        sizer_right.Add(self.tip3, 0, wx.ALL, 10)

        sizer_max = wx.BoxSizer()
        sizer_max.Add(self.preview, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        sizer_max.Add(sizer_right, 0, wx.EXPAND | wx.ALL, 0)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_max)
        self.Layout()

        dfs_btn.Bind(wx.EVT_BUTTON, self.btn_click)
        bfs_btn.Bind(wx.EVT_BUTTON, self.btn_click)
        maze_btn.Bind(wx.EVT_BUTTON, self.btn_click)
        clear_paths_btn.Bind(wx.EVT_BUTTON, self.clear_paths)
        self.check1.Bind(wx.EVT_RADIOBUTTON, self.check_size)
        self.check2.Bind(wx.EVT_RADIOBUTTON, self.check_size)
        self.check3.Bind(wx.EVT_RADIOBUTTON, self.check_size)

    def clear_paths(self, event):
        """Clears only non-obstacle paths from the maze, reverting any non-standard colors to white."""
        dc = wx.ClientDC(self.preview)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))

        # 遍历每个格子，如果颜色不是白色或黑色，则将其设置为白色
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                # 获取当前方格的颜色
                current_color = dc.GetPixel(int(j * self.w + self.w / 2), int(i * self.h + self.h / 2))

                # 如果当前颜色不是白色或黑色
                if current_color != wx.Colour(255, 255, 255) and current_color != wx.Colour(0, 0, 0):
                    # 重置为白色
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                    dc.DrawRectangle(int(j * self.w), int(i * self.h), int(self.w), int(self.h))
                else:
                    # 如果是白色或黑色，保持原样
                    dc.SetBrush(wx.Brush(current_color))
                    dc.DrawRectangle(int(j * self.w), int(i * self.h), int(self.w), int(self.h))

        # 标记起点和终点为红色
        dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
        dc.DrawRectangle(0, 0, int(self.w), int(self.h))  # 起点
        dc.DrawRectangle(int((self.maze_size - 1) * self.w), int((self.maze_size - 1) * self.h), int(self.w),
                         int(self.h))  # 终点

    def redraw_maze(self, dc):
        """重绘迷宫，但保持迷宫结构不变，确保每个方格颜色正确。"""
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                # 获取当前方格的颜色
                current_color = dc.GetPixel(int(j * self.w), int(i * self.h))

                # 判断当前颜色是否不是白色或黑色
                if current_color != wx.Colour(255, 255, 255) and current_color != wx.Colour(0, 0, 0):
                    # 如果颜色不是白色或黑色，重置为白色
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                else:
                    # 否则根据地图数据设置颜色
                    if dfs.temp_map[i + 1][j + 1] == 1 or bfs.temp_map[i + 1][j + 1] == 1:
                        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))  # 黑色，障碍
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))  # 白色，通路

                # 绘制方格
                dc.DrawRectangle(int(j * self.w), int(i * self.h), int(self.w), int(self.h))

        # 标记起点和终点
        dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
        dc.DrawRectangle(0, 0, int(self.w), int(self.h))
        dc.DrawRectangle(int((self.maze_size - 1) * self.w), int((self.maze_size - 1) * self.h), int(self.w),int(self.h))

    def btn_click(self, evt):
        dc = wx.ClientDC(self.preview)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        event = evt.GetEventObject()
        if event.GetLabel() in ['深度优先遍历', '广度优先遍历']:
            if not self.maze_init:
                dlg = wx.MessageDialog(None, u'迷宫未建立', u'操作提示')
                dlg.ShowModal()
                self.tip1.SetLabel(u'迷宫未建立')
            else:
                start_time = time.time()  # 记录算法开始时间

                # 根据按钮选择执行相应的算法
                if event.GetLabel() == '深度优先遍历':
                    self.tip1.SetLabel(u'深度优先遍历开始')
                    solved = dfs.start(self.maze_size, self.w, self.h, dc)
                elif event.GetLabel() == '广度优先遍历':
                    self.tip1.SetLabel(u'广度优先算法开始')
                    solved = bfs.start(self.maze_size, self.w, self.h, dc)

                elapsed_time = time.time() - start_time  # 计算运行时间

                # 根据算法是否找到解来弹出对应的消息框
                if not solved:
                    dlg = wx.MessageDialog(None, f'迷宫无解,{event.GetLabel()} 执行时间: {elapsed_time:.2f} 秒', u'操作提示')
                    dlg.ShowModal()
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))  # 搜索成功时改变颜色
                    message = f"{event.GetLabel()} 执行时间: {elapsed_time:.2f} 秒"
                    dlg = wx.MessageDialog(None, message, u'执行时间')
                    dlg.ShowModal()
        else:
            if self.maze_size == 0:
                dlg = wx.MessageDialog(None, u'请先选择迷宫尺寸', u'操作提示')
                dlg.ShowModal()

            dfs.temp_map = dfs.init_map(self.maze_size)
            bfs.temp_map = bfs.init_map(self.maze_size)

            self.tip1.SetLabel(u'迷宫建立')
            self.maze_init = True

            self.w, self.h = self.preview.GetSize()
            self.w /= self.maze_size
            self.h /= self.maze_size

            for i in range(self.maze_size):
                for j in range(self.maze_size):
                    dc.DrawRectangle(int(i * self.w), int(j * self.h), int(self.w), int(self.h))

            dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            dc.DrawRectangle(0, 0, int(self.w), int(self.h))
            dc.DrawRectangle(int((self.maze_size - 1) * self.w), int((self.maze_size - 1) * self.h), int(self.w),
                             int(self.h))

            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

            for index in range((int)((self.maze_size ** 2) * 0.3)):
                i = random.randint(0, self.maze_size - 1)
                j = random.randint(0, self.maze_size - 1)
                if i + j > 0 and i * j != (self.maze_size - 1) ** 2:
                    dfs.temp_map[i + 1][j + 1] = 1
                    bfs.temp_map[i + 1][j + 1] = 1
                    dc.DrawRectangle(int(i * self.w), int(j * self.h), int(self.w), int(self.h))
            print(dfs.temp_map)  # 可以根据需要打印其他模块的地图

    def check_size(self, evt):
        event = evt.GetEventObject()
        if event.GetLabel() == '10':
            self.maze_size = 10
        elif event.GetLabel() == '20':
            self.maze_size = 20
        elif event.GetLabel() == '50':
            self.maze_size = 50
        print(self.maze_size)

class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
