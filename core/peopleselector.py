"""Выбор, кого из нескольких обнаруженных людей наводить."""


class PeopleSelector:
    def __init__(self):
        self.selected_idx = 0
        self._count = 0

    def update(self, poses, ref_landmark_index=0):
        """poses — список поз (по одной на человека).
        Сортирует людей слева направо для стабильной нумерации между
        кадрами и подгоняет selected_idx под новое число людей.
        """
        if not poses:
            self._count = 0
            return []

        poses = sorted(poses, key=lambda lm: lm[ref_landmark_index].x)
        self._count = len(poses)
        self.selected_idx = min(self.selected_idx, self._count - 1)
        return poses

    def next_person(self):
        if self._count:
            self.selected_idx = (self.selected_idx + 1) % self._count

    def prev_person(self):
        if self._count:
            self.selected_idx = (self.selected_idx - 1) % self._count

    def selected(self, poses):
        if not poses:
            return None
        return poses[self.selected_idx]