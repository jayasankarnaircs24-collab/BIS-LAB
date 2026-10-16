import random
SPAN = 6000.0        
MOMENT = 1.125e8    
E_STEEL = 200000.0   
SIGMA_ALLOW = 250.0  
DEFLECT_LIMIT = 24.0 

def get_fitness(beam):
    b, h = beam
    area = b * h
    
    i_x = (b * (h ** 3)) / 12.0  
    z_x = (b * (h ** 2)) / 6.0   
    
    stress = MOMENT / z_x
    deflection = (5 * 25.0 * (SPAN ** 4)) / (384 * E_STEEL * i_x)
    aspect_ratio = h / b
    
    penalty = 0
    if stress > SIGMA_ALLOW: penalty += 500000
    if deflection > DEFLECT_LIMIT: penalty += 500000
    if aspect_ratio < 1.5 or aspect_ratio > 3.5: penalty += 500000
        
    return 1.0 / (area + penalty) 
POP_SIZE = 30
MUTATION_RATE = 0.15
CROSSOVER_RATE = 0.8
GENERATIONS = 50

population = [[random.uniform(50, 400), random.uniform(100, 600)] for _ in range(POP_SIZE)]

best_beam = None
best_fitness = -1

for gen in range(GENERATIONS):
    # 4. EVALUATE FITNESS
    fitness_scores = [get_fitness(ind) for ind in population]
    
    for i, score in enumerate(fitness_scores):
        if score > best_fitness:
            best_fitness = score
            best_beam = population[i].copy()
            
    total_fit = sum(fitness_scores) if sum(fitness_scores) > 0 else 1
    probs = [f / total_fit for f in fitness_scores]
    
    new_pop = []
    while len(new_pop) < POP_SIZE:
        p1 = random.choices(population, weights=probs, k=1)[0]
        p2 = random.choices(population, weights=probs, k=1)[0]
        
        if random.random() < CROSSOVER_RATE:
            a = random.random()
            c1 = [a * p1[0] + (1-a) * p2[0], (1-a) * p1[1] + a * p2[1]]
            c2 = [(1-a) * p1[0] + a * p2[0], a * p1[1] + (1-a) * p2[1]]
        else:
            c1, c2 = p1.copy(), p2.copy()
            
        for child in [c1, c2]:
            for gene in range(2):
                if random.random() < MUTATION_RATE:
                    child[gene] += random.uniform(-20, 20)
                    child[gene] = max(50, min(600, child[gene])) 
            new_pop.append(child)
            
    population = new_pop[:POP_SIZE]


opt_b, opt_h = best_beam
print("--- Optimization Complete ---")
print(f"Optimal Width:  {opt_b:.1f} mm")
print(f"Optimal Height: {opt_h:.1f} mm")
print(f"Final Area:     {opt_b * opt_h:.1f} mm²")
