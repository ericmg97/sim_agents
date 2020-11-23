from random import randint
from environment import Environment
from simulation import Simulation

def create_environment():
    N = randint(7, 15)
    M = randint(7, 15)
    per_obs = randint(1, 30)
    per_dirty =randint(1, 30)
    cant_childs = randint(1, M - 2)
    return Environment(N, M, per_obs, per_dirty, cant_childs), (N, M, per_obs, per_dirty, cant_childs)

def create_simulations(cant):
    simulations = {}
    for _ in range(cant):
        env, params = create_environment()
        ref_time = randint(3, 40)

        simulations[params] = Simulation(env, ref_time)
    
    return simulations


if __name__ == "__main__":
    sims = create_simulations(10)
    results = {}
    for sim in sims.items():
        params = sim[0]
        simulation = sim[1]
        trash = 0
        reason = {}
        for _ in range(31):
            result = simulation.execute()
            trash += result[0]
            if not result[1] in reason.keys():
                reason[result[1]] = 0
            else:
                reason[result[1]] += 1

            simulation.reset()

        results[params] = (int(trash/30),*reason.items())
    
    print("ok")
