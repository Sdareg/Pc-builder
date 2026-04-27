class Component:
    def __init__(self, data_dict):# i will add more attributes later
        self.type = data_dict.get('Type')
        self.name = data_dict.get('Name')
        self.socket = data_dict.get('Socket')
        self.memory = data_dict.get('Memory')
        self.price = int(data_dict.get('Price', 0))
        self.tdp = int(data_dict.get('TDP', 0))

class Build:
    def __init__(self, name):
        self.name = name
        self.parts = {
            "CPU": None, "Motherboard": None, "GPU": None, 
            "RAM": None, "Storage": None, "PSU": None, "Case": None
        }

    def add_item(self, component):
        self.parts[component.type] = component

    def get_total(self):
        return sum(p.price for p in self.parts.values() if p)

    def get_status(self):
        errors = []
        cpu, mobo, psu = self.parts["CPU"], self.parts["Motherboard"], self.parts["PSU"]
        
        for key in ["CPU", "Motherboard", "GPU", "RAM", "Storage", "PSU"]:
            if self.parts[key] is None:
                errors.append(f"Missing essential component: {key}")

        if cpu and mobo:
            if cpu.socket != mobo.socket:
                errors.append(f"Socket Mismatch: {cpu.name} ({cpu.socket}) vs {mobo.name} ({mobo.socket})")
            if cpu.memory != mobo.memory:
                errors.append(f"RAM Mismatch: CPU needs {cpu.memory}, Mobo needs {mobo.memory}")
       
        
        total_watts = sum(p.tdp for p in self.parts.values() if p and p.type !="PSU") #had bug here, forget to not count psu in total energy draw, and was confused were from i was getting additional watts (even after realising my mistake i wrote{...if p and p !="PSU"} and wasted another 20 minutes angry and confused)
        if psu and total_watts > psu.tdp:
            errors.append(f"Insufficient Power: System needs ~{total_watts}W, PSU is {psu.tdp}W")
            
        return errors