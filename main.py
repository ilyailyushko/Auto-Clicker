import json
import os
import time
import pyautogui
from pynput import mouse

def list_files():
    files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('_clicks.json')]
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    return files

def record_clicks(scenario_name):
    # Словарь для хранения координат кликов
    click_dict = {}
    click_count = 0

    def on_click(x, y, button, pressed):
        nonlocal click_count
        if pressed:
            click_count += 1
            click_dict[click_count] = (x, y)
            print(f'Клик мыши по координатам ({x}, {y})')

    # Запуск прослушивателя событий мыши
    with mouse.Listener(on_click=on_click) as listener:
        print("Нажмите любую кнопку мыши, чтобы получить координаты. Для выхода нажмите Ctrl+C.")
        try:
            listener.join()
        except KeyboardInterrupt:
            print("Сценарий прерван. Вот записанные клики:")
            print(click_dict)
            # Сохранение словаря в файл
            with open(f"{scenario_name}_clicks.json", "w") as file:
                json.dump(click_dict, file, indent=4)
            print(f"Словарь кликов сохранён как {scenario_name}_clicks.json")

def play_clicks(scenario_name, delay, repetitions):
    try:
        with open(scenario_name, "r") as file:
            click_dict = json.load(file)
        if not click_dict:
            print(f"Файл {scenario_name} не содержит кликов.")
            return
        print(f"Загруженные клики: {click_dict}")
        for _ in range(repetitions):
            for click_number in sorted(click_dict.keys(), key=int):
                x, y = click_dict[click_number]
                pyautogui.click(x, y)
                print(f"Клик по координатам ({x}, {y})")
                time.sleep(delay)  # Интервал между кликами
    except FileNotFoundError:
        print(f"Файл не найден: {scenario_name}")
    except json.JSONDecodeError:
        print(f"Ошибка чтения файла: {scenario_name}. Возможно, файл поврежден.")

def main():
    action = input("Вы хотите (з)аписать или (в)оспроизвести сценарий? (з/в): ").strip().lower()
    
    if action not in ['з', 'в']:
        print("Недопустимый ввод. Введите 'з' для записи или 'в' для воспроизведения.")
        return

    print("Вот файлы в текущей директории:")
    files = list_files()

    if action == 'з':
        scenario_name = input("Введите имя сценария: ").strip()
        record_clicks(scenario_name)
    elif action == 'в':
        file_number = int(input("Введите номер файла для воспроизведения: ").strip())
        if 1 <= file_number <= len(files):
            scenario_name = files[file_number - 1]
            delay = float(input("Введите задержку между кликами (в секундах): ").strip())
            repetitions = int(input("Введите количество повторений: ").strip())
            play_clicks(scenario_name, delay, repetitions)
        else:
            print("Недопустимый номер файла.")

if __name__ == "__main__":
    main()
