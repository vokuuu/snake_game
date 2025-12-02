import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка - Классическая игра")
        self.root.geometry("900x850")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a1a')
        
        # Размеры игрового поля
        self.cell_size = 20
        self.grid_width = 30
        self.grid_height = 25
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size
        
        # Цвета
        self.bg_color = '#1a1a1a'
        self.grid_color = '#2d2d2d'
        self.snake_color = '#4CAF50'
        self.snake_head_color = '#45a049'
        self.food_color = '#f44336'
        self.text_color = '#ffffff'
        
        # Игровые переменные
        self.score = 0
        self.high_score = 0
        self.game_speed = 100  # миллисекунды
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.game_running = False
        self.game_over = False
        
        # Создание интерфейса
        self.create_widgets()
        
        # Инициализация игры
        self.reset_game()
        
        # Связывание клавиш
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<space>', self.toggle_pause)
        self.root.focus_set()
        
        # Запуск игрового цикла
        self.game_loop()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        self.title_label = tk.Label(
            self.root,
            text="🐍 ЗМЕЙКА",
            font=('Arial', 24, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.title_label.pack(pady=10)
        
        # Панель счета
        self.score_frame = tk.Frame(self.root, bg=self.bg_color)
        self.score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"Счёт: {self.score}",
            font=('Arial', 14),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.score_label.pack(side='left', padx=20)
        
        self.high_score_label = tk.Label(
            self.score_frame,
            text=f"Рекорд: {self.high_score}",
            font=('Arial', 14),
            fg='#FFD700',
            bg=self.bg_color
        )
        self.high_score_label.pack(side='left', padx=20)
        
        # Игровое поле
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.bg_color,
            highlightthickness=2,
            highlightbackground='#333'
        )
        self.canvas.pack(pady=10)
        
        # Панель управления
        self.control_frame = tk.Frame(self.root, bg=self.bg_color)
        self.control_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            self.control_frame,
            text="СТАРТ",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=10,
            command=self.start_game
        )
        self.start_button.pack(side='left', padx=10)
        
        self.restart_button = tk.Button(
            self.control_frame,
            text="ЗАНОВО",
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            width=10,
            command=self.reset_game
        )
        self.restart_button.pack(side='left', padx=10)
        
        # Инструкция
        self.instruction_label = tk.Label(
            self.root,
            text="Управление: ← ↑ → ↓ или WASD • ПАУЗА: Пробел",
            font=('Arial', 10),
            fg='#888',
            bg=self.bg_color
        )
        self.instruction_label.pack(pady=5)

    def reset_game(self):
        """Сброс игры в начальное состояние"""
        # Позиция змейки (голова + 2 сегмента)
        self.snake = [
            (10, 12),  # голова
            (9, 12),   # сегмент 1
            (8, 12)    # сегмент 2
        ]
        
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.score = 0
        self.game_speed = 150
        self.game_running = False
        self.game_over = False
        
        # Создание первой еды
        self.create_food()
        
        # Обновление интерфейса
        self.update_score()
        self.draw_game()

    def create_food(self):
        """Создание еды в случайной позиции"""
        while True:
            self.food = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            # Проверяем, чтобы еда не появилась на змейке
            if self.food not in self.snake:
                break

    def start_game(self):
        """Запуск игры"""
        if not self.game_running and not self.game_over:
            self.game_running = True
            self.start_button.config(text="ПАУЗА", bg='#FF9800')
        elif self.game_running:
            self.game_running = False
            self.start_button.config(text="ПРОДОЛЖИТЬ", bg='#4CAF50')

    def toggle_pause(self, event=None):
        """Переключение паузы"""
        if self.game_running:
            self.game_running = False
            self.start_button.config(text="ПРОДОЛЖИТЬ", bg='#4CAF50')
        elif not self.game_over:
            self.game_running = True
            self.start_button.config(text="ПАУЗА", bg='#FF9800')

    def on_key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.keysym
        
        # Управление стрелками
        if key in ['Left', 'Right', 'Up', 'Down']:
            self.change_direction(key)
        
        # Управление WASD
        elif key.lower() in ['a', 'd', 'w', 's']:
            direction_map = {'a': 'Left', 'd': 'Right', 'w': 'Up', 's': 'Down'}
            self.change_direction(direction_map[key.lower()])
        
        # Запуск игры пробелом (если игра не идет)
        elif key == 'space' and not self.game_running and not self.game_over:
            self.start_game()

    def change_direction(self, new_direction):
        """Изменение направления движения"""
        # Проверка на противоположное направление
        opposite_directions = {
            'Left': 'Right', 'Right': 'Left',
            'Up': 'Down', 'Down': 'Up'
        }
        
        if not self.game_over and new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction

    def move_snake(self):
        """Движение змейки"""
        if not self.game_running or self.game_over:
            return
            
        # Обновляем направление
        self.direction = self.next_direction
        
        # Получаем текущую позицию головы
        head_x, head_y = self.snake[0]
        
        # Вычисляем новую позицию головы
        direction_map = {
            'Left': (-1, 0),
            'Right': (1, 0),
            'Up': (0, -1),
            'Down': (0, 1)
        }
        
        dx, dy = direction_map[self.direction]
        new_head = (head_x + dx, head_y + dy)
        
        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.end_game()
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.end_game()
            return
        
        # Добавляем новую голову
        self.snake.insert(0, new_head)
        
        # Проверка съедания еды
        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.create_food()
            
            # Увеличение скорости каждые 50 очков
            if self.score % 50 == 0 and self.game_speed > 50:
                self.game_speed -= 10
        else:
            # Удаляем хвост, если не съели еду
            self.snake.pop()

    def update_score(self):
        """Обновление счета на экране"""
        self.score_label.config(text=f"Счёт: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"Рекорд: {self.high_score}")

    def end_game(self):
        """Завершение игры"""
        self.game_running = False
        self.game_over = True
        self.start_button.config(text="ИГРА ОКОНЧЕНА", bg='#f44336')

    def draw_game(self):
        """Отрисовка игрового поля"""
        self.canvas.delete("all")
        
        # Рисуем сетку (опционально)
        self.draw_grid()
        
        # Рисуем змейку
        for i, (x, y) in enumerate(self.snake):
            color = self.snake_head_color if i == 0 else self.snake_color
            self.draw_cell(x, y, color)
            
            # Добавляем глаза на голову
            if i == 0:
                self.draw_eyes(x, y)
        
        # Рисуем еду
        self.draw_cell(self.food[0], self.food[1], self.food_color)
        
        # Сообщение о паузе
        if not self.game_running and not self.game_over:
            self.canvas.create_text(
                self.canvas_width // 2,
                self.canvas_height // 2,
                text="НАЖМИТЕ СТАРТ ДЛЯ НАЧАЛА",
                fill='white',
                font=('Arial', 16, 'bold')
            )
        
        # Сообщение о конце игры
        if self.game_over:
            self.canvas.create_text(
                self.canvas_width // 2,
                self.canvas_height // 2,
                text="ИГРА ОКОНЧЕНА!",
                fill='#f44336',
                font=('Arial', 20, 'bold')
            )

    def draw_grid(self):
        """Отрисовка сетки игрового поля"""
        for x in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=self.grid_color, width=1)
        for y in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill=self.grid_color, width=1)

    def draw_cell(self, x, y, color):
        """Отрисовка одной клетки"""
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        
        # Основной квадрат
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
        
        # Эффект объема
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='', outline=color, width=1)

    def draw_eyes(self, x, y):
        """Рисуем глаза на голове змейки"""
        eye_size = self.cell_size // 5
        direction_offsets = {
            'Right': [(-0.3, -0.3), (-0.3, 0.3)],
            'Left': [(0.3, -0.3), (0.3, 0.3)],
            'Up': [(-0.3, 0.3), (0.3, 0.3)],
            'Down': [(-0.3, -0.3), (0.3, -0.3)]
        }
        
        offsets = direction_offsets.get(self.direction, [(-0.3, -0.3), (-0.3, 0.3)])
        
        for dx, dy in offsets:
            eye_x = (x + 0.5 + dx) * self.cell_size
            eye_y = (y + 0.5 + dy) * self.cell_size
            self.canvas.create_oval(
                eye_x - eye_size, eye_y - eye_size,
                eye_x + eye_size, eye_y + eye_size,
                fill='white', outline=''
            )

    def game_loop(self):
        """Главный игровой цикл"""
        self.move_snake()
        self.draw_game()
        
        # Продолжаем цикл
        self.root.after(self.game_speed, self.game_loop)


def main():
    """Запуск игры"""
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()