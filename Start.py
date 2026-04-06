import time
from telemetrix import telemetrix

PORT = '/dev/cu.usbserial-140'
PCA_ADDR = 0x40


def set_servo(board, channel, value):
    """
    Универсальная функция управления
    :param channel: 0, 1 (180 градусов) или 2, 3 (360 градусов)
    :param value: угол для 180° или скорость для 360°
    """
    value = max(0, min(180, value))
    # Масштабируем 0-180 градусов в 150-600 тиков ШИМ
    pulse = int((value / 180) * (600 - 150) + 150)

    off_l = pulse & 0xFF
    off_h = pulse >> 8
    reg = 0x06 + (channel * 4)
    board.i2c_write(PCA_ADDR, [reg, 0, 0, off_l, off_h])

def hard_stop(board, channel):
    """Полностью отключает генерацию ШИМ на канале"""
    # Регистр OFF_H для конкретного канала
    reg_off_h = 0x06 + (channel * 4) + 3
    # Запись 0x10 (16 в десятичной) в этот регистр принудительно выключает канал
    board.i2c_write(PCA_ADDR, [reg_off_h, 0x10])


def run_quad_servos():
    board = telemetrix.Telemetrix(com_port=PORT, arduino_wait=4)

    try:
        print("Инициализация системы...")
        board.set_pin_mode_i2c()

        # Настройка PCA9685 (стандартный блок инициализации)
        board.i2c_write(PCA_ADDR, [0x00, 0x01])
        time.sleep(0.1)
        board.i2c_write(PCA_ADDR, [0x00, 0x11])
        board.i2c_write(PCA_ADDR, [0xFE, 0x79])
        board.i2c_write(PCA_ADDR, [0x00, 0x01])
        time.sleep(0.1)
        board.i2c_write(PCA_ADDR, [0x00, 0xA1])

        print("--- Выполнение движений ---")

        # 1. Выставляем 180-градусные серво в начальные позиции
        # print("Каналы 0 и 1: Установка углов")
        # set_servo(board, 0, 0)  # Первый на 0 градусов
        #set_servo(board, 1, 180)  # Второй на 180 градусов

        # 2. Запускаем вращение 360-градусных серво
        print("Каналы 2 и 3: Запуск вращения")
        #set_servo(board, 2, 70)  # Медленно в одну сторону
        # set_servo(board, 3, 110)  # Медленно в другую сторону
        # 3: 60 центр 40 и 80
        # 2: 80 и 46

        time.sleep(1)  # Ждем 3 секунды выполнения


        set_servo(board, 3, 40)
        time.sleep(14)
        hard_stop(board, 3)

        # range(старт, стоп, шаг)
        for angle in range(90, 60, -1):
            set_servo(board, 0, angle)
            time.sleep(0.05)

        time.sleep(5)

        for angle in range(60, 90, +1):
            set_servo(board, 0, angle)
            time.sleep(0.05)

        time.sleep(2)

        for angle in range(90, 120, +1):
            set_servo(board, 0, angle)
            time.sleep(0.05)

        time.sleep(5)

        for angle in range(120, 90, -1):
            set_servo(board, 0, angle)
            time.sleep(0.05)

        time.sleep(2)

        for angle in range(90, 60, -1):
            set_servo(board, 1, angle)
            time.sleep(0.05)

        time.sleep(5)

        for angle in range(60, 90, +1):
            set_servo(board, 1, angle)
            time.sleep(0.05)

        time.sleep(2)

        for angle in range(90, 120, +1):
            set_servo(board, 1, angle)
            time.sleep(0.05)

        time.sleep(5)

        for angle in range(120, 90, -1):
            set_servo(board, 1, angle)
            time.sleep(0.05)

        time.sleep(2)

        set_servo(board, 3, 40)
        time.sleep(12)
        hard_stop(board, 3)

        set_servo(board, 2, 46)
        time.sleep(10)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(5)
        hard_stop(board, 3)

        set_servo(board, 2, 80)
        time.sleep(23)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(5)
        hard_stop(board, 3)

        set_servo(board, 2, 46)
        time.sleep(21)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(5)
        hard_stop(board, 3)

        set_servo(board, 2, 80)
        time.sleep(23)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(5)
        hard_stop(board, 3)

        set_servo(board, 2, 46)
        time.sleep(22)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(5)
        hard_stop(board, 3)

        set_servo(board, 2, 80)
        time.sleep(22)
        hard_stop(board, 2)

        set_servo(board, 3, 80)
        time.sleep(6)
        hard_stop(board, 3)

        set_servo(board, 2, 46)
        time.sleep(10)
        hard_stop(board, 2)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        board.shutdown()


if __name__ == "__main__":
    run_quad_servos()
