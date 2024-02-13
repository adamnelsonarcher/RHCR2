import numpy as np
fCalls = 0

def frog(x): # x is an array with 2 items
  x1, x2 = x
  global fCalls
  fCalls += 1
  return (x1 * np.sin(np.sqrt(np.abs(x2 + 1 - x1))) *
         np.cos(np.sqrt(np.abs(x1 + x2 + 1))) +(x2 + 1) * 
         np.cos(np.sqrt(np.abs(x2 + 1 - x1))) *
         np.sin(np.sqrt(np.abs(x1 + x2 + 1))))

def RHC(sp, z, p, seed):
  #print(f"RHC: {sp}, {z}, {p}, {seed}")
  np.random.seed(seed)
  current = sp

  while True:
    # Sample p solutions in the neighborhood of size z of the current solution
    neighbors = []
    for _ in range(p):  # Iterate p times
      random_vector = np.random.uniform(-z, z, size=2) 
      neighbor = current + random_vector
      if (-512 <= neighbor[0] <= 512 and -512 <= neighbor[1] <= 512):
        neighbors.append(neighbor) #only if it is within [-512, 512]

    # Find the best neighbor based on the objective function
    best_value = float('inf') 
    sol = None

    for neighbor in neighbors:  # Iterate over each neighbor
      neighbor_value = frog(neighbor)
      if neighbor_value < best_value: 
        best_value = neighbor_value  # Update the best value
        sol = neighbor  # Update the best neighbor

    #print(f"{frog(sol)} vs {frog(current) - 0.0001}")
    if frog(sol) < (frog(current) - 0.0001): #threshold of 0.0001 to save computations
      current = sol  # continue to run with new starting point
    else:
      return current # terminate the loop with the best solution

def RHCR2(sp, z, p, seed):
  global fCalls
  FrogCalls = []
  # Run RHC three times with decreasing neighborhood sizes
  sol1 = RHC(sp, z, p, seed)
  FrogCalls.append(fCalls)
  fCalls = 0
  sol2 = RHC(sol1, z/20, p, seed+1)
  FrogCalls.append(fCalls)
  fCalls = 0
  sol3 = RHC(sol2, z/400, p, seed+2)
  FrogCalls.append(fCalls)
  fCalls = 0
  FrogCalls.append(sum(FrogCalls))
  # Return solutions and their corresponding function values
  return sol1, sol2, sol3, FrogCalls


###### user input and printing ##############
sp_input = input("Enter the value for sp (x,y), leave blank for (0,0): ")
sp = tuple(map(int, sp_input.split(','))) if sp_input.strip() else (0, 0)
z_input = input("Enter the value for z or leave blank for default (9): ")
z = int(z_input) if z_input.strip() else 9
p_input = input("Enter the value for p or leave blank for default (400): ")
p = int(p_input) if p_input.strip() else 400
seed_input = input("Enter a seed value or leave blank for random seed: ")
seed = int(seed_input) if seed_input.strip() else np.random.randint(1, 1000)

sol1, sol2, sol3, fCall = RHCR2(sp, z, p, seed)

print(f"\nFor parameters: \nsp={sp}, z={z}, p={p}, seed={seed}")
print(f"starting height: {frog(sp)}\n")
print(f"sol1, (z: {z}): {sol1}, "
      f"\n   f(sol1): {frog(sol1)}"
      f"\n   times f was called: {fCall[0]}\n")
print(f"sol2, (z: {z/20}): {sol2}, "
      f"\n   f(sol2): {frog(sol2)}"
      f"\n   times f was called: {fCall[1]}\n")
print(f"sol3, (z: {z/400}): {sol3}, "
      f"\n   f(sol3): {frog(sol3)}"
      f"\n   times f was called: {fCall[2]}\n")
print(f"Total calls to f: {fCall[3]}")
######################################
