from i3ipc import Connection
import sys
import subprocess

i3 = Connection()

# Функция для выполнения команд в командной строке и получения вывода
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode("utf-8")

# Проверяем, что передано достаточно аргументов
if len(sys.argv) < 2:
    print("Background setup command required.")
    sys.exit(1)

# Получаем аргумент, переданный при запуске скрипта
background_command = sys.argv[1]

# Получаем вывод xrandr
xrandr_output = run_command("xrandr")

# Разделяем вывод на строки
xrandr_lines = xrandr_output.splitlines()

# Переменные для хранения информации о подключенных мониторах
connected_monitors = []

# Парсим вывод xrandr, ищем строки, содержащие информацию о подключенных мониторах
for line in xrandr_lines:
    if " connected " in line:
        monitor_info = line.split()
        monitor_name = monitor_info[0]
        connected_monitors.append(monitor_name)

# Задаём конфигурацию мониторов в зависимость от их подключения
monitor_setup = ""
if 'eDP-1' in connected_monitors and not 'HDMI-1' in connected_monitors:
    monitor_setup = "xrandr --output eDP-1 --primary --auto --pos 0x0 --output HDMI-1 --auto --pos 1920x0"
elif 'HDMI-1' in connected_monitors and 'eDP-1' in connected_monitors:
    monitor_setup = "xrandr --output HDMI-1 --primary --mode 3440x1440 --pos 0x0 --output eDP-1 --auto --pos 3440x180"
    i3.command("workspace number 1")
    i3.command("move workspace to output HDMI-1")
    i3.command("workspace number 3")
    i3.command("workspace number 10")
    i3.command("workspace number 1")
run_command(monitor_setup)
run_command(background_command)
