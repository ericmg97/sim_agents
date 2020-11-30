from utils import is_in

class Bot():
    def __init__(self, row, col):
        self.row = row
        self.column = col
        self.have_child = False

    def move(self, env, childs, agent_type = "Smart"):
        if agent_type == "Brute":
            return self._move_brute(env, childs)
        elif agent_type == "Smart":
            return self._move_smart(env, childs)

    def _move_brute(self, env, childs):
        place = env[self.row][self.column]

        if 4 in place.objects:
            place.del_object(4)
            return env, True
        
        elif 5 in place.objects and self.have_child:
            self.have_child = False

            for i in range(len(childs)):
                if childs[i].row == self.row and childs[i].column == self.column:
                    childs[i].taked = False
                    childs[i].corral = True
                    break
                
            return env, False
        
        if not self.have_child:
            path = self._path_to_closest_object(env, 4)
            
            if path is None:
                path = self._path_to_closest_object(env, 2)
            
                if path is None:
                    return env, False
            
            next_move = path[1]

            self.row = next_move[0]
            self.column = next_move[1]
            
            if 2 in env[self.row][self.column].objects:
                self.have_child = True

                for i in range(len(childs)):
                    if childs[i].row == self.row and childs[i].column == self.column:
                        childs[i].taked = True
                        break

            return place.move(env, self.row, self.column, [1]), False

        else:
            path = self._path_to_closest_object(env, 4)

            if path is None:
                path = self._path_to_closest_object(env, 5)
            
                if path is None:
                    return env, False

            first_move = path[1]
            if 4 in env[first_move[0]][first_move[1]].objects or 5 in env[first_move[0]][first_move[1]].objects:
                next_move = path[1]
            else:
                next_move = path[2]

            for i in range(len(childs)):
                if childs[i].row == self.row and childs[i].column == self.column:
                    childs[i].row = next_move[0]
                    childs[i].column = next_move[1]
                    break

            self.row = next_move[0]
            self.column = next_move[1]

            return place.move(env, self.row, self.column, place.objects[:]), False

    def _move_smart(self, env, childs):
        place = env[self.row][self.column]

        if 4 in place.objects:
            place.del_object(4)
            return env, True

        elif 5 in place.objects and self.have_child:
            self.have_child = False

            for i in range(len(childs)):
                if childs[i].row == self.row and childs[i].column == self.column:
                    childs[i].taked = False
                    childs[i].corral = True
                    break
                
            return env, False

        #busca un niño si no tiene ninguno cargado
        if not self.have_child:
            path = self._path_to_closest_object(env, 2)
            
            #todos los niños estan en el corral, empieza a buscar basura
            if path is None:
                path = self._path_to_closest_object(env, 4)

                if path is None:
                    return env, False
                
                next_move = path[1]

                self.row = next_move[0]
                self.column = next_move[1]

                return place.move(env, self.row, self.column, [1]), False
            
            #quedan niños sueltos por el ambiente
            else:
                next_move = path[1]

                self.row = next_move[0]
                self.column = next_move[1]
                
                if 2 in env[self.row][self.column].objects:
                    self.have_child = True

                    for i in range(len(childs)):
                        if childs[i].row == self.row and childs[i].column == self.column:
                            childs[i].taked = True
                            break

                return place.move(env, self.row, self.column, [1]), False
     
        #busca un corral vacio para dejar el niño q carga
        else:
            path = self._path_to_closest_object(env, 5)
            
            if path is None:
                return env, False
            
            first_move = path[1]
            if 4 in env[first_move[0]][first_move[1]].objects or 5 in env[first_move[0]][first_move[1]].objects:
                next_move = path[1]
            else:
                next_move = path[2]

            for i in range(len(childs)):
                if childs[i].row == self.row and childs[i].column == self.column:
                    childs[i].row = next_move[0]
                    childs[i].column = next_move[1]
                    break

            self.row = next_move[0]
            self.column = next_move[1]
            
            return place.move(env, self.row, self.column, place.objects[:]), False

    def _path_to_closest_object(self, env, obj):      
        if self.have_child:
            checked = [[True if 3 in env[i][j].objects or 2 in env[i][j].objects else False for j in range(len(env[0]))] for i in range(len(env))]
        else:
            checked = [[True if 3 in env[i][j].objects else False for j in range(len(env[0]))] for i in range(len(env))]
        
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)] 
        cola = [[(self.row, self.column)]]

        while cola:
            path = cola.pop(0)          
            row, col = path[-1]

            if len(env[row][col].objects) and env[row][col].objects[0] == obj:
                return path
            
            for direct in moves:          
                new_row = row + direct[0]
                new_col = col + direct[1]

                if is_in(new_row, new_col, checked) and not checked[new_row][new_col]:  
                    new_path = list(path)
                    new_path.append((new_row, new_col))
                    cola.append(new_path)

            checked[row][col] = True