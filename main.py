from PyQt6 import QtWidgets
from TokensPage import TokensModel
from database import DbConnection
from form import Form

if __name__ == '__main__':
    DbConnection.createDatabase()
    tokens_model = TokensModel()  # Модель токенов.
    tokens_model.setTokens(DbConnection.getTokens())

    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('InvestmentViewer')
    app.setOrganizationName('Ferrus Company')
    window = Form(tokens_model=tokens_model)
    window.show()
    sys.exit(app.exec())
