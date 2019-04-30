from PyQt5.QtWidgets import QPushButton
import qtawesome
class my_pushbutton_play(QPushButton):
    def __init__(self,music_name,music_address):
        QPushButton.__init__(self,'播放')
        self.music_address=music_address
        self.music_name=music_name
class my_pushbutton_love(QPushButton):
    def __init__(self,music_name):
        QPushButton.__init__(self,'评分')
        self.music_name=music_name
class my_pause_putton(QPushButton):
    def __init__(self):
        QPushButton.__init__(self,qtawesome.icon('fa.pause', color='#F76677', font=18), "")
        self.flag=True
    def auto_change(self):
        self.flag=not self.flag
    def set_falg(self):
        self.flag=True