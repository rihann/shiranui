import main_ui
from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt
import sys
from PyQt5.QtWidgets import QPushButton,QLabel,QWidget,QHBoxLayout,QVBoxLayout,QGridLayout,QScrollArea,QFormLayout,QLineEdit,QInputDialog,QTextEdit
import qtawesome
import mongo_process
import my_widget
import time
import algorithms
import denglu
import registered
import yindao
#将界面，逻辑，数据据，算法分隔开
class denglu_gui(QtWidgets.QMainWindow,QtCore.QObject,denglu.Ui_MainWindow):#登陆界面
    _signal = QtCore.pyqtSignal(int)
    _signal_zhuce = QtCore.pyqtSignal()
    _signal_yindao = QtCore.pyqtSignal(int)
    def __init__(self,parent=None):
        super(denglu_gui,self).__init__(parent)
        super().setupUi(self)
        self.mongo=mongo_process.process_data()
        self.pushButton.clicked.connect(self.denglu)
        self.pushButton_2.clicked.connect(self.enter_zhuce)
        self.password.setEchoMode(QLineEdit.Password)
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.set_label(self.label)
        self.set_label(self.label_2)
        self.set_label(self.label_3)
        self.statusbar.setStyleSheet("color:white")
        self.setWindowTitle('音乐播放器')
    def set_label(self,label):
        label.setStyleSheet("color:white")
    def show_gui(self):
        self.show()
    def denglu(self):
        user_name=self.user_name.text()
        password = self.password.text()
        if(not user_name.isdigit()):
            self.statusbar.showMessage("密码或账号错误", 3000)
        else:
            real_password = self.mongo.get_password(int(user_name))
            if (real_password != None and real_password == password):
                self.close()
                user_info=self.mongo.get_user_info(int(user_name))
                data=user_info['songRecord']
                if(len(data)>0):
                    self._signal.emit(int(user_name))
                else:
                    self._signal_yindao.emit(int(user_name))
                self.mongo.my_close()
            else:
                self.statusbar.showMessage("密码或账号错误", 3000)
    def enter_zhuce(self):
        self.close()
        self._signal_zhuce.emit()
class registered_gui(QtWidgets.QMainWindow,QtCore.QObject,registered.Ui_MainWindow):
    _signal = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(registered_gui,self).__init__(parent)
        super().setupUi(self)
        self.mongo=mongo_process.process_data()
        self.pushButton.clicked.connect(self.zhuce)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.set_label(self.label)
        self.set_label(self.label_2)
        self.set_label(self.label_3)
        self.statusbar.setStyleSheet("color:white")
        self.setWindowTitle('音乐播放器')
    def show_gui(self):
        self.show()
    def set_label(self,label):
        label.setStyleSheet("color:white")
    def zhuce(self):
        user_name=self.user_name.text()
        password = self.lineEdit_2.text()
        if(not user_name.isdigit()):
            self.statusbar.showMessage("账号只能为纯数字", 3000)
        else:
            real_password = self.mongo.get_password(int(user_name))
            if (real_password ==None and len(password)>0):
                self.mongo.insert_user(int(user_name),password)
                self.close()
                self.mongo.my_close()
                self._signal.emit()
            else:
                self.statusbar.showMessage("账号已经被注册", 3000)
class yindao_gui(QtWidgets.QMainWindow,QtCore.QObject,yindao.Ui_MainWindow):#引导界面
    _signal = QtCore.pyqtSignal(int,list)
    def __init__(self,parent=None):
        super(yindao_gui,self).__init__(parent)
        super().setupUi(self)
        self.pushButton.clicked.connect(self.enter_main)
        self.mongo=mongo_process.process_data()
        style_lists=self.mongo.get_all_style()
        self.comboBox.addItem('')
        for style in style_lists:
            self.comboBox.addItem(style)
        self.style_list=[]
        self.comboBox.currentIndexChanged.connect(self.show_style)
    def show_init(self,user_id):
        self.ID=user_id
        self.show()
    def enter_main(self):
        self.close()
        self.style_list=list(set(self.style_list))
        self._signal.emit(self.ID,self.style_list)
    def show_style(self,i):
        current_text=self.display_style.text()
        local_text=self.comboBox.currentText()
        self.style_list.append(local_text)
        new_text=current_text+"  "+local_text
        self.display_style.setText(new_text)
class main_gui(QtWidgets.QMainWindow,QtCore.QObject,main_ui.Ui_MainWindow):
    _signal=QtCore.pyqtSignal(dict)
    def __init__(self,parent=None):
        super(main_gui,self).__init__(parent)
        super().setupUi(self)
        self.music_count = 0
        self.mongo = mongo_process.process_data()
        self.set_recommend()
        self.set_process_bar()
        self.setWindowOpacity(0.8)  # 设置窗口透明度
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet('''#MainWindow{background-color:blue}''')
        self.sousuo.clicked.connect(self.find_music_singer)
        self.statusbar.setStyleSheet("color:white")
        self.algorithn1_form_info = {}  # 推荐算法一歌单
        self.algorithn2_form_info = {}  # 推荐算法二歌单
        self.user_info.setStyleSheet("color:white")
        self.setWindowTitle('音乐播放器')
        self.player = QtMultimedia.QMediaPlayer()
        self.player.durationChanged.connect(self.set_dateDuration)
        self.player.positionChanged.connect(self.update_position)
        self.style_list=self.mongo.get_all_style()
        for style in self.style_list:
            self.comboBox.addItem(style)
        self.comboBox.currentIndexChanged.connect(self.show_style)
    def show_gui(self,user_name):
        self.ID = user_name
        self.get_user_history_form()
        self.music_forms()
        self.user_info.setText('用户ID:'+str(self.ID))
        self.show()
    def show_gui_yindao(self,user_name,style_list):
        self.ID = user_name
        self.get_user_history_form()
        self.music_forms()
        self.user_info.setText('用户ID:' + str(self.ID))
        self.style_list_love=style_list
        self.local_music_info=self.mongo.return_song_in_style_list(self.style_list_love)
        self.show_sousuo()
        self.music_form_info.setText('根据您喜欢的音乐风格，给您推荐的音乐')
        self.show()
    def show_style(self,i):
        data,a=self.mongo.get_sousuo(self.comboBox.currentText())
        if(data!=None):
            self.local_music_info=data
            self.show_sousuo()
    def set_recommend(self):#设置三个推荐内容模块，和歌单
        self.QPushButton_history=QPushButton(qtawesome.icon('fa.heart',color='white'),'历史播放')#按照播放频率排序
        self.QPushButton_algorithm1=QPushButton(qtawesome.icon('fa.music',color='white'),'协同过滤')
        self.QPushButton_algorithm2=QPushButton(qtawesome.icon('fa.music',color='white'),'内容推荐')
        self.QPushButton_history.clicked.connect(self.control_music_form)
        self.QPushButton_algorithm1.clicked.connect(self.control_music_form)
        self.QPushButton_algorithm2.clicked.connect(self.control_music_form)
        #将按钮加入布局
        self.left_layout.addWidget(self.QPushButton_history,0,0,1,3)
        self.left_layout.addWidget(self.QPushButton_algorithm1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.QPushButton_algorithm2, 2, 0, 1, 3)
        self.set_putton_style(self.QPushButton_history)
        self.set_putton_style(self.QPushButton_algorithm1)
        self.set_putton_style(self.QPushButton_algorithm2)
    def set_putton_style(self,btn):
        btn.setStyleSheet('''
                    QPushButton{border:none;color:white;}
                    QPushButton#left_label{
                        border:none;
                        border-bottom:1px solid white;
                        font-size:18px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                ''')
    def control_music_form(self):
        btn=self.sender()
        if(btn.text()=='历史播放'):
            self.music_form_info.setText('基于用户历史播放记录的推荐，降序排列')
            self.get_user_history_form()
            self.local_music_info=self.history_form_info
            self.show_music_form(0)
        if(btn.text()=='协同过滤'):
            if(len(self.history_form_info)>=10):
                if (len(self.algorithn1_form_info) > 0):
                    self.music_form_info.setText('基于nmf模型的协同过滤推荐')
                    self.local_music_info = self.algorithn1_form_info
                    self.show_music_form(1)
                else:
                    self.work_1 = work_algorithm_1(self.ID)
                    self.work_1.qt_signal.connect(self.respond_algorithm_1)
                    self.work_1.start()
            else:
                self.statusbar.showMessage('请先听10首音乐以上，再点击推荐', 3000)
        if (btn.text() == '内容推荐'):
            if (len(self.history_form_info) >= 10):
                if (len(self.algorithn2_form_info) > 0):
                    self.music_form_info.setText('基于knn模型的内容推荐')
                    self.local_music_info = self.algorithn2_form_info
                    self.show_music_form(1)
                else:
                    self.work_2 = work_algorithm_2(self.ID)
                    self.work_2.qt_signal.connect(self.respond_algorithm_2)
                    self.work_2.start()
            else:
                self.statusbar.showMessage('请先听10首音乐以上，再点击推荐', 3000)
    def respond_algorithm_1(self,info,song_list):
        self.work_1.quit()
        self.algorithn1_form_info = self.get_recommend(song_list)
        self.music_form_info.setText('基于nmf模型的协同过滤推荐')
        self.local_music_info = self.algorithn1_form_info
        self.show_music_form(1)
        self.statusbar.showMessage(info, 3000)
    def respond_algorithm_2(self,info,song_list):
        self.work_2.quit()
        self.algorithn2_form_info = self.get_recommend(song_list)
        self.music_form_info.setText('基于逻辑回归模型的内容推荐')
        self.local_music_info = self.algorithn2_form_info
        self.show_music_form(1)
        self.statusbar.showMessage(info, 3000)
    def music_forms(self):
        self.music_layout=QFormLayout()
        music_widget=QWidget()
        music_widget.setLayout(self.music_layout)
        self.music_form.setWidget(music_widget)
        self.music_form.setWidgetResizable(True)
        #显示图片

        self.img_label.setPixmap(QPixmap('tubiao//gedan.png'))
        self.music_form_info.setText('欢迎使用音乐播放器')

    def set_process_bar(self):#进度条及播放控制
        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_process_bar.setValue(49)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        self.console_button_1.clicked.connect(self.play_before)
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
        self.console_button_2.clicked.connect(self.play_next)
        self.console_button_3 = my_widget.my_pause_putton()
        self.console_button_3.clicked.connect(self.pause_music)
        self.console_button_3.setIconSize(QtCore.QSize(30, 30))
        self.music_name_label=QLabel('歌曲名')
        self.music_name_label.setWordWrap(True)
        self.music_name_label.setMaximumSize(200,200)
        self.music_name_label.setStyleSheet("color:white")
        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 1)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示
        self.procee_down_layout=QHBoxLayout()
        self.procee_down_widget=QtWidgets.QWidget()
        self.procee_down_widget.setLayout(self.procee_down_layout)
        self.procee_down_layout.addWidget(self.music_name_label)
        self.procee_down_layout.addStretch(1)
        self.procee_down_layout.addWidget(self.right_playconsole_widget)
        self.procee_down_layout.addStretch(1)
        self.process_layout.addWidget(self.right_process_bar)
        self.process_layout.addWidget(self.procee_down_widget)
    def show_music_form(self,flag):#歌曲列表界面
        #self.music_form_info.setText('基于用户历史播放记录的推荐，降序排列')
        self.clear_music_form()
        self.music_count=0
        qlabel_music_name = QLabel('音乐名')
        qlabel_music_singer = QLabel('歌手')
        qlabel_music_style = QLabel('歌曲类型')
        qlabel_music_time = QLabel('时间')
        if(flag==0):
            qlabel_music_num = QLabel('播放次数')
        qlabel_music_score = QLabel('评分')
        qlabel = QLabel('')
        qlabe2 = QLabel('')
        h = QWidget()
        layout = QHBoxLayout()
        h.setLayout(layout)
        layout.addWidget(qlabel_music_name)
        layout.addWidget(qlabel_music_singer)
        layout.addWidget(qlabel_music_style)
        layout.addWidget(qlabel_music_time)
        if(flag==0):
            layout.addWidget(qlabel_music_num)
        layout.addWidget(qlabel_music_score)
        layout.addWidget(qlabel)
        layout.addWidget(qlabe2)
        self.music_layout.addRow('', h)
        for data in self.local_music_info:
                qlabel_music_name = QLabel(data)
                qlabel_music_singer = QLabel(self.local_music_info[data]['author'])
                qlabel_music_style = QLabel(self.local_music_info[data]['style'])

                qlabel_music_time = QLabel()
                qlabel_music_time.setText(self.process_time(self.local_music_info[data]['time']))
                if(flag==0):
                    qlabel_music_num = QLabel()
                    qlabel_music_num.setText(str(self.history_form_user[data][0]))
                    qlabel_score = QLabel()
                    qlabel_score.setText(str(round(self.history_form_user[data][1], 2)))
                else:
                    qlabel_score = QLabel()
                    qlabel_score.setText(str(8))
                score_button=my_widget.my_pushbutton_love(data)
                score_button.clicked.connect(self.get_score)
                score_button.setStyleSheet('''
                                                QPushButton{border:none;color:black;}
                                                QPushButton#left_label{
                                                    border:none;
                                                    border-bottom:1px solid black;
                                                    font-size:18px;
                                                    font-weight:700;
                                                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                                }
                                                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                                            ''')
                play_button=my_widget.my_pushbutton_play(data,self.local_music_info[data]['download_path'])
                play_button.clicked.connect(self.play_music)
                play_button.setStyleSheet('''
                                    QPushButton{border:none;color:black;}
                                    QPushButton#left_label{
                                        border:none;
                                        border-bottom:1px solid black;
                                        font-size:18px;
                                        font-weight:700;
                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                    }
                                    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                                ''')

                h= QWidget()
                layout = QHBoxLayout()
                h.setLayout(layout)
                layout.addWidget(qlabel_music_name)
                layout.addWidget(qlabel_music_singer)
                layout.addWidget(qlabel_music_style)
                layout.addWidget(qlabel_music_time)
                if(flag==0):
                    layout.addWidget(qlabel_music_num)
                layout.addWidget(qlabel_score)
                layout.addWidget(play_button)
                layout.addWidget(score_button)
                self.music_layout.addRow(str(self.music_count), h)
                self.music_count = self.music_count + 1
    def show_sousuo(self):#输入音乐列表，展示结果.
        self.clear_music_form()
        self.music_form_info.setText('搜索结果')
        self.music_count = 0
        qlabel_music_name = QLabel('音乐名')
        qlabel_music_singer = QLabel('歌手')
        qlabel_music_style = QLabel('歌曲类型')
        qlabel_music_time = QLabel('时间')
        qlabel = QLabel('')
        h = QWidget()
        layout = QHBoxLayout()
        h.setLayout(layout)
        layout.addWidget(qlabel_music_name)
        layout.addWidget(qlabel_music_singer)
        layout.addWidget(qlabel_music_style)
        layout.addWidget(qlabel_music_time)
        layout.addWidget(qlabel)
        self.music_layout.addRow('', h)
        for data in self.local_music_info:
            qlabel_music_name = QLabel(data)
            qlabel_music_singer = QLabel(self.local_music_info[data]['author'])
            qlabel_music_style = QLabel(self.local_music_info[data]['style'])

            qlabel_music_time = QLabel()
            qlabel_music_time.setText(self.process_time(self.local_music_info[data]['time']))

            play_button = my_widget.my_pushbutton_play(data,self.local_music_info[data]['download_path'])
            play_button.clicked.connect(self.play_music)
            play_button.setStyleSheet('''
                                            QPushButton{border:none;color:black;}
                                            QPushButton#left_label{
                                                border:none;
                                                border-bottom:1px solid black;
                                                font-size:18px;
                                                font-weight:700;
                                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                                            }
                                            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                                        ''')

            h = QWidget()
            layout = QHBoxLayout()
            h.setLayout(layout)
            layout.addWidget(qlabel_music_name)
            layout.addWidget(qlabel_music_singer)
            layout.addWidget(qlabel_music_style)
            layout.addWidget(qlabel_music_time)
            layout.addWidget(play_button)

            self.music_layout.addRow(str(self.music_count), h)

            self.music_count = self.music_count + 1
    def process_time(self,second):
        min=int(second/60)
        sec=second%60
        return str(min)+':'+str(sec)
    def clear_music_form(self):#移除form布局
        for i in range(self.music_count+1):
            self.music_layout.removeRow(0)
    def get_user_history_form(self):#获得用户历史歌单
        self.history_form_user,self.history_form_info=self.mongo.get_user_music(self.ID)
    def get_recommend(self,music_list):#获得推荐的歌单数据
        return self.mongo.get_recommend_form(music_list)
    def play_music(self):#播放音乐
        btn=self.sender()
        self.music_name=btn.music_name
        address=btn.music_address
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content=QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def pause_music(self):#暂停和播放音乐
        btn = self.sender()
        if(btn.flag==True):
            self.player.pause()
        else:
            self.player.play()
        btn.auto_change()
    def set_dateDuration(self,duration):#设置进度条范围
        self.right_process_bar.setRange(0,duration)
        self.right_process_bar.setEnabled(duration>0)
    def update_position(self,position):#设置进度条范围
        self.right_process_bar.setValue(position)
    def find_music_singer(self):
        text=self.sousuo_input.text()
        out,singer_info=self.mongo.get_sousuo(text)
        if(len(out)==0):
            self.statusbar.showMessage('没有相关音乐或歌手', 3000)
        else:
            self.local_music_info=out
            self.show_sousuo()
            if(singer_info!=None):
                self.music_form_info.setText(singer_info)
    def play_next(self):#播放下一首歌
        music=self.music_name
        music_list=list(self.local_music_info)
        index_name=music_list.index(music)
        if(index_name==(len(music_list)-1)):
            index_name=0
        else:
            index_name=index_name+1
        self.music_name = music_list[index_name]
        address = self.local_music_info[self.music_name]['download_path']
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def play_before(self):#播放上一首歌
        music=self.music_name
        music_list=list(self.local_music_info)
        index_name=music_list.index(music)
        if(index_name==0):
            index_name=-1
        else:
            index_name=index_name-1
        self.music_name = music_list[index_name]
        address = self.local_music_info[self.music_name]['download_path']
        self.music_name_label.setText(self.music_name)
        self.mongo.update_music(self.ID, self.music_name)
        url = QUrl.fromLocalFile(address)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    def get_score(self):#更新分数
        btn=self.sender()
        d, okPressed = QInputDialog.getDouble(self, "请输入评分", "Value:", 10)
        self.mongo.update_score(self.ID,btn.music_name,d)
class work_algorithm_1(QtCore.QThread,QtCore.QObject):#推荐算法一，工作线程
    qt_signal = QtCore.pyqtSignal(str,list)

    def __init__(self, ID,parent=None):
        super(work_algorithm_1, self).__init__(parent)
        self.ID=ID

    def run(self):
        model=algorithms.my_model_nmf()
        model.init_datebase()
        model.train_model()
        song_list=model.recommed_song(self.ID)
        self.qt_signal.emit('已经完成协同过滤推荐',song_list)
class work_algorithm_2(QtCore.QThread,QtCore.QObject):#推荐算法二，工作线程
    qt_signal = QtCore.pyqtSignal(str,list)

    def __init__(self, ID,parent=None):
        super(work_algorithm_2, self).__init__(parent)
        self.ID=ID

    def run(self):
        model=algorithms.my_model_knn()
        model.init_datebase()
        song_list=model.recommend_Logistic(self.ID)
        self.qt_signal.emit('已经完成内容推荐',song_list)
app = QtWidgets.QApplication(sys.argv)

denglu_MainWindow=QtWidgets.QMainWindow()
denglu_ui=denglu_gui(denglu_MainWindow)
denglu_ui.show()

yindao_MainWindow=QtWidgets.QMainWindow()
yindao_ui=yindao_gui(yindao_MainWindow)

zhuce_MainWindow=QtWidgets.QMainWindow()
zhuce_ui=registered_gui(zhuce_MainWindow)

MainWindow1 = QtWidgets.QMainWindow()
main_gui=main_gui(MainWindow1)

zhuce_ui._signal.connect(denglu_ui.show_gui)
denglu_ui._signal_zhuce.connect(zhuce_ui.show_gui)
denglu_ui._signal_yindao.connect(yindao_ui.show_init)
yindao_ui._signal.connect(main_gui.show_gui_yindao)

denglu_ui._signal.connect(main_gui.show_gui)
sys.exit(app.exec_())
