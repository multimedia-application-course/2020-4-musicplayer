# coding utf8
"""
@author: xinhong
@function: music player
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import requests, traceback
import qtawesome as qta
import sys


class MusicPlayer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.custom_style()
        self.playing = False #播放初始化状态
        self.player = QMediaPlayer(self)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.check_music_status)
    
    # 设置样式
    def custom_style(self):
        self.setStyleSheet('''
            #main_widget{
                border-radius:5px;
            }
            #play_btn,#pervious_btn,#next_btn{
                border:none;
            }
            #play_btn:hover,#pervious_btn:hover,#next_btn:hover{
                background:gray;
                border-radius:5px;
                cursor:pointer;
            }
            #main_widget
            {
            border-image:url(./p4.jpg);
            }
        ''')
        self.close_btn.setStyleSheet('''
            QPushButton{
                background:#F76677;
                border-radius:5px;
                }
            QPushButton:hover{
                background:red;
                }''')
        self.status_label.setStyleSheet('''
            QLabel{
                background:#F7D674;
                border-radius:5px;
                }
        ''')
        
        
        
        
    
    def init_ui(self):
        self.setFixedSize(960, 700)
        self.setWindowTitle("TEAM 刘鑫泓 梁志健 MusicPlayer")
        #窗口布局
        self.main_widget = QtWidgets.QWidget() 
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        # 标题
        self.title_lable = QtWidgets.QLabel("")

        # 关闭按钮
        self.close_btn = QtWidgets.QPushButton("")  # 关闭按钮
        self.close_btn.clicked.connect(self.close_event)
        self.close_btn.setFixedSize(15,15)

        # 音乐状态按钮
        self.status_label = QtWidgets.QLabel("")
        # self.swith_btn.clicked.connect(self.swith_background)
        self.status_label.setFixedSize(15,15)

        # 播放按钮
        play_icon = qta.icon("fa.play-circle",)
        self.play_btn = QtWidgets.QPushButton(play_icon,"")
        self.play_btn.setIconSize(QtCore.QSize(80, 80))
        self.play_btn.setFixedSize(82,82)
        self.play_btn.setObjectName("play_btn")
        self.play_btn.clicked.connect(self.play_music)

        # 下一首按钮
        next_icon = qta.icon("fa.play-circle-o")
        self.next_btn = QtWidgets.QPushButton(next_icon,"")
        self.next_btn.setIconSize(QtCore.QSize(80,80))
        self.next_btn.setFixedSize(82,82)
        self.next_btn.setObjectName("next_btn")
        self.next_btn.clicked.connect(self.next_music)
        # 进度条
        self.process_bar = QtWidgets.QProgressBar()
        self.process_value = 0
        self.process_bar.setValue(self.process_value)
        self.process_bar.setFixedHeight(5)
        self.process_bar.setTextVisible(False)
        self.main_layout.addWidget(self.close_btn,0,0,1,1)
        self.main_layout.addWidget(self.title_lable,0,1,1,1)
        self.main_layout.addWidget(self.status_label,1,0,1,1)
        self.main_layout.addWidget(self.play_btn, 1, 1, 1, 1)
        self.main_layout.addWidget(self.next_btn, 1, 2, 1, 1)
        self.main_layout.addWidget(self.process_bar,2,0,1,3)
        self.setCentralWidget(self.main_widget)
        self.setWindowOpacity(0.5) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边
    
    #关闭事件
    def close_event(self):
        self.close()
    
    #鼠标长按事件
    def mousePressEvent(self, QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    
    #鼠标移动
    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()
    
    #s鼠标释放
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QtDui.QCursor(QtCore.Qt.ArrowCursor))
    
    #初始化播放器
    def init_player(self, url):
        #print('url', url)
        content = QMediaContent(QtCore.QUrl(url))
        self.player.setMedia(content)
        self.player.setVolume(50)
        self.player.play()
        self.duration = self.player.duration()
        
        self.status_label.setStyleSheet('''
        QLabel{
            background:#6DDF6D;
            border-radius:5px;
        }
        ''')
        
        #进度条计时
        self.process_timer = QtCore.QTimer()
        self.process_timer.setInterval(1000)
        self.process_timer.start()
        self.process_timer.timeout.connect(self.process_timer_status)
    
    #播放音乐
    def play_music(self):
        try:
            #播放
            if self.playing is False:
                self.playing = True #设置播放状态
                self.play_btn.setIcon(qta.icon("fa.pause-circle"))
                player_status =  self.player.mediaStatus() #获取播放装填
                #print("player_status:{}".format(player_status))
                if player_status == 6:
                    #设置装填标签颜色绿色
                    self.status_label.setStyleSheet('''
                    QLabel{
                    background:#0099CC;
                    border-radius:5px;
                    }
                    '''

                        
                    )
                else:
                    self.next_music() #下一首
            #pause
            else:
                #设置状态为蓝色
                self.status_label.setStyleSheet('''
                QLabel{
                background:#0099CC;
                border-radius:5px;
                }
                ''')
                self.playing = False #更改状态
                self.play_btn.setIcon(qta.icon("fa.play-circle"))#设置播放秃瓢
                self.player.pause()
        except Exception as e:
            print('184{}'.format(e.__class__.__name__), end='')
            print(e)
                
                                                    
    
    #下一首音乐
    def next_music(self):
        try:
            #设置状态为黄色
            self.status_label.setStyleSheet('''
            QLabel{
                    background:#F7D674;
                    border-radius:5px;
            }
            ''')
            self.playing = True
            self.play_btn.setIcon(qta.icon("fa.pause-circle"))#修改图标
            self.process_value = 0 #重置进度条
            
            #获取歌曲
            self.get_music_thread = GetMusicThread()
            self.get_music_thread.finished_signel.connect(self.init_player)
            self.get_music_thread.start()
        except Exception as e:
            print('207{}'.format(e.__class__.__name__), end='')
            print(e)
    
    
    def check_music_status(self):
        player_status = self.player.mediaStatus()#获取播放器状态
        player_duration = self.player.duration()#获取播放器时长
        #print('duration: {}'.format(player_duration))
        #print('status: {}'.format(player_status))
        
        #播放下一首
        if player_status == 7:
            self.next_music()
        
        if player_duration > 0:
            self.duration = player_duration
    
    #进度条dignshiqi
    def process_timer_status(self):
        try:
            if self.playing is True:
                self.process_value += (100 / (self.duration/1000))
                #print("当前进度: {}".format(self.process_value))
                self.process_bar.setValue(self.process_value)
        except Exception as e:
            print("232{}:".format(e.__class__.__name__), end='')
            print(e)
            

class GetMusicThread(QtCore.QThread):
    finished_signel = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        reps = requests.post("https://api.uomg.com/api/rand.music?sort=热歌榜&format=json")
        #print(reps.json())
        file_url= reps.json()['data']['url']
        self.finished_signel.emit(file_url)



def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MusicPlayer()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()