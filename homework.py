from dataclasses import dataclass
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:.3f} ч.;"
                f" Дистанция: {self.distance:.3f} км;"
                f" Ср. скорость: {self.speed:.3f} км/ч;"
                f" Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите run в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUN_1 = 18
    COEFF_CALORIE_RUN_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_RUN_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2)
                * self.weight
                / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_WALK_1 = 0.035
    COEFF_CALORIE_WALK_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.COEFF_CALORIE_WALK_1
                * self.weight
                + ((self.get_mean_speed()
                    * self.get_mean_speed())
                    // self.height)
                * self.COEFF_CALORIE_WALK_2
                * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_CALORIE_SWIM_1 = 1.1
    COEFF_CALORIE_SWIM_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_SWIM_1)
                * self.COEFF_CALORIE_SWIM_2
                * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_code: Dict[str, str] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type in train_code:
        return train_code.get(workout_type)(*data)

    raise ValueError('Отсутствует тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
