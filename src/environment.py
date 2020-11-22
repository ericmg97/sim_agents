from random import randint
from agent import Bot
from child import Child
from utils import is_in

class Environment():
    def __init__(self, N, M, per_obs, per_dirt, cant_childs):
        self.environment = [[Place(i, j) for j in range(M)] for i in range(N)]
        
        self.dirty = 0

        self.available = self._check_available_pos()
        
        self._create_corral(N, M, cant_childs)
        
        self.childs = self._create_childs(cant_childs)    
        self.agent = self._create_agent()

        self._fill_env(N, M, per_obs, 3)
        self._fill_env(N, M, per_dirt, 4)

    def __str__(self):
        str_out = ""
        for row in self.environment:
            for place in row:    
                str_out += f"{place.objects} "
            
            str_out += "\n"
        
        return str_out

    def _create_corral(self, N, M, cant):
        row = randint(0, N - 1)
        col = randint(0, M - cant - 1)    

        for i in range(cant):
            self.environment[row][col + i].add_object(5)
            self.available.remove((row, col + i))
  
    def _create_childs(self, cant):
        childs = []
        for _ in range(cant):
            if len(self.available):
                i = randint(0, len(self.available) - 1)
                row = self.available[i][0]
                col = self.available[i][1]
                self.environment[row][col].add_object(2)

                childs.append(Child(row, col))
                self.available.pop(i)
            else:
                break
        else:
            return childs

    def _create_agent(self):
        i = randint(0, len(self.available) - 1)
        position = self.available[i]
        
        self.environment[position[0]][position[1]].add_object(1)
        self.available.pop(i)
        
        return Bot(*position)

    def _fill_env(self, N, M, per_obj, obj_type):
        cant_obj = int(N*M*per_obj/100)
        
        if obj_type == 4:
            self.dirty = cant_obj

        for _ in range(cant_obj):
            if len(self.available):
                i = randint(0, len(self.available) - 1)
                row = self.available[i][0]
                col = self.available[i][1]
                self.environment[row][col].add_object(obj_type)
                self.available.pop(i)
            else:
                break

    def _check_available_pos(self):
        available = []
        for i, row in enumerate(self.environment):
            for j, obj in enumerate(row):
                if not len(obj.objects):
                    available.append((i, j))

        return available

    def natural_change(self):
        for child in self.childs:
            print(self)
            if not child.taked:
                self.environment = child.move(self.environment)

    def shuffle(self):
        pass

class Place():
    def __init__(self, row, col, objs = []):
        self.objects = objs[:]
        self.row = row
        self.column = col
    
    def add_object(self, obj):
        self.objects.append(obj)

    def del_object(self, obj):
        self.objects.remove(obj)

    def clear(self, env):
        self.objects = []

    def move(self, env, new_r, new_c, objs):
        for obj in objs:
            env[new_r][new_c].add_object(obj)
            env[self.row][self.column].del_object(obj)

        return env

if __name__ == "__main__":
    
    a = Environment(5,8,20,10,3)
    a.natural_change()
    print(f"\n{a}")
