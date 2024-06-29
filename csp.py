from typing import List, Dict, Tuple


class Evacuee:
    def __init__(self, ID: str, evac_type: str, members: int, has_pet: bool,
                 housing_preference: str, dietary_needs: str,
                 location_preference: str, friends_community: str,
                 job_proximity: str):
        self.ID = ID
        self.evac_type = evac_type
        self.members = members
        self.has_pet = has_pet
        self.housing_preference = housing_preference
        self.dietary_needs = dietary_needs
        self.location_preference = location_preference
        self.friends_community = friends_community
        self.job_proximity = job_proximity

    def __repr__(self):
        return (f"Evacuee(ID={self.ID}, evac_type={self.evac_type}, members={self.members}, "
                f"has_pet={self.has_pet}, housing_preference={self.housing_preference}, "
                f"dietary_needs={self.dietary_needs}, location_preference={self.location_preference}, "
                f"friends_community={self.friends_community}, job_proximity={self.job_proximity})")


class HousingAllocation:
    def __init__(self, ID: str, house_type: str, pet_friendly: bool, capacity: int,
                 location: str, amenities: List[str]):
        self.ID = ID
        self.house_type = house_type
        self.pet_friendly = pet_friendly
        self.capacity = capacity
        self.location = location
        self.amenities = amenities

    def __repr__(self):
        return (f"HousingAllocation(ID={self.ID}, house_type={self.house_type}, pet_friendly={self.pet_friendly}, "
                f"capacity={self.capacity}, location={self.location}, amenities={self.amenities})")


def satisfy_constraints(evacuee: Evacuee, allocation: HousingAllocation) -> bool:
    """ Check if an allocation satisfies the evacuee's constraints. """
    if evacuee.members > allocation.capacity:
        return False
    if evacuee.has_pet and not allocation.pet_friendly:
        return False
    return True


def revise(domains: Dict[str, List[HousingAllocation]], xi: str, xj: str) -> bool:
    revised = False
    for x in domains[xi][:]:
        if all(not satisfy_constraints(evacuee, x) or x.ID == y.ID for evacuee in evacuees for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised


def ac3(domains: Dict[str, List[HousingAllocation]], evacuees: List[Evacuee]) -> bool:
    queue = [(xi.ID, xj.ID) for xi in evacuees for xj in evacuees if xi != xj]
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in evacuees:
                if xk.ID != xi and xk.ID != xj:
                    queue.append((xk.ID, xi))
    return True


def backtracking(domains: Dict[str, List[HousingAllocation]], assignment: Dict[str, HousingAllocation],
                 evacuees: List[Evacuee], all_assignments: List[Dict[str, HousingAllocation]], limit: int = 10):
    """ Backtracking algorithm to find valid assignments. """
    if len(all_assignments) >= limit:
        return all_assignments

    if len(assignment) == len(evacuees):
        all_assignments.append(assignment.copy())
        return all_assignments

    evacuee = next(evac for evac in evacuees if evac.ID not in assignment)
    for allocation in domains[evacuee.ID]:
        if allocation.ID in [assign.ID for assign in assignment.values()]:
            continue

        assignment[evacuee.ID] = allocation
        backtracking(domains, assignment, evacuees, all_assignments, limit)
        del assignment[evacuee.ID]

    return all_assignments


def generate_preference_list(evacuees: List[Evacuee], allocations: List[HousingAllocation]):
    """ Generate a preference list for each evacuee based on constraints. """
    domains = {evac.ID: [alloc for alloc in allocations if satisfy_constraints(evac, alloc)] for evac in evacuees}

    print("Initial Domains:", {k: [a.ID for a in v] for k, v in domains.items()})  # Debugging: Print initial domains

    # Apply AC-3 to enforce arc consistency
    if not ac3(domains, evacuees):
        return "No valid assignment found after applying AC-3."

    print("Domains after AC-3:", {k: [a.ID for a in v] for k, v in domains.items()})  # Debugging: Print domains after AC-3

    # Apply backtracking to find valid assignments
    all_assignments = backtracking(domains, {}, evacuees, [], limit=10)
    if not all_assignments:
        return "No valid assignments found."

    return all_assignments


# Example usage
evacuees = [
    Evacuee("E1", "family", 4, True, "house", "kosher", "central", "community1", "workplace1"),
    Evacuee("E2", "single", 1, False, "hotel", "none", "north", "community2", "workplace2")
]

allocations = [
    HousingAllocation("H1", "house", True, 5, "central", ["kitchen", "internet"]),
    HousingAllocation("H2", "hotel", False, 2, "north", ["internet"]),
    HousingAllocation("H3", "house", False, 4, "central", ["kitchen"]),
]

result = generate_preference_list(evacuees, allocations)
for i, assignment in enumerate(result):
    print(f"Assignment {i+1}:")
    for evac_id, alloc in assignment.items():
        print(f"  Evacuee {evac_id} -> Allocation {alloc.ID}")
