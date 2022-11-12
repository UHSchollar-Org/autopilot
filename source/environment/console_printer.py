
def print_streets(map):
    names = []
    for u,v,name in map.simple_map.edges(data= "name"):
        if not names.__contains__(name):
            names.append(name)
    names.sort()
    print(names)
                
def print_signs(map):
    for n, nbrsdict in map.simple_map.adjacency():
        for nbr, eattr in nbrsdict.items():
            to_print = ""
            to_print += str(n) + " -> " + str(nbr) + " : "
                
            for s in eattr.get("signs"):
                to_print += (str(s) + ",")
            print(to_print)

def print_street_len(map):
    for n, nbrsdict in map.simple_map.adjacency():
        for nbr, eattr in nbrsdict.items():
            to_print = ""
            to_print += str(n) + " -> " + str(nbr) + " : " + str(eattr.get("length"))

            print(to_print)