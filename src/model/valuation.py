def generate_next_valuation(curr_valuation: list[bool]):
    n = len(curr_valuation)
    for i in range(n-1, -1, -1):
        if curr_valuation[i] == True:
            curr_valuation[i] = False            
        else:
            curr_valuation[i] = True
            break
    if i == 0:
        return 


def valuation(n: int) -> list[bool]:
    atoms = list(False for _ in range(n))
    end_reached = False

    while not end_reached:
        yield atoms
        if all(atoms):
            end_reached = True

        generate_next_valuation(atoms)
        


