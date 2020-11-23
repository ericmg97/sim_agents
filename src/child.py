from random import randint
from utils import is_in

class Child():
    def __init__(self, row, col):
        self.row = row
        self.column = col
        self.taked = False

    def move(self, env):
        place = env[self.row][self.column]
        movs = self._check_dir(env)
        
        if not len(movs):
            return env, False

        i = randint(0, len(movs) - 1)
        new_row = self.row + movs[i][0]
        new_col = self.column + movs[i][1]
        print( f"\n{self.row} {self.column} -----> {new_row} {new_col}\n")
        new_place = env[new_row][new_col]

        if len(new_place.objects):
            j = 2
            while True:
                obs_place = env[self.row + movs[i][0]*j][self.column + movs[i][1]*j]
                if not len(obs_place.objects):
                    env = new_place.move(env, self.row + movs[i][0]*j, self.column + movs[i][1]*j, [3])
                    break
                j += 1
        
        move_env = place.move(env, new_row, new_col, [2])
        new_env, can_put = self._put_trash(move_env, self.row, self.column)
        self.row = new_row
        self.column = new_col
        return new_env, can_put


    def _check_dir(self,env):
        movs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for mov in movs[:]:
            if is_in(self.row + mov[0],self.column + mov[1], env):
                place = env[self.row + mov[0]][self.column + mov[1]]

                if len(place.objects):                    
                    if place.objects[0] == 3:
                        j = 2
                        while True:
                            if is_in(self.row + mov[0]*j, self.column + mov[1]*j, env):
                                objects = env[self.row + mov[0]*j][self.column + mov[1]*j].objects
                                if len(objects) and objects[0] == 3:
                                    j += 1
                                    continue
                                elif not len(objects):
                                    break
                            
                            movs.remove(mov)
                            break        
                    else:
                        movs.remove(mov)
            else:
                movs.remove(mov)
       
        return movs


    def _put_trash(self, env, row, column):
        movs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (0, 0)]

        for mov in movs[:]:
            if is_in(row + mov[0], column + mov[1], env):
                place = env[row + mov[0]][column + mov[1]]

                if len(place.objects):                    
                    movs.remove(mov)

            else:
                movs.remove(mov)
        
        if not len(movs):
            return env, False

        i = randint(0, len(movs) - 1)
        dirt_mov = movs[i]
        env[row + dirt_mov[0]][column + dirt_mov[1]].add_object(4)
        print(f"Trash -> {row + dirt_mov[0]}, {column + dirt_mov[1]}")
        return env, True