import threading


class Mutex:
    def __init__(self, _name: str):
        self.__name = _name
        self.__lock_id = None
        self.__lock = True

    @property
    def name(self):
        return self.__name

    @property
    def lock(self):
        return self.__lock

    def LOCK(self):
        while self.lock:
            ...

        _lock_id = threading.get_ident()

        if self.__lock_id is None or self.__lock_id == _lock_id:
            self.__lock = True
            self.__lock_id = _lock_id
        else:
            self.LOCK()

    def UNLOCK(self):
        self.__lock = False
        self.__lock_id = None
