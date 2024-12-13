import numpy as np
from collections import defaultdict

def crossover(parent1, parent2):
    child1 = parent1.copy()
    child2 = parent2.copy()

    for i in parent1.keys():
        if np.random.rand() < 0.5:
            child1[i], child2[i] = child2[i], child1[i]

    return child1, child2

def mutation(child, subjects_per_class, teachers_per_subject, d):
    class_id = np.random.randint(1, len(child) + 1)
    subject_index = np.random.randint(len(child[class_id]))
    subject_id = child[class_id][subject_index][0]

    session = np.random.randint(0, 10)
    start_period = session * 6 + np.random.randint(1, 8 - d[subject_id])
    teacher = np.random.choice(teachers_per_subject[subject_id])

    child[class_id][subject_index] = [subject_id, start_period, teacher]
    return child

def fitness(individual, t, d, subjects_per_class, teachers_per_subject):
    score = 0
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)

    for idx, class_schedule_list in individual.items():
        for subject in class_schedule_list:
            subject_id, start_period, teacher = subject
            duration = d[subject_id]

            # Kiểm tra chồng lấn thời khóa biểu trong cùng lớp
            if any(start_period <= s < start_period + duration or s <= start_period < s + duration for (sub, s) in assigned_classes[idx]):
                continue

            # Kiểm tra chồng lấn thời khóa biểu trong cùng giáo viên
            if any(start_period <= s < start_period + duration or s <= start_period < s + duration for (sub, s) in assigned_teachers[teacher]):
                continue

            # Nếu không có chồng lấn, cập nhật lịch cho lớp và giáo viên
            assigned_classes[idx].append((subject_id, start_period))
            assigned_teachers[teacher].append((subject_id, start_period))
            score += 1

    return score

def overlap(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    return not (end1 < start2 or end2 < start1)
