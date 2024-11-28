from queue import Queue
import time
import threading
import random


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        time.sleep(random.randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        local_table = self.tables[0]
        is_busy = False
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    is_busy = True
                    local_table = table
                    break
                else:
                    is_busy = False
                    continue

            if is_busy:
                local_table.guest = guest
                guest.start()
                print(f'{guest.name} сел(-а) за стол номер {local_table.number}')
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty():
            for table in self.tables:
                if table.guest is not None:
                    # обслуживанике началось
                    if table.guest.is_alive():
                        pass
                    else:
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

                        if not self.queue.empty():
                            table.guest = self.queue.get()
                            table.guest.start()
                            print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
