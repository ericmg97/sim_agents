def is_in(row, col, environment):
    return True if row >= 0 and col >= 0 and row < len(environment) and col < len(environment[0]) else False