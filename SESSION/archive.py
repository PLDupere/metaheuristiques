import numpy as np


class ArchivePareto:
    def __init__(self, max_size=100):
        self.solutions = []  # Positions des centres
        self.objectives = []  # [J_IFCMS, J_edge]
        self.max_size = max_size


    def is_dominated(self, obj_new, obj_archive):
        better_or_equal = all(obj_archive[i] <= obj_new[i] for i in range(len(obj_new))) # Equation (III.1)
        strictly_better = any(obj_archive[i] < obj_new[i] for i in range(len(obj_new)))  # Equation (III.2)
        return better_or_equal and strictly_better


    def update(self, solution, objectives):
        # For safety
        objectives = [float(obj) for obj in objectives]
        for archived_obj in self.objectives:
            if self.is_dominated(objectives, archived_obj):
                return

        to_remove = []
        for i, archived_obj in enumerate(self.objectives):
            if self.is_dominated(archived_obj, objectives):
                to_remove.append(i)

        for i in sorted(to_remove, reverse=True):
            self.solutions.pop(i)
            self.objectives.pop(i)

        self.solutions.append(solution.copy())
        self.objectives.append(objectives)

        if len(self.solutions) > self.max_size:
            self._truncate_archive()


    def _truncate_archive(self):
        if len(self.solutions) <= self.max_size:
            return
        indices_to_keep = self._select_diverse_solutions(self.max_size)
        self.solutions = [self.solutions[i] for i in indices_to_keep]
        self.objectives = [self.objectives[i] for i in indices_to_keep]


    def _select_diverse_solutions(self, target_size):
        if len(self.objectives) == 0:
            return []
        
        obj_array = np.array(self.objectives, dtype=float)
        
        obj_min = obj_array.min(axis=0)
        obj_max = obj_array.max(axis=0)
        obj_normalized = (obj_array - obj_min) / (obj_max - obj_min + 1e-10)
        
        selected = [0]
        
        while len(selected) < target_size and len(selected) < len(self.objectives):
            # Trouve la solution la plus distante des solutions sélectionnées
            max_min_dist = -np.inf
            best_idx = -1
            for i in range(len(self.objectives)):
                if i in selected:
                    continue
                
                min_dist = np.min([
                    np.linalg.norm(obj_normalized[i] - obj_normalized[j])
                    for j in selected
                ])
                if min_dist > max_min_dist:
                    max_min_dist = min_dist
                    best_idx = i

            if best_idx >= 0:
                selected.append(best_idx)
            else:
                break

        return selected


    def select_russian_roulette(self):
        if len(self.solutions) == 0:
            return None
        
        if len(self.solutions) == 1:
            return self.solutions[0].copy()
        
        objectives_array = np.array(self.objectives, dtype=float)
        combined_objectives = np.sum(objectives_array, axis=1)
        max_obj = np.max(combined_objectives)
        weights = (max_obj - combined_objectives + 1e-10)
        weights = weights / np.sum(weights)
        idx = np.random.choice(len(self.solutions), p=weights)
        return self.solutions[idx].copy()


    def get_best_solution(self):
        if len(self.solutions) == 0:
            return None
        return self.solutions[0].copy()


    def size(self):
        return len(self.solutions)


    def get_all_solutions(self):
        return self.solutions.copy(), self.objectives.copy()
