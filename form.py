from PyQt6 import QtWidgets
from TokensPage import TokensModel, TokensPage


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
