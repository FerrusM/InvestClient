import sqlite3
from classes import TokenClass


class DbConnection:
    DATABASE_NAME = 'tinkoff_invest.db'
    TOKENS_TABLE = 'Tokens'
    CURRENT_DATETIME = 'CURRENT_TIMESTAMP'

    command_create_tokens_table = '''
        CREATE TABLE IF NOT EXISTS {0} (
        token TEXT NOT NULL, 
        name TEXT NOT NULL, 
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (token),
        UNIQUE (name))'''.format(
        TOKENS_TABLE,
        CURRENT_DATETIME
    )

    command_trigger_bu_changed = '''CREATE TRIGGER IF NOT EXISTS Tokens_AU_changed_at AFTER UPDATE OF changed_at ON {0}
    BEGIN
        UPDATE {0} SET changed_at = CURRENT_TIMESTAMP WHERE rowid = NEW.rowid;
    END;'''.format(TOKENS_TABLE)

    command_add_token = 'INSERT INTO {0} (token, name) VALUES (?, ?)'.format(TOKENS_TABLE)
    command_get_tokens = 'SELECT * FROM {0}'.format(TOKENS_TABLE)

    @classmethod
    def createDatabase(cls):
        """Создаёт базу данных."""
        connection = sqlite3.connect(cls.DATABASE_NAME)  # Создаем подключение к базе данных.
        cursor = connection.cursor()

        '''------Создание таблицы токенов------'''
        cursor.execute(cls.command_create_tokens_table)
        '''------------------------------------'''

        cursor.execute(cls.command_trigger_bu_changed)

        # cursor.execute(cls.command_trigger_bi_created)
        # cursor.execute(cls.command_trigger_bu_created)
        # cursor.execute(cls.command_trigger_ai_created)

        connection.commit()
        connection.close()

    @classmethod
    def addToken(cls, token: TokenClass):
        connection = sqlite3.connect(cls.DATABASE_NAME)  # Создаем подключение к базе данных.
        cursor = connection.cursor()

        flag: bool = True
        try:
            cursor.execute(cls.command_add_token, (token.token, token.name))
        except Exception as error:
            flag = False

        connection.commit()
        connection.close()
        return flag

    @classmethod
    def getTokens(cls) -> list[TokenClass]:
        tokens: list[TokenClass] = []
        connection = sqlite3.connect(cls.DATABASE_NAME)  # Создаем подключение к базе данных.
        cursor = connection.cursor()

        cursor.execute(cls.command_get_tokens)
        for record in cursor.fetchall():
            tokens.append(TokenClass(token=record[0], name=record[1]))

        connection.close()
        return tokens
