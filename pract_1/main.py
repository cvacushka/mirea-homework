import json
import sys
from commands import CommandDispatcher


class ShellEmulator:
    def __init__(self, config_path):
        # Загрузка конфигурации из файла
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.vfs_path = config['vfs_path']#путь к вирт файл системе
        self.hostname = config['hostname']# наш хост
        self.username = config['username']#наш пользователь
        self.dispatcher = CommandDispatcher(self.vfs_path) #создаем экземпляр класса для уп команд

    def execute_command(self, command):
        """Выполнение команды"""
        result = self.dispatcher.execute(command)
        return result

    def start_cli(self):
        """Запуск CLI интерфейса для ввода команд"""
        print(f"Welcome to {self.hostname} shell!")#шлет привет
        
        while True:
            try:
                # Показать приглашение командной строки
                command = input(f"{self.username}@{self.hostname}:~$ ").strip()#Ждем команду
            
                # Выполнение команды
                cmd_res = self.execute_command(command)
                

                if cmd_res == "exit":
                    print("Exiting shell...")
                    sys.exit(0)
                else:
                    print(cmd_res)
                    
            except (EOFError, KeyboardInterrupt):#позерство
                print("\nExiting shell...")
                break


# Запуск эмулятора
if __name__ == "__main__":#проверяем что строка содержит путь к файду конфиг
    if len(sys.argv) < 2:
        print("Usage: shell_emulator.py <path_to_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    emulator = ShellEmulator(config_file)#экземплр с указ файлом конфиг
    emulator.start_cli()#запуск
