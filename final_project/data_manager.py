from models import Component

def load_catalog(filename):
    catalog = []
    try:
        with open(filename, "r") as f: # r for read mode
            next(f)  
            for line in f:
                if not line.strip(): continue
                vals = line.strip().split(",")
                d = {"Type": vals[0], "Name": vals[1], "Socket": vals[2], 
                     "Memory": vals[3], "Price": vals[4], "TDP": vals[5]}
                catalog.append(Component(d))
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
    return catalog

def save_to_file(build):
    filename = f"{build.name}.txt"
    with open(filename, "w") as f:
        f.write(f"BUILD NAME: {build.name}\n")
        f.write("-" * 30 + "\n") #i love the fact that i can multiply char/str
        for cat, p in build.parts.items():
            name = p.name if p else "None"
            f.write(f"{cat}: {name}\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total Cost: ${build.get_total()}\n")
    print(f"Successfully saved to {filename}")