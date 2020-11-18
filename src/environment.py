from random import randint
from agent import Bot


class Environment():
    def __init__(self, N, M, per_obs, per_dirt, cant_childs):
        self.environment = [[0]*M for _ in range(N)]
        self._available = self._check_available_pos()
        self.ok = True
        
        self.childs = cant_childs
        self._create_corral(N, M)

        self.agent = self._create_agent()
             
        self._fill_env(cant_childs, 2)
        self._fill_env(int(N*M*per_obs/100), 3)
        self._fill_env(int(N*M*per_dirt/100), 4)

    def _create_corral(self, N, M):
        if N >= self.childs and M > 0:
            for i in range(self.childs):
                self.add_object(0, i, 5)
                self._available.remove((0, i))

        elif M >= self.childs and N > 0:
            for i in range(self.childs):
                self.add_object(i, 0, 5)
                self._available.remove((i, 0))

        else:
            return False

    def _create_agent(self):
        i = randint(0, len(self._available))
        position = self._available[i]
        
        self.add_object(*position, 1)
        self._available.pop(i)
        
        return Bot(*position)

    def _fill_env(self, cant_obj, obj_type):
        for _ in range(cant_obj):
            if len(self._available):
                i = randint(0, len(self._available))
                self.add_object(*self._available[i], obj_type)
                self._available.pop(i)
            else:
                self.ok = False
                break

    def _check_available_pos(self):
        available = []
        for i, row in enumerate(self.environment):
            for j, obj in enumerate(row):
                if not obj:
                    available.append((i, j))

        return available

    def get_object(self, row, col):
        try:
            return self.environment[row][col]
        except:
            return None

    def add_object(self, row, col, obj_type):
        place = self.get_object(row, col)

        if place is None:
            return False
        else:
            self.environment[row][col] = obj_type
            return True

    def move_object(self, row, col, dir):
        pass