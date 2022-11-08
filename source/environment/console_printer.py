
def print_street(self):
        names = []
        for u,v,name in self.simple_map.edges(data= "name"):
            if not names.__contains__(name):
                names.append(name)
        names.sort()
        print(names)
                
def print_signs(self):
        for n, nbrsdict in self.simple_map.adjacency():
            for nbr, eattr in nbrsdict.items():
                to_print = ""
                to_print += str(n) + " -> " + str(nbr) + " : "
                
                for s in eattr.get("signs"):
                    to_print += (str(s) + ",")
                print(to_print)