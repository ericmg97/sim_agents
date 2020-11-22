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
    
    
        