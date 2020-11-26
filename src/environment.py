from random import randint
from agent import Bot
from child import Child
from utils import is_in

class Environment():
    def __init__(self, N, M, per_obs, per_dirt, cant_childs, agent_type):
        self.environment = [[Place(i, j) for j in range(M)] for i in range(N)]
        
        self.dirty = 0
        self.rows = N
        self.columns = M
        
        self._create_corral(cant_childs)
        
        self.childs = self._create_childs(cant_childs)
        self.childs_ok = [False for i in range(cant_childs)]
        self.agent = self._create_agent(agent_type)

        self._fill_env(N, M, per_obs, 3)
        self._fill_env(N, M, per_dirt, 4)

    def __str__(self):
        str_out = ""
        for row in self.environment:
            for place in row:    
                str_out += f"{place.objects} "
            
            str_out += "\n"
        
        return str_out

    def _create_corral(self, cant):
        row = randint(0, self.rows - 1)
        col = randint(0, self.columns - cant - 1)    

        for i in range(cant):
            self.environment[row][col + i].add_object(5)
  
    def _create_childs(self, cant):
        available = self._check_available_pos()
        childs = []
        for _ in range(cant):
            if len(available):
                i = randint(0, len(available) - 1)
                row = available[i][0]
                col = available[i][1]
                self.environment[row][col].add_object(2)
                
                childs.append(Child(row, col))
                available.pop(i)
            else:
                break
        else:
            return childs

    def _create_agent(self, agent_type):
        available = self._check_available_pos()
        i = randint(0, len(available) - 1)
        position = available[i]
        
        self.environment[position[0]][position[1]].add_object(1)
        
        return Bot(*position, agent_type)

    def _fill_env(self, N, M, per_obj, obj_type):
        cant_obj = int(N*M*per_obj/100)
        available = self._check_available_pos()

        if obj_type == 4:
            self.dirty = cant_obj

        for _ in range(cant_obj):
            if len(available):
                i = randint(0, len(available) - 1)
                row = available[i][0]
                col = available[i][1]
                self.environment[row][col].add_object(obj_type)
                available.pop(i)
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
            if not child.taked and not child.corral:
                self.environment, put_trash = child.move(self.environment)
                if put_trash:
                    self.dirty += 1

    def shuffle(self):
        row_corral = randint(0, self.rows - 1)
        col_corral = randint(0, self.columns - len(self.childs) - 1)
        put_corral = 0

        available = self._check_available_pos()
        ok = [[False for j in range(self.columns)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                place = self.environment[i][j]
                if len(place.objects) and not ok[i][j]:
                    if 5 not in place.objects and len(available):
                        k = randint(0, len(available) - 1)
                        swap_place = available[k]
                        available.pop(k)
                        available.append((i, j))
                        ok[swap_place[0]][swap_place[1]] = True
                        
                        if 1 in place.objects:
                            self.agent.row = swap_place[0]
                            self.agent.column = swap_place[1]
                        if 2 in place.objects:
                            for c in range(len(self.childs)):
                                if self.childs[c].row == i and self.childs[c].column == j:
                                    self.childs[c].row = swap_place[0]
                                    self.childs[c].column = swap_place[1]
                                    break

                        self.environment = self.environment[i][j].swap(self.environment, swap_place[0], swap_place[1])
                        
                    elif 5 in place.objects:
                        if 5 in self.environment[row_corral][col_corral + put_corral].objects:
                            put_corral += 1
                            j -= 1
                            ok[row_corral][col_corral + put_corral] = True
                            continue
                        
                        ok[row_corral][col_corral + put_corral] = True
                        
                        if 1 in place.objects:
                            self.agent.row = row_corral
                            self.agent.column = col_corral + put_corral
                        if 2 in place.objects:
                            for c in range(len(self.childs)):
                                if self.childs[c].row == i and self.childs[c].column == j:
                                    self.childs[c].row = row_corral
                                    self.childs[c].column = col_corral + put_corral
                                    break

                        if 1 in self.environment[row_corral][col_corral + put_corral].objects:
                            self.agent.row = i
                            self.agent.column = j
                        if 2 in self.environment[row_corral][col_corral + put_corral].objects:
                            for c in range(len(self.childs)):
                                if self.childs[c].row == row_corral and self.childs[c].column == col_corral + put_corral:
                                    self.childs[c].row = i
                                    self.childs[c].column = j
                                    break

                        self.environment = self.environment[i][j].swap(self.environment, row_corral, col_corral + put_corral)

                        if (row_corral, col_corral + put_corral) in available:
                            available.remove((row_corral, col_corral + put_corral))

                        put_corral += 1 

    def move_agent(self):
        self.environment, del_trash = self.agent.move(self.environment, self.childs)
        if del_trash:
            self.dirty -= 1
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
    
    def replace(self, env, new_r, new_c):
        env[new_r][new_c] = Place(new_r, new_c)
        return self.move(env, new_r, new_c, self.objects[:])

    def swap(self, env, new_r, new_c):
        temp_objs = env[new_r][new_c].objects
        temp_env = self.replace(env, new_r, new_c)
        
        for obj in temp_objs:
            self.add_object(obj)

        return temp_env