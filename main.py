import random
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

population_size = 100

num_generations = 100

crossover_rate = 0.5

mutation_rate = 0.7

num_days = 5

num_hours = 4


class Teacher:
    def __init__(self, name, discipline):
        self.name = name
        self.discipline = discipline

    def teaches(self, discipline):
        return discipline == self.discipline

    def __str__(self):
        return self.name

class Class:
    def __init__(self, discipline, teacher):
        self.discipline = discipline
        self.teacher = teacher

    def __str__(self):
        return f"{self.discipline} {self.teacher}"


disciplines_count = {
    0: 6,
    1: 4,
    2: 2,
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    7: 1,
    8: 4,
    9: 2,
    10: 1,
    11: 1,
}

disciplines = [
    "Iнформаційні системи",
    "Розробка під мобільні застосунки",
    "Теорія прийняття рішень",
    "Чисельні методи",
    "Математична логіка",
    "Методи паралельних обчислень",
    "Математичний аналіз",
    "Диференціальні рівняння",
    "Англійська",
    "Методи моделювання систем",
    "Теорія ймовірності",
    "Філософія",
]

teachers = [
    Teacher("Teacher 0", 0),
    Teacher("Teacher 1", 1),
    Teacher("Teacher 2", 2),
    Teacher("Teacher 2", 3),
    Teacher("Teacher 3", 4),
    Teacher("Teacher 4", 5),
    Teacher("Teacher 5", 6),
    Teacher("Teacher 5", 7),
    Teacher("Teacher 6", 8),
    Teacher("Teacher 7", 9),
    Teacher("Teacher 8", 9),
    Teacher("Teacher 9", 10),
    Teacher("Teacher 9", 11),
]


def printSchedule(schedule):
    df = pd.DataFrame(data={
        'day': schedule.keys(),
        'lessons': schedule.values()
    })
    print(df)


def generate_random_schedule():
    schedule = {}

    for day in range(num_days):
        for hour in range(num_hours):
            discipline_idx = random.randint(0, len(disciplines) - 1)
            discipline = disciplines[discipline_idx]

            eligible_teachers = list(
                filter(lambda x: x.teaches(discipline_idx), teachers)
            )
            teacher_idx = random.randint(0, len(eligible_teachers) - 1)
            teacher = eligible_teachers[teacher_idx]

            schedule[(day, hour)] = Class(discipline, teacher)

    return schedule

def get_fitness(schedule):
    fitness = 0
    
    schedule_disciplines = [
        schedule[(day, hour)].discipline
        for day in range(num_days)
        for hour in range(num_hours)
    ]
    schedule_teachers = [
        schedule[(day, hour)].teacher
        for day in range(num_days)
        for hour in range(num_hours)
    ]

    fitness += len(set(schedule_disciplines)) + len(set(schedule_teachers))

    # додати 1 якщо дисципліна викладається менше ніж 3 рази за 2 дні
    for day in range(num_days-2):
        for discipline in disciplines:
            day_slice = schedule_disciplines[day*num_hours : (day + 2)*num_hours]
            count = day_slice.count(discipline)
            if count < 3:
                fitness += 1

    # додати 1 якщо вчитель викладає менше ніж 3 рази за 2 дні
    for day in range(num_days-2):
        for teacher in teachers:
            day_slice = schedule_teachers[day*num_hours : (day + 2)*num_hours]
            count = day_slice.count(teacher)
            if count < 3:
                fitness += 1

    # відняти 1 якщо йде 2 дисципліни підряд
    for i in range(0, len(schedule_disciplines) - 1):
        if schedule_disciplines[i] == schedule_disciplines[i + 1]:
            fitness -= 1

    # відняти 1 якщо йде 2 вчителя підряд
    for i in range(0, len(schedule_teachers) - 1):
        if schedule_teachers[i] == schedule_teachers[i + 1]:
            fitness -= 1

    # відняти 1 від кожної дисципліни, якщо вона викладається більшу кількість разів, ніж повинна
    for discipline in disciplines:
        if (
            schedule_disciplines.count(discipline)
            > disciplines_count[disciplines.index(discipline)]
        ):
            fitness -= 1

    # додати одиницю, якщо дисципліна включена в розклад
    for discipline in disciplines:
        if schedule_disciplines.count(discipline) == 1:
            fitness += 1

    return fitness

def crossover(schedule1, schedule2, crossover_rate):
    new_schedule = {}
    for day, hour in schedule1:
        if random.random() < crossover_rate:
            new_schedule[(day, hour)] = schedule1[(day, hour)]
        else:
            new_schedule[(day, hour)] = schedule2[(day, hour)]
    return new_schedule

def mutation(schedule):
    day = random.randint(0, num_days - 1)
    hour = random.randint(0, num_hours - 1)

    discipline_idx = random.randint(0, len(disciplines) - 1)
    discipline = disciplines[discipline_idx]

    eligible_teachers = list(filter(lambda x: x.teaches(discipline_idx), teachers))
    teacher_idx = random.randint(0, len(eligible_teachers) - 1)
    teacher = eligible_teachers[teacher_idx]
    schedule[(day, hour)] = Class(discipline, teacher)



def genetic_algorithm():
    population = [generate_random_schedule() for i in range(population_size)]

    for gen in range(num_generations):
        fitnesses = [get_fitness(schedule) for schedule in population]

        worst_schedule_idx = min (range(len(fitnesses)), key=lambda x: fitnesses[x])
        best_schedule_idx = max(range(len(fitnesses)), key=lambda x: fitnesses[x])
        best_schedule = population[best_schedule_idx]

        print("Generation:", gen, "Best fitness:", fitnesses[best_schedule_idx])
        print("Generation:", gen, "Worst fitness:", fitnesses[worst_schedule_idx])

        new_population = [best_schedule]

        while len(new_population) < population_size:
            parent1_idx = random.randint(0, len(population) - 1)
            parent2_idx = random.randint(0, len(population) - 1)
            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]

            child = crossover(parent1, parent2, crossover_rate)

            if random.random() < mutation_rate:
                mutation(child)

            new_population.append(child)
        population = new_population

    return best_schedule


gen_algo = genetic_algorithm()
printSchedule(gen_algo)

print()
