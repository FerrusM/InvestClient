from PyQt6 import QtWidgets, QtCore
from TokensPage import TokensModel
from classes import TokenClass
from connection import ConnectionWithServer
from database import DbConnection
from form import Form

# HOST: str = ''  # Строка, представляющая либо имя хоста в нотации домена Интернета, либо IPv4-адрес.
HOST: str = 'localhost'
PORT: int = 12883

if __name__ == '__main__':
    DbConnection.createDatabase()
    tokens_model = TokensModel()  # Модель токенов.
    tokens_model.setTokens(DbConnection.getTokens())

    __connection = ConnectionWithServer()

    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('InvestmentViewer')
    app.setOrganizationName('Ferrus Company')
    window = Form(tokens_model=tokens_model)

    assert __connection.open_connection()

    @QtCore.pyqtSlot(TokenClass)
    def __addToken_slot(token: TokenClass):
        if __connection.add_token(token.token):
            if DbConnection.addToken(token):
                window.tab_tokens.tokensView.model().setTokens(DbConnection.getTokens())
            else:
                raise SystemError('Не получилось добавить токен в бд!')
        else:
            raise SystemError('Не получилось отправить токен на сервер!')

    window.tab_tokens.add_token_signal.connect(__addToken_slot)
    window.show()
    status: int = app.exec()
    __connection.close_connection()
    sys.exit(status)
