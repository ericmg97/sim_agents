from copy import deepcopy

class Simulation():
    def __init__(self, environment, refresh_time):
        self.environment = environment
        self._original_env = deepcopy(environment)
        self.time = 1
        self.refresh_time = refresh_time
        self.dirty_cant = environment.dirty
    
    def execute(self):
        for t in range(1, 100*self.refresh_time):
            self.time = t
            
            self.environment.move_agent()
            
            self.environment.natural_change()

            if not self.time % self.refresh_time:
                self.environment.shuffle()
        

            self.dirty_cant += self.environment.dirty

            if self.environment.dirty/(self.environment.rows*self.environment.columns) >= 0.6:
                return self.check_results("Despedido")
            elif self.environment.dirty == 0:
                for child in self.environment.childs:
                    if not child.corral:
                        break
                else:
                    return self.check_results("Todo Limpio")
            
        return self.check_results("Tiempo Agotado")

    def reset(self):
        self.environment = deepcopy(self._original_env)
        self.time = 1
        self.dirty_cant = self.environment.dirty

    def check_results(self, reason):
        dirty_places_ave = self.dirty_cant / self.time
        area = self.environment.rows * self.environment.columns
        
        return int(((dirty_places_ave)*100)/(area)), reason