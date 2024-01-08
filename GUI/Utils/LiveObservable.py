class LiveObservable:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify_observers(self, message):
        for observer in self._observers:
            observer.notify(message)


class LiveObserver:
    def notify(self, message):
        raise NotImplementedError("You must implement the notify method.")


class MessageDisplay(LiveObserver):
    def notify(self, message):
        print(f"Received message: {message}")
