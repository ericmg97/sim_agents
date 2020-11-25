from random import randint
from environment import Environment
from simulation import Simulation

def create_environment(agent_type):
    N = randint(5, 10)
    M = randint(5, 10)
    per_obs = randint(1, 20)
    per_dirty = randint(1, 20)
    cant_childs = randint(1, M - 4)
    return Environment(N, M, per_obs, per_dirty, cant_childs, agent_type), (N, M, per_obs, per_dirty, cant_childs)

def create_simulations(cant, agent_type):
    simulations = {}
    for _ in range(cant):
        env, params = create_environment(agent_type)
        ref_time = randint(3, 40)

        simulations[params] = Simulation(env, ref_time)
    
    return simulations


if __name__ == "__main__":
    # test = create_simulations(1, "Trash")
    # for item in test.items():
    #     outp = item[1].execute()

    #Agent Type: Trash Goal or Children Goal
    sims = create_simulations(10, "Trash")
    results = {}
    for sim in sims.items():
        params = sim[0]
        simulation = sim[1]
        trash = 0
        reason = {}
        for _ in range(30):
            result = simulation.execute()
            trash += result[0]
            if not result[1] in reason.keys():
                reason[result[1]] = 1
            else:
                reason[result[1]] += 1

            simulation.reset()

        results[params] = (int(trash/30),*reason.items())
    
    print("aa")