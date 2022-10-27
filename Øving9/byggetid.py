# !/usr/bin/python3
# coding=utf-8


import random


def topological_sort(tasks):
    sorted_tasks = []
    for task in tasks:
        if task not in sorted_tasks:
            topological_sort_helper(task, sorted_tasks)
    return sorted_tasks


def topological_sort_helper(task, sorted_tasks):
    for dep in task.depends_on:
        if dep not in sorted_tasks:
            topological_sort_helper(dep, sorted_tasks)
    sorted_tasks.append(task)


def building_time(tasks):
    sorted_tasks = topological_sort(tasks)
    for task in sorted_tasks:
        task.time = max(
            [dep.time for dep in task.depends_on] + [0]) + task.time
    return max([task.time for task in tasks])


class Task:
    def __init__(self, time, depends_on, i):
        self.time = time
        self.depends_on = depends_on
        self.i = i

    def __str__(self):
        depends_on_str = ", ".join(
            "Task " + str(task.i) for task in self.depends_on
        )
        return "Task {:}: {{time: {:}, depends_on: ".format(
            self.i, self.time
        ) + "[{:}]}}".format(depends_on_str)

    def __repr__(self):
        return str(self)


def test_case_from_list(tasks_arr):
    tasks = [Task(task[0], [], i) for i, task in enumerate(tasks_arr)]
    for i in range(len(tasks_arr)):
        for j in tasks_arr[i][1]:
            tasks[i].depends_on.append(tasks[j])
    random.shuffle(tasks)
    return tasks


tests = [
    ([(4, [])], 4),
    ([(1, []), (4, [2]), (5, [])], 9),
    ([(3, [])], 3),
    ([(2, [1, 2]), (1, [2]), (4, [])], 7),
    ([(4, [])], 4),
    ([(4, [])], 4),
    ([(1, [])], 1),
    ([(1, [1]), (3, [])], 4),
    ([(1, [1]), (3, [2]), (3, [])], 7),
    ([(2, [2, 3]), (3, [3]), (3, [3]), (5, [])], 10),
]

random.seed(123)

failed = False

for test_case, answer in tests:
    student = building_time(test_case_from_list(test_case))
    if student != answer:
        failed = True
        response = "Koden feilet for følgende input: (tasks={:}). ".format(
            str(test_case_from_list(test_case))
        ) + "Din output: {:}. Riktig output: {:}".format(student, answer)
        print(response)
        break

if not failed:
    print("Koden fungerte for alle eksempeltestene.")
