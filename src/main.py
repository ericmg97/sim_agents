from random import randint
from environment import Environment
from simulation import Simulation

def create_environment(agent_type):
    N = randint(5, 10)
    M = randint(5, 10)
    per_obs = randint(10, 30)
    per_dirty = randint(10, 20)
    cant_childs = randint(1, M - 3)
    return Environment(N, M, per_obs, per_dirty, cant_childs, agent_type), (N, M, per_obs, per_dirty, cant_childs)

def create_simulations(cant, agent_type):
    simulations = {}
    for _ in range(cant):
        env, params = create_environment(agent_type)
        ref_time = randint(5, 8)

        simulations[params] = Simulation(env, ref_time)
    
    return simulations


if __name__ == "__main__":
    #Agent Type: Trash Goal or Children Goal
    #Brute or Smart
    sims = create_simulations(10, "Brute")
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

        results[params] = [int(trash/30),*reason.items()]
        print(f"Done -> {params}")
    
    for result in results.items():
        params = result[0]
        outp = result[1]
        print("\n________________________________________________\n\n")
        print(f"Cantidad de Filas: {params[0]}\nCantidad de Columnas: {params[1]}\nObstaculos(%): {params[2]}%\nSuciedad(%): {params[3]}%\nCantidad de Niños: {params[4]}\n\n")
        print(f"% de Suciedad Promedio: {outp[0]}%")
        outp.pop(0)
        for o in outp:
            reason = o[0]
            times = o[1]
            print(f"{reason} -> {times} veces")
            