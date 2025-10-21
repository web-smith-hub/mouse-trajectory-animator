import pyautogui
import time
import math
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MouseAnimator:
    def __init__(self):
        self.is_running = False
        self.duration = 10
        self.trajectory_type = "random"
        self.speed = 1.0
        self.amplitude = 100
        self.frequency = 0.1
        
    def random_trajectory(self, duration):
        """Хаотичная траектория с случайными точками"""
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        
        while time.time() - start_time < duration and self.is_running:
            x = random.randint(50, screen_width - 50)
            y = random.randint(50, screen_height - 50)
            
            move_duration = random.uniform(0.5, 2.0) / self.speed
            pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeInOutQuad)
            time.sleep(random.uniform(0.1, 0.5))
            
    def circular_trajectory(self, duration):
        """Круговая траектория"""
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        angle = 0
        while time.time() - start_time < duration and self.is_running:
            x = center_x + self.amplitude * math.cos(angle)
            y = center_y + self.amplitude * math.sin(angle)
            
            pyautogui.moveTo(x, y, duration=0.01)
            angle += self.frequency * self.speed
            time.sleep(0.01)
            
    def wave_trajectory(self, duration):
        """Волнообразная траектория"""
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        center_y = screen_height // 2
        
        x = 50
        while time.time() - start_time < duration and self.is_running:
            y = center_y + self.amplitude * math.sin(x * self.frequency)
            
            if x > screen_width - 50:
                x = 50
            
            pyautogui.moveTo(x, y, duration=0.01)
            x += 2 * self.speed
            time.sleep(0.01)
            
    def zigzag_trajectory(self, duration):
        """Зигзагообразная траектория"""
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        
        x, y = 50, 50
        direction_x, direction_y = 1, 1
        
        while time.time() - start_time < duration and self.is_running:
            x += 5 * self.speed * direction_x
            y += 3 * self.speed * direction_y
            
            if x >= screen_width - 50 or x <= 50:
                direction_x *= -1
            if y >= screen_height - 50 or y <= 50:
                direction_y *= -1
                
            pyautogui.moveTo(x, y, duration=0.01)
            time.sleep(0.02)
            
    def figure_eight_trajectory(self, duration):
        """Траектория в форме восьмерки"""
        start_time = time.time()
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        t = 0
        while time.time() - start_time < duration and self.is_running:
            x = center_x + self.amplitude * math.sin(t)
            y = center_y + self.amplitude * math.sin(2 * t) / 2
            
            pyautogui.moveTo(x, y, duration=0.01)
            t += self.frequency * self.speed
            time.sleep(0.01)
            
    def start_animation(self):
        """Запуск анимации в отдельном потоке"""
        if self.is_running:
            return
            
        self.is_running = True
        
        trajectories = {
            "random": self.random_trajectory,
            "circular": self.circular_trajectory,
            "wave": self.wave_trajectory,
            "zigzag": self.zigzag_trajectory,
            "figure_eight": self.figure_eight_trajectory
        }
        
        trajectory_func = trajectories.get(self.trajectory_type, self.random_trajectory)
        
        def run_animation():
            try:
                trajectory_func(self.duration)
            finally:
                self.is_running = False
                
        thread = threading.Thread(target=run_animation)
        thread.daemon = True
        thread.start()
        
    def stop_animation(self):
        """Остановка анимации"""
        self.is_running = False

class MouseAnimatorGUI:
    def __init__(self):
        self.animator = MouseAnimator()
        self.setup_gui()
        self.load_settings()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Mouse Trajectory Animator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Длительность
        ttk.Label(main_frame, text="Длительность (сек):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.duration_var = tk.DoubleVar(value=10)
        duration_spin = ttk.Spinbox(main_frame, from_=1, to=60, width=10, textvariable=self.duration_var)
        duration_spin.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Тип траектории
        ttk.Label(main_frame, text="Тип траектории:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.trajectory_var = tk.StringVar(value="random")
        trajectory_combo = ttk.Combobox(main_frame, textvariable=self.trajectory_var, width=15)
        trajectory_combo['values'] = ('random', 'circular', 'wave', 'zigzag', 'figure_eight')
        trajectory_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Скорость
        ttk.Label(main_frame, text="Скорость:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(main_frame, from_=0.1, to=3.0, variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Амплитуда
        ttk.Label(main_frame, text="Амплитуда:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.amplitude_var = tk.IntVar(value=100)
        amplitude_spin = ttk.Spinbox(main_frame, from_=50, to=300, width=10, textvariable=self.amplitude_var)
        amplitude_spin.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Частота
        ttk.Label(main_frame, text="Частота:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.frequency_var = tk.DoubleVar(value=0.1)
        frequency_scale = ttk.Scale(main_frame, from_=0.01, to=0.5, variable=self.frequency_var, orient=tk.HORIZONTAL)
        frequency_scale.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Запустить", command=self.start_animation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Остановить", command=self.stop_animation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Сохранить настройки", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к запуску")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Привязка изменений
        self.duration_var.trace('w', self.update_settings)
        self.trajectory_var.trace('w', self.update_settings)
        self.speed_var.trace('w', self.update_settings)
        self.amplitude_var.trace('w', self.update_settings)
        self.frequency_var.trace('w', self.update_settings)
        
    def update_settings(self, *args):
        """Обновление настроек аниматора"""
        self.animator.duration = self.duration_var.get()
        self.animator.trajectory_type = self.trajectory_var.get()
        self.animator.speed = self.speed_var.get()
        self.animator.amplitude = self.amplitude_var.get()
        self.animator.frequency = self.frequency_var.get()
        
    def start_animation(self):
        """Запуск анимации"""
        self.update_settings()
        self.animator.start_animation()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set(f"Анимация запущена на {self.animator.duration} сек")
        
        # Таймер для автоматического завершения
        self.root.after(int(self.animator.duration * 1000 + 500), self.check_animation_status)
        
    def stop_animation(self):
        """Остановка анимации"""
        self.animator.stop_animation()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Анимация остановлена")
        
    def check_animation_status(self):
        """Проверка статуса анимации"""
        if not self.animator.is_running:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_var.set("Анимация завершена")
        else:
            self.root.after(500, self.check_animation_status)
            
    def save_settings(self):
        """Сохранение настроек в файл"""
        settings = {
            'duration': self.duration_var.get(),
            'trajectory_type': self.trajectory_var.get(),
            'speed': self.speed_var.get(),
            'amplitude': self.amplitude_var.get(),
            'frequency': self.frequency_var.get()
        }
        
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Успех", "Настройки сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {e}")
            
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                self.duration_var.set(settings.get('duration', 10))
                self.trajectory_var.set(settings.get('trajectory_type', 'random'))
                self.speed_var.set(settings.get('speed', 1.0))
                self.amplitude_var.set(settings.get('amplitude', 100))
                self.frequency_var.set(settings.get('frequency', 0.1))
                
                self.update_settings()
        except Exception:
            pass
            
    def run(self):
        """Запуск GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Обработка закрытия окна"""
        self.animator.stop_animation()
        self.root.destroy()

if __name__ == "__main__":
    # Отключение fail-safe PyAutoGUI
    pyautogui.FAILSAFE = False
    
    # Запуск приложения
    app = MouseAnimatorGUI()
    app.run()
