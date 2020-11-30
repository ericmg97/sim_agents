from random import randint
from environment import Environment
from simulation import Simulation
from copy import deepcopy

def create_environment():
    N = randint(5, 10)
    M = randint(5, 10)
    per_obs = randint(10, 30)
    per_dirty = randint(10, 20)
    cant_childs = randint(1, M - 3)
    return Environment(N, M, per_obs, per_dirty, cant_childs), (N, M, per_obs, per_dirty, cant_childs)

def create_simulations(cant):
    simulations = {}
    for _ in range(cant):
        env, params = create_environment()
        ref_time = randint(5, 8)

        simulations[params] = Simulation(env, ref_time)
    
    return simulations


if __name__ == "__main__":
    #Agent Type: Trash Goal or Children Goal
    #Brute or Smart
    sims1 = create_simulations(10)
    sims2 = deepcopy(sims1)
    print("_"*60)
    print("|%-5s|%-8s|%-15s|%-13s|%-13s|" % ("Sim #", " Tamaño", " Obstaculos(%)", " Suciedad(%)", " Cant. Niños"))
    print("_"*60)
    
    results = {}
    for no, (sim1, sim2) in enumerate(zip(sims1.items(), sims2.items())):
        params = sim1[0]    
        print("|%-5s|%-8s|%-15s|%-13s|%-13s|" % (no+1, f"  {params[0]}x{params[1]}", f"      {params[2]}%", f"     {params[3]}%", f"      {params[4]}"))
        
        simulation1 = sim1[1]
        simulation2 = sim2[1]
        trash1, trash2 = 0, 0
        reason1 = {}
        reason2 = {}
        for _ in range(30):
            result1 = simulation1.execute("Brute")
            result2 = simulation2.execute("Smart")
            trash1 += result1[0]
            trash2 += result2[0]

            if not result1[1] in reason1.keys():
                reason1[result1[1]] = 1
            else:
                reason1[result1[1]] += 1
            
            if not result2[1] in reason2.keys():
                reason2[result2[1]] = 1
            else:
                reason2[result2[1]] += 1

            simulation1.reset()
            simulation2.reset()

        results[params] = [[int(trash1/30), reason1], [int(trash2/30), reason2]]
    
    print("\n")

    print("_"*65)
    print("|%-5s|%-14s|%-13s|%-11s|%-8s|%-7s|" % ("Sim #", " Avg Suciedad", " Todo Limpio", " Despedido", " Tiempo", " Total"))
    print("_"*65)

    for i, result in enumerate(results.items()):
        outp_reasons = {"Todo Limpio":0, "Despedido":0, "Tiempo Agotado":0}
        outp = result[1][0]   
        
        for item in outp[1].items():
            outp_reasons[item[0]] = item[1]
        total = sum(outp[1].values())
        
        print("|%-5s|%-14s|%-13s|%-11s|%-8s|%-7s|" % (i + 1, f"    {outp[0]}%",f"     {outp_reasons['Todo Limpio']}", f"    {outp_reasons['Despedido']}", f"   {outp_reasons['Tiempo Agotado']}", f"  {total}"))

    print("\n")

    print("_"*65)
    print("|%-5s|%-14s|%-13s|%-11s|%-8s|%-7s|" % ("Sim #", " Avg Suciedad", " Todo Limpio", " Despedido", " Tiempo", " Total"))
    print("_"*65)

    for i, result in enumerate(results.items()):
        outp_reasons = {"Todo Limpio":0, "Despedido":0, "Tiempo Agotado":0}
        outp = result[1][1]   
        
        for item in outp[1].items():
            outp_reasons[item[0]] = item[1]
        total = sum(outp[1].values())
        
        print("|%-5s|%-14s|%-13s|%-11s|%-8s|%-7s|" % (i + 1, f"    {outp[0]}%",f"     {outp_reasons['Todo Limpio']}", f"    {outp_reasons['Despedido']}", f"   {outp_reasons['Tiempo Agotado']}", f"  {total}"))