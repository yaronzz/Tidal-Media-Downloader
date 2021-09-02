#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  taskModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from tidal_gui.view.taskView import TaskView
from tidal_gui.viewModel.viewModel import ViewModel


class TaskModel(ViewModel):
    def __init__(self):
        super(TaskModel, self).__init__()
        self.view = TaskView()
