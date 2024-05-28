import typing
from PyQt6 import QtCore, QtWidgets, QtGui
from common import Header, ColumnWithHeader
from database import DbConnection
from classes import TokenClass


class TokensModel(QtCore.QAbstractItemModel):
    """Модель токенов."""
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self.__columns: tuple[ColumnWithHeader, ...] = (
            ColumnWithHeader(
                header=Header(
                    title='Имя',
                    tooltip='Имя токена.'
                ),
                data_function=lambda token: token.name),
            ColumnWithHeader(
                header=Header(
                    title='Токен',
                    tooltip='Токен.'
                ),
                data_function=lambda token: token.token)
        )
        self.__tokens: list[TokenClass] = []

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.__tokens)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.__columns)

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        column: ColumnWithHeader = self.__columns[index.column()]
        token: TokenClass = self.__tokens[index.row()]
        return column(role, token)

    def parent(self, child: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = ...) -> QtCore.QModelIndex:
        return self.createIndex(row, column)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == QtCore.Qt.Orientation.Vertical:
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return section + 1  # Проставляем номера строк.
        elif orientation == QtCore.Qt.Orientation.Horizontal:
            return self.__columns[section].header(role=role)

    def setTokens(self, tokens: list[TokenClass]):
        self.beginResetModel()
        self.__tokens = tokens
        self.endResetModel()


TITLE_FONT = QtGui.QFont()
TITLE_FONT.setPointSize(9)
TITLE_FONT.setBold(True)


class TitleLabel(QtWidgets.QLabel):
    """Класс QLabel'а-заголовка."""
    def __init__(self, text: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(text=text, parent=parent)
        self.setFont(TITLE_FONT)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)


class TitleWithCount(QtWidgets.QHBoxLayout):
    """Виджет, представляющий собой отцентрированный заголовок с QLabel'ом количества чего-либо в правом углу."""
    def __init__(self, title: str, count_text: str = '0', parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setSpacing(0)

        self.addSpacing(10)
        self.addStretch(1)
        self.addWidget(TitleLabel(text=title, parent=parent), 0)

        self.__label_count = QtWidgets.QLabel(text=count_text, parent=parent)
        self.__label_count.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.addWidget(self.__label_count, 1)

        self.addSpacing(10)

    def setCount(self, count_text: str | None):
        self.__label_count.setText(count_text)


class SavedTokensPanel(QtWidgets.QGroupBox):
    """Панель отображения сохранённых токенов."""
    def __init__(self, tokens_model: TokensModel, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        verticalLayout_main = QtWidgets.QVBoxLayout(self)
        verticalLayout_main.setContentsMargins(2, 2, 2, 2)
        verticalLayout_main.setSpacing(2)

        self.titlebar = TitleWithCount(title='СОХРАНЁННЫЕ ТОКЕНЫ', count_text='0', parent=self)
        verticalLayout_main.addLayout(self.titlebar, 0)

        self.tableView = QtWidgets.QTableView(parent=self)
        # self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        # self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # self.tableView.setSortingEnabled(True)
        self.tableView.setModel(tokens_model)
        verticalLayout_main.addWidget(self.tableView, 1)
        self.__onModelUpdate()

        tokens_model.modelReset.connect(self.__onModelUpdate)

    @QtCore.pyqtSlot()
    def __onModelUpdate(self):
        self.tableView.resizeColumnsToContents()  # Авторазмер столбцов под содержимое.
        self.titlebar.setCount(str(self.tableView.model().rowCount()))

    def model(self) -> TokensModel:
        """Возвращает модель."""
        model = self.tableView.model()
        assert type(model) is TokensModel
        return typing.cast(TokensModel, model)

    # def onUpdateView(self):
    #     """Выполняется после обновления модели."""
    #     self.treeView_saved_tokens.expandAll()  # Разворачивает все элементы.
    #     self.treeView_saved_tokens.resizeColumnsToContents()  # Авторазмер всех столбцов под содержимое.
    #     self.titlebar.setCount(str(self.model().getTokensCount()))  # Отображаем количество сохранённых токенов.


class AddTokenPanel(QtWidgets.QGroupBox):
    """Панель добавления токенов."""
    add_token_signal = QtCore.pyqtSignal(TokenClass)  # Сигнал, испускаемый при необходимости добавить токен в модель.

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        verticalLayout_main = QtWidgets.QVBoxLayout(self)
        verticalLayout_main.setContentsMargins(2, 2, 2, 2)
        verticalLayout_main.setSpacing(2)

        title = TitleLabel(text='НОВЫЙ ТОКЕН', parent=self)
        verticalLayout_main.addWidget(title, 0)

        """-------------Строка добавления нового токена-------------"""
        horizontalLayout = QtWidgets.QHBoxLayout(self)
        horizontalLayout.setSpacing(2)

        self.lineEdit_new_token = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_new_token.setPlaceholderText('Введите токен')
        horizontalLayout.addWidget(self.lineEdit_new_token, 3)

        self.lineEdit_token_name = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_token_name.setPlaceholderText('Введите имя токена')
        horizontalLayout.addWidget(self.lineEdit_token_name, 1)

        self.pushButton_save_token = QtWidgets.QPushButton(text='Сохранить', parent=self)
        self.pushButton_save_token.setEnabled(False)  # Кнопка "Сохранить" для нового токена д.б. неактивна по умолчанию.
        horizontalLayout.addWidget(self.pushButton_save_token, 0)

        verticalLayout_main.addLayout(horizontalLayout)
        """---------------------------------------------------------"""

        self.lineEdit_new_token.textChanged.connect(self.__addedTokenChanged_slot)
        self.pushButton_save_token.clicked.connect(self.__addToken)

    @QtCore.pyqtSlot(str)
    def __addedTokenChanged_slot(self, text: str):
        """Событие при изменении добавляемого токена."""
        self.pushButton_save_token.setEnabled(bool(text))

    @QtCore.pyqtSlot()
    def __addToken(self):
        """Добавляет токен."""
        self.lineEdit_new_token.setEnabled(False)
        self.lineEdit_token_name.setEnabled(False)

        token = TokenClass(token=self.lineEdit_new_token.text(), name=self.lineEdit_token_name.text())
        self.add_token_signal.emit(token)

        self.lineEdit_new_token.clear()
        self.lineEdit_token_name.clear()
        self.lineEdit_new_token.setEnabled(True)
        self.lineEdit_token_name.setEnabled(True)


class TokensPage(QtWidgets.QWidget):
    add_token_signal = QtCore.pyqtSignal(TokenClass)  # Сигнал, испускаемый при необходимости добавить токен в модель.

    """Страница токенов."""
    def __init__(self, tokens_model: TokensModel, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        verticalLayout_main = QtWidgets.QVBoxLayout(self)
        verticalLayout_main.setContentsMargins(2, 2, 2, 2)
        verticalLayout_main.setSpacing(2)

        self.tokensView = SavedTokensPanel(tokens_model=tokens_model, parent=self)
        verticalLayout_main.addWidget(self.tokensView, 1)

        '''----------------Панель добавления нового токена----------------'''
        self.groupBox_new_token = AddTokenPanel(parent=self)
        self.groupBox_new_token.add_token_signal.connect(self.add_token_signal.emit)
        verticalLayout_main.addWidget(self.groupBox_new_token, 0)
        '''---------------------------------------------------------------'''

    # @QtCore.pyqtSlot(TokenClass)
    # def __addToken_slot(self, token: TokenClass):
    #     response_
    #
    #     if DbConnection.addToken(token):
    #         self.tokensView.model().setTokens(DbConnection.getTokens())
    #     else:
    #         ...
