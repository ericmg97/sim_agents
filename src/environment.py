from random import randint
from agent import Bot
from place import Place
class Environment():
    def __init__(self, N, M, per_obs, per_dirt, cant_childs):
        self.environment = [[Place(i,j) for i in range(M)] for j in range(N)]
        
        self.dirty = 0
        self.ok = True

        self.available = self._check_available_pos()
        
        self._create_corral(N, M, cant_childs)
        
        self.childs = self._create_childs(cant_childs)    
        self.agent = self._create_agent()

        self._fill_env(N, M, per_obs, 3)
        self._fill_env(N, M, per_dirt, 4)

    def _create_corral(self, N, M, cant):
        row = randint(0, N - 1)
        col = randint(0, M - cant - 1)    

        for i in range(cant):
            self.add_object(row, col + i, 5)
            self.available.remove((row, col + i))
  
    def _create_childs(self, cant):
        childs = []
        for _ in range(cant):
            if len(self.available):
                i = randint(0, len(self.available) - 1)
                self.add_object(*self.available[i], 2)
                childs.append(self.available[i])
                self.available.pop(i)
            else:
                self.ok = False
                break
        else:
            return childs

    def _create_agent(self):
        i = randint(0, len(self.available) - 1)
        position = self.available[i]
        
        self.add_object(*position, 1)
        self.available.pop(i)
        
        return Bot(*position)

    def _fill_env(self, N, M, per_obj, obj_type):
        cant_obj = int(N*M*per_obj/100)
        
        if obj_type == 4:
            self.dirty = cant_obj

        for _ in range(cant_obj):
            if len(self.available):
                i = randint(0, len(self.available) - 1)
                self.add_object(*self.available[i], obj_type)
                self.available.pop(i)
            else:
                self.ok = False
                break

    def _check_available_pos(self):
        available = []
        for i, row in enumerate(self.environment):
            for j, obj in enumerate(row):
                if not len(obj.objects):
                    available.append((i, j))

        return available

    def get_place(self, row, col):
        try:
            return self.environment[row][col]
        except:
            return None

    def add_object(self, row, col, obj_type):
        place = self.get_place(row, col)

        if place is None:
            return False
        else:
            self.environment[row][col].add_object(obj_type)
            return True
    
    def natural_change(self):
        pass

    def shuffle(self):
        pass

if __name__ == "__main__":
    a = Environment(5,8,20,10,3)
    print("sad") 