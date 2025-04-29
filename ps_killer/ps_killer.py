import os
import time
import signal
import subprocess

import redis


_redis = redis.Redis(db=0)

def find_and_kill_alarms():
    try:
        # Получаем все процессы через ps
        output = subprocess.check_output(["ps", "aux"], text=True)
        
        # Проходимся по строкам
        for line in output.splitlines():
            if "/school_bell/alarm.py" in line:
                parts = line.split()
                pid = int(parts[1])  # PID всегда во втором столбце (после USER)

                print(f"❗ Найден процесс с --alarm, убиваем PID {pid}")
                os.kill(pid, signal.SIGKILL)  # Жёсткое убийство процесса
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    while True:
        fire = int(_redis.get("fire").decode())
        alarm = int(_redis.get("alarm").decode())
        test = int(_redis.get("test").decode())
        if not fire and not alarm and not test:
            find_and_kill_alarms()
            time.sleep(1)

if __name__ == "__main__":
    main()
