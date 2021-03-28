import numpy as np
from matplotlib import pyplot as plt
from random import uniform, random
from typing import Tuple

time_in_hours = 1000
num_of_people = 100
R = 5.0
MAX_DIST = 0.07
AREA_SIZE_X = 10
AREA_SIZE_Y = 10
infection_time = 24 * 5
quarantine_time = 24 * 10

states_list = ["healthy", "infected", "sick", "recovered", "death"]
state_color = {"healthy":"green", "infected":"red", "sick":"purple", "recovered":"blue", "death":"black"}


class Person:
    def __init__(self):
        self.x_pos = uniform(0.0, float(AREA_SIZE_X))
        self.y_pos = uniform(0.0, float(AREA_SIZE_Y))
        self.state = "healthy"
        self.time_from_infection = 0
        self.time_for_quarantine = 0
        # self.has_mask = True if random() < 0.5 else False

    def move(self):
        alfa = uniform(0.0, 2 * np.pi)
        if self.state in ['sick', 'death']:
            return
        else:
            self.x_pos = (self.x_pos + np.cos(alfa) * R) % AREA_SIZE_X
            self.y_pos = (self.y_pos + np.sin(alfa) * R) % AREA_SIZE_Y

    def get_position(self) -> Tuple[int, int]:
        return self.x_pos, self.y_pos

    def get_state(self) -> str:
        return self.state


def is_distance_close_enough(sick_person, healty_person):
    distance = np.sqrt(
        (sick_person.x_pos - healty_person.x_pos)**2 +
        (sick_person.y_pos - healty_person.y_pos)**2
    )
    return distance < MAX_DIST


def update_person_state_based_on_distance(people):
    for p1 in people:
        if p1.state == 'infected': #p1.state == 'sick' or
            for p2 in people:
                if p2.state == 'healthy' and is_distance_close_enough(p1, p2):
                    # if p1.has_mask and p2.has_mask:
                    #     p2.state = 'infected' if random() < 0.2 else 'healthy'
                    # elif p1.has_mask or p2.has_mask:
                    #     p2.state = 'infected' if random() < 0.5 else 'healthy'
                    # else:
                        p2.state = 'infected'


def update_person_state_based_on_time(people):
    for p in people:
        if p.state == 'infected':
            p.time_from_infection += 1
            if p.time_from_infection == infection_time:
                p.state = 'sick'
        if p.state == 'sick':
            p.time_for_quarantine += 1
            if p.time_for_quarantine == quarantine_time:
                p.state = 'recovered' if random() > 0.05 else "death"


def update_historical_data(historical_data, population):
    for state in states_list:
        historical_data[state].append(len([p.state for p in population if p.state == state]))


def plot_person(person):
    plt.subplot(2, 1, 1)
    plt.plot(person.x_pos, person.y_pos, 'o', color=state_color[person.get_state()])


def plot_historical_data(time_arr, historical_data):
    plt.subplot(2, 1, 2)

    title = "Pandemy after " + str(len(time_arr)) + " hours \n " \
            " healthy: " + str(historical_data['healthy'][-1]) + \
            " infected: " + str(historical_data['infected'][-1]) +\
            " sick: " + str(historical_data['sick'][-1]) +\
            " recovered: " + str(historical_data['recovered'][-1]) +\
            " death: " + str(historical_data['death'][-1])

    plt.title(title, y=2.2)
    for state in states_list:
        plt.plot(time_arr, historical_data[state], label=state, color=state_color[state])

    plt.legend(bbox_to_anchor=(0.25, 0.85), loc='upper right', borderaxespad=0.)


def simulate_pandemy():
    population = [Person() for _ in range(num_of_people)]
    population[0].state = "infected"
    # population[0].has_mask = False

    historical_data = {state: [] for state in states_list}
    time_arr = []

    for t in range(time_in_hours):
        plt.clf()
        for p in population:
            p.move()
            plot_person(p)

        update_person_state_based_on_distance(population)
        update_person_state_based_on_time(population)
        update_historical_data(historical_data, population)
        time_arr.append(t)

        if t % 72 == 1 :
            plot_historical_data(time_arr, historical_data)
            plt.show()


simulate_pandemy()

