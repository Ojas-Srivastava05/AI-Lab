districts = [
    "Kuchchh", "Banaskantha", "Patan", "Mehsana", "Sabarkantha",
    "Gandhinagar", "Ahmedabad", "Kheda", "Panchmahal", "Dahod",
    "Vadodara", "Anand", "Surendranagar", "Rajkot", "Jamnagar",
    "Porbandar", "Junagadh", "Amreli", "Bhavnagar", "Bharuch",
    "Narmada", "Surat", "Tapi", "Navsari", "Dangs", "Valsad"
]

colors = ["Red", "Green","Blue"]

adjacency = {
    "Kuchchh": ["Banaskantha", "Patan", "Surendranagar", "Rajkot", "Jamnagar"],
    "Banaskantha": ["Kuchchh", "Patan", "Mehsana", "Sabarkantha"],
    "Patan": ["Kuchchh", "Banaskantha", "Mehsana", "Surendranagar"],
    "Mehsana": ["Banaskantha", "Patan", "Sabarkantha", "Gandhinagar", "Ahmedabad", "Surendranagar"],
    "Sabarkantha": ["Banaskantha", "Mehsana", "Gandhinagar", "Kheda", "Panchmahal"],
    "Gandhinagar": ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Ahmedabad": ["Mehsana", "Gandhinagar", "Kheda", "Anand", "Surendranagar", "Bhavnagar"],
    "Kheda": ["Sabarkantha", "Gandhinagar", "Ahmedabad", "Panchmahal", "Anand"],
    "Panchmahal": ["Sabarkantha", "Kheda", "Dahod", "Vadodara", "Anand"],
    "Dahod": ["Panchmahal", "Vadodara"],
    "Vadodara": ["Panchmahal", "Dahod", "Anand", "Bharuch", "Narmada"],
    "Anand": ["Ahmedabad", "Kheda", "Panchmahal", "Vadodara", "Bharuch"],
    "Surendranagar": ["Kuchchh", "Patan", "Mehsana", "Ahmedabad", "Rajkot", "Bhavnagar"],
    "Rajkot": ["Kuchchh", "Surendranagar", "Jamnagar", "Porbandar", "Junagadh", "Amreli", "Bhavnagar"],
    "Jamnagar": ["Kuchchh", "Rajkot", "Porbandar"],
    "Porbandar": ["Rajkot", "Jamnagar", "Junagadh"],
    "Junagadh": ["Rajkot", "Porbandar", "Amreli"],
    "Amreli": ["Rajkot", "Junagadh", "Bhavnagar"],
    "Bhavnagar": ["Ahmedabad", "Surendranagar", "Rajkot", "Amreli"],
    "Bharuch": ["Vadodara", "Anand", "Narmada", "Surat"],
    "Narmada": ["Vadodara", "Bharuch", "Surat", "Tapi", "Dangs"],
    "Surat": ["Bharuch", "Narmada", "Tapi", "Navsari"],
    "Tapi": ["Narmada", "Surat", "Navsari", "Dangs"],
    "Navsari": ["Surat", "Tapi", "Dangs", "Valsad"],
    "Dangs": ["Narmada", "Tapi", "Navsari", "Valsad"],
    "Valsad": ["Navsari", "Dangs"]
}

assignment = {}

def is_valid(district, color):
    for neighbor in adjacency[district]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(index):
    if index == len(districts):
        return True
    district = districts[index]
    for color in colors:
        if is_valid(district, color):
            assignment[district] = color
            if backtrack(index + 1):
                return True
            del assignment[district]
    return False

if backtrack(0):
    print("Map Coloring Solution:")
    for d in districts:
        print(f"  {d}: {assignment[d]}")
else:
    print("No solution found.")
