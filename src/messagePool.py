from queue import Queue


class MessagePool:
    def __init__(self):
        self.message_queue = Queue()

    def add_message(self, message):
        self.message_queue.put(message)

    def get_message(self):
        if not self.message_queue.empty():
            return self.message_queue.get()
        else:
            return None

    def has_messages(self):
        return not self.message_queue.empty()

    def clear_all_messages(self):
        with self.message_queue.mutex:
            self.message_queue.queue.clear()
