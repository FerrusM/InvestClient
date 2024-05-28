import pickle
import socket
from common.protocol import ClientRequest, Commands, ServerResponse

# HOST: str = ''  # Строка, представляющая либо имя хоста в нотации домена Интернета, либо IPv4-адрес.
HOST: str = 'localhost'
PORT: int = 12883


class ConnectionWithServer:
    def __init__(self):
        self.__socket: socket.socket | None = None
        ...

    def connection(self) -> bool:
        if self.__socket is None:
            return False
        else:
            ...

    def open_connection(self) -> bool:
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
                print('Соединение с сервером успешно установлено. Реквизиты {0}.'.format(self.__socket.getpeername()))
                return True
        else:
            return False

    def close_connection(self):
        # self.stopAutoupdate()
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None
        print('Соединение отсутствует! Попробуйте переподключиться!')

    def add_token(self, token: str) -> bool:
        request = ClientRequest(command=Commands.ADD_TOKEN, data=token)
        dump = pickle.dumps(request)  # Сериализация.
        try:
            self.__socket.send(dump)  # Отправляем сообщение.
        except ConnectionResetError as cre:
            print('Функция: socket.send. Ошибка: {0}.'.format(cre))
            return False
        except Exception as error:
            print('Функция: socket.send. Ошибка: {0}.'.format(error))
            return False
        else:  # Если исключения не было.
            try:
                data = self.__socket.recv(1024)  # Получаем список телефонных номеров.
            except Exception as error:
                print('Функция: socket.recv. Ошибка: {0}.'.format(error))
                return False
            else:  # Если исключения не было.
                response = pickle.loads(data)
                if isinstance(response, ServerResponse):
                    if response.command == Commands.ADD_TOKEN:
                        if response.flag:
                            print('Добавление успешно выполнено.')
                            return True
                        else:
                            print('Ошибка выполнения запроса ({0}) на сервере!'.format(response.command))
                            return False
                    else:
                        print('Ответ сервера ({0}) не соответствует запросу ({1})!'.format(response.command, request.command))
                        return False
                else:
                    print('Некорректный тип сообщения от сервера ({0})!'.format(type(response)))
                    return False
