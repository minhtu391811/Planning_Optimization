else:
            #     pheromones[(cls, sub, start, teacher)] -= pheromones[(cls, sub, start, teacher)] * float(len(conflicting_idxs) / len(schedule))