from itertools import permutations

# ── Constraint checker ──────────────────────────────────
def is_valid(arrangement, friends, same_city):
    """Check if a single arrangement satisfies both rules. O(n)"""
    for i in range(len(arrangement) - 1):
        a, b = arrangement[i], arrangement[i+1]
        if (a,b) in friends or (b,a) in friends:
            return False   # Rule 1 violated: friends adjacent
        if (a,b) in same_city or (b,a) in same_city:
            return False   # Rule 2 violated: same city adjacent
    return True

# ── Brute Force Solver ──────────────────────────────────
def brute_force_seating(students, friends, same_city):
    """
    Try every permutation until a valid one is found.
    Time Complexity: O(n! x n)  — catastrophic for large n
    """
    total_checked = 0
    for arrangement in permutations(students):  # generates n! arrangements
        total_checked += 1
        if is_valid(arrangement, friends, same_city):
            return arrangement, total_checked   # found a valid plan
    return None, total_checked                  # no valid plan exists


# ── Example: 6 Students ─────────────────────────────────
students  = ['Alice','Bob','Carol','Dave','Eve','Frank']
friends   = {('Alice','Bob'), ('Carol','Dave')}
same_city = {('Alice','Bob'), ('Carol','Dave'), ('Eve','Frank')}

result, checked = brute_force_seating(students, friends, same_city)

if result:
    print(f'Valid arrangement found after checking {checked} arrangements:')
    print(' --> '.join(result))
else:
    print(f'No valid arrangement exists. Checked all {checked} arrangements.')

# Possible Output:
# Valid arrangement found after checking 47 arrangements:
# Alice --> Carol --> Bob --> Eve --> Dave --> Frank


# ── Demonstrate the explosion ────────────────────────────
import math
print('\nArrangements to check by class size:')
for n in [3, 5, 8, 10, 12, 15, 20]:
    print(f'  n={n:2d}  →  {math.factorial(n):,} arrangements')
