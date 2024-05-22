import socket
from PyQt6 import QtWidgets
from TokensPage import TokensModel, TokensPage


HOST: str = ''  # Строка, представляющая либо имя хоста в нотации домена Интернета, либо IPv4-адрес.
PORT: int = 12883


class Form(QtWidgets.QMainWindow):
    """Главная форма."""
    def __init__(self, tokens_model: TokensModel, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.resize(900, 500)
        self.setWindowTitle('Тинькофф Инвестиции')

        '''====================================Ui_MainWindow===================================='''
        '''------------------------------Создаём CentralWidget------------------------------'''
        central_widget = QtWidgets.QWidget(parent=self)

        main_verticalLayout = QtWidgets.QVBoxLayout(central_widget)
        main_verticalLayout.setContentsMargins(1, 1, 0, 0)
        main_verticalLayout.setSpacing(0)

        '''------------------------------Создаём tabWidget------------------------------'''
        self.tabWidget = QtWidgets.QTabWidget(parent=central_widget)  # Панель вкладок.

        self.tab_tokens = TokensPage(tokens_model=tokens_model, parent=self)  # Страница "Токены".
        self.tabWidget.addTab(self.tab_tokens, 'Токены')
        '''-----------------------------------------------------------------------------'''

        main_verticalLayout.addWidget(self.tabWidget)
        '''---------------------------------------------------------------------------------'''

        self.setCentralWidget(central_widget)
        '''====================================================================================='''

        self.__socket: socket.socket | None = None

    def connect(self) -> bool:
        if self.__socket is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address: tuple[str, int] = (HOST, PORT)
            try:
                self.__socket.connect(address)  # Подключаемся к серверному сокету.
            except Exception as error:
                self.__socket.close()
                self.__socket = None
                print('Соединение не установлено. Ошибка: {0}.'.format(error))
                return False
            else:  # Если исключения не было.
                print('Соединение с сервером успешно установлено.')
                return True
        else:
            return False

    def close_connection(self):
        # self.stopAutoupdate()
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None
        print('Соединение отсутствует! Попробуйте переподключиться!')
