class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(self):
        pass

    def get_message(self) -> str:
        return (f" Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:.3f} ч.;"
                f" Дистанция: {self.distance:.3f} км;"
                f" Ср. скорость: {self.speed:.3f} км/ч;"
                f" Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(type(self).__name__,
                                self.duration,
                                distance,
                                mean_speed,
                                calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_run_1 = 18
        coeff_calorie_run_2 = 20
        h_in_min = 60
        return ((coeff_calorie_run_1 * self.get_mean_speed()
                 - coeff_calorie_run_2) * self.weight
                 / self.M_IN_KM * (self.duration * h_in_min))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        coeff_calorie_walk_1 = 0.035
        coeff_calorie_walk_2 = 0.029
        h_in_min = 60
        return ((coeff_calorie_walk_1
                 * self.weight + ((self.get_mean_speed()
                 * self.get_mean_speed()) // self.height)
                 * coeff_calorie_walk_2 * self.weight)
                 * (self.duration * h_in_min))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

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
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return ((self.get_mean_speed() + coeff_calorie_1)
                 * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TrainCode = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type in TrainCode:
        return TrainCode.get(workout_type)(*data)
    else:
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