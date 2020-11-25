from utils import is_in

class Bot():
    def __init__(self, row, col, agent_type):
        self.row = row
        self.column = col
        self.agent_type = agent_type

    def move(self, env):
        if self.agent_type == "Brute":
            return self._move_brute(env)
        elif self.agent_type == "Smart":
            return self._move_smart(env)

    def _move_brute(self, env):
        place = env[self.row][self.column]

        if 4 in place.objects:
            place.del_object(4)
            return env
        
        path_to_closest = self._check_closest_object(4, env, 4)
        
        if path_to_closest is None:
            return env
        else:
            next_move = path_to_closest[1]

            self.row = next_move[0]
            self.column = next_move[1]
            
            return place.move(env,self.row, self.column, [1])

    def _move_smart(self, env):
        pass

    def _check_closest_object(self, moves, env, obj):
        if moves == 8:
            movs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (0, 0)]
        elif moves == 4:
            movs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        return self._path_to_closest(movs, env, obj)

    def _path_to_closest(self, moves, env, obj):   
        checked = [[True if 3 in env[i][j].objects else False for j in range(len(env[0]))] for i in range(len(env))]
        cola = [[(self.row, self.column)]]

        while cola:
            path = cola.pop(0)          
            row, col = path[-1]

            if obj in env[row][col].objects:
                return path
            
            for direct in moves:          
                new_row = row + direct[0]
                new_col = col + direct[1]

                if is_in(new_row, new_col, checked) and not checked[new_row][new_col]:  
                    new_path = list(path)
                    new_path.append((new_row, new_col))
                    cola.append(new_path)

            checked[row][col] = True