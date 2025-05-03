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
        fire_bin = _redis.get("fire")
        alarm_bin = _redis.get("alarm")
        test_bin = _redis.get("test")

        fire = int(fire_bin) if fire_bin else None
        alarm = int(alarm_bin) if alarm_bin else None
        test = int(test_bin) if test_bin else None
        if not fire and not alarm and not test:
            find_and_kill_alarms()
            time.sleep(1)

if __name__ == "__main__":
    main()
