import tkinter as tk
import numpy as np


class GameOfLife:
    def __init__(self, master, size=50, cell_size=10):
        self.master = master
        self.size = size  # Размер поля (количество клеток в каждом направлении)
        self.cell_size = cell_size  # Размер клетки в пикселях
        self.canvas = tk.Canvas(master, width=size * cell_size, height=size * cell_size)  # Создание холста
        self.canvas.pack()
        # Создание начальной случайной конфигурации клеток
        self.board = np.random.choice([0, 1], (size, size))
        self.running = False  # Флаг для отслеживания состояния симуляции

    def draw_board(self):
        # Очистка холста
        self.canvas.delete('cells')
        # Отрисовка клеток
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    # Заполнение клетки черным цветом, если она жива
                    self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                                 (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                                 fill='black', tags='cells')

    def next_generation(self):
        new_board = np.zeros((self.size, self.size), dtype=int)
        # Подсчет следующего поколения клеток на основе правил игры
        for i in range(self.size):
            for j in range(self.size):
                # Подсчет числа соседей для каждой клетки
                neighbors = np.sum(self.board[max(0, i - 1):min(self.size, i + 2),
                                   max(0, j - 1):min(self.size, j + 2)]) - self.board[i][j]
                if self.board[i][j]:
                    # Если клетка жива, она остается живой, если у нее 2 или 3 соседа
                    if neighbors == 2 or neighbors == 3:
                        new_board[i][j] = 1
                else:
                    # Если клетка мертва, она становится живой, если у нее 3 соседа
                    if neighbors == 3:
                        new_board[i][j] = 1
        self.board = new_board

    def step(self):
        # Выполнение одного шага симуляции
        self.next_generation()
        self.draw_board()
        # Если симуляция запущена, вызываем следующий шаг через 100 миллисекунд
        if self.running:
            self.master.after(100, self.step)

    def start_stop(self):
        # Функция запускает или останавливает симуляцию
        if self.running:
            self.running = False
        else:
            self.running = True
            self.step()


def main():
    # Создание главного окна приложения
    root = tk.Tk()
    # Установка заголовка окна
    root.title("Game of Life")
    # Создание экземпляра игры, передавая главное окно в качестве родительского виджета
    game = GameOfLife(root)
    # Создание кнопки "Start/Stop" для запуска и остановки симуляции, связанной с методом start_stop экземпляра game
    start_stop_button = tk.Button(root, text="Start/Stop", command=game.start_stop)
    # Размещение кнопки на главном окне
    start_stop_button.pack()
    # Отрисовка начального состояния игры
    game.draw_board()
    # Запуск главного цикла обработки событий Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
