import PySimpleGUI as sg
import copy

sg.theme("DarkBrown4")
#sg.theme_text_color("#c73530")
sg.theme_text_color("#f82222")
sg.theme_border_width(0)
sg.theme_input_background_color("#2b2b2b")
sg.theme_input_text_color("#c75450")
sg.theme_button_color((sg.theme_text_color(), sg.theme_background_color()))
disabled_color = "#3c3f41"
input_background_color = "#333333"


fontsize = 15
fonttype = "DejaVu Sans Mono"
small_font = (fonttype, fontsize-4)


atom_units = {
    "H": 1.008,
    "He": 4.0026,
    "Li": 6.94,
    "Be": 9.0122,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.180,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.085,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "Ar": 39.948,
    "K": 39.098,
    "Ca": 40.078,
    "Sc": 44.956,
    "Ti": 47.867,
    "V": 50.942,
    "Cr": 51.996,
    "Mn": 54.938,
    "Fe": 55.845,
    "Co": 58.933,
    "Ni": 58.693,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ga": 69.723,
    "Ge": 72.630,
    "As": 74.922,
    "Se": 78.971,
    "Br": 79.904,
    "Kr": 83.798,
    "Rb": 1.0,
    "Sr": 1.0,
    "Y": 1.0,
    "Zr": 1.0,
    "Nb": 1.0,
    "Mo": 1.0,
    "Tc": 1.0,
    "Ru": 1.0,
    "Rh": 1.0,
    "Pd": 1.0,
    "Ag": 1.0,
    "Cd": 1.0,
    "In": 1.0,
    "Sn": 1.0,
    "Sb": 1.0,
    "Te": 1.0,
    "I": 1.0,
    "Xe": 1.0,
    "Cs": 1.0,
    "Ba": 1.0,
    "Hf": 1.0,
    "Ta": 1.0,
    "W": 1.0,
    "Re": 1.0,
    "Os": 1.0,
    "Ir": 1.0,
    "Pt": 1.0,
    "Au": 1.0,
    "Hg": 1.0,
    "Tl": 1.0,
    "Pb": 1.0,
    "Bi": 1.0,
    "Po": 1.0,
    "At": 1.0,
    "Rn": 1.0,
    "Fr": 1.0,
    "Ra": 1.0,
    "Rf": 1.0,
    "Db": 1.0,
    "Sg": 1.0,
    "Bh": 1.0,
    "Hs": 1.0,
}


continue_program = True


def print_chemical_reaction(reactants, products):
    string = " + ".join([r.chemical for r in reactants]) + "  ->  " + " + ".join([p.chemical for p in products])
    print(string)


def split_chemical_in_parts(chemical: str):
    splits = []
    last_type = -1  # -1 for None, 0 for Number, 1 for Letter
    for ind, c in enumerate(chemical):
        if c.isdigit():
            if last_type == 0:
                continue
            else:
                splits.append(ind)
                last_type = 0
        else:  # Assuming c is a letter i.e. not a special character
            if c.isupper():
                splits.append(ind)
                last_type = 1
            else:
                continue
    if not splits:
        return []

    output = []
    for i in range(len(splits)-1):
        if chemical[splits[i]].isdigit():
            output.append(int(chemical[splits[i]:splits[i+1]]))
            continue
        output.append(chemical[splits[i]:splits[i+1]])

    if chemical[splits[-1]].isdigit():
        output.append(int(chemical[splits[-1]:]))
    else:
        output.append(chemical[splits[-1]:])

    return output


def balance_reaction(reactants, products):
    states = [[reactants, products]]
    for r in states[0][0] + states[0][1]:
        r.amount = 1
        r.redefine_chemical_string()
    seen_missing_comb = []
    new_states = []
    t = 0
    while t < 300000:
        seen_missing_comb.clear()
        print(t, len(states))
        if len(states) == 0:
            return reactants, products
        for s in states:
            r = s[0]
            p = s[1]

            r_missing, p_missing = check_balanced(r, p)
            if [r_missing, p_missing] in seen_missing_comb:
                continue
            seen_missing_comb.append([r_missing, p_missing])
            if r_missing:
                for m in r_missing:
                    for ind, n in enumerate(r):
                        if m in n.components:
                            new_r = r[:]
                            new_r.pop(ind)
                            new_r.append(copy.deepcopy(n))
                            new_r[-1].amount += 1
                            #new_r[-1].redefine_chemical_string()
                            new_states.append([new_r, p])
                continue
            elif p_missing:
                for m in p_missing:
                    for ind, n in enumerate(p):
                        if m in n.components:
                            new_p = p[:]
                            new_p.pop(ind)
                            new_p.append(copy.deepcopy(n))
                            new_p[-1].amount += 1
                            #new_p[-1].redefine_chemical_string()
                            new_states.append([r, new_p])
                continue
            else:
                for m in r + p:
                    m.redefine_chemical_string()
                return r, p
        states.clear()
        states = new_states[:]
        new_states.clear()
        t += 1
    return reactants, products


def check_balanced(reactants, products):
    r_components = {}
    p_components = {}
    for r in reactants:
        for n in r.components:
            if n in r_components:
                r_components[n] += r.components[n] * r.amount
                continue
            r_components[n] = r.components[n] * r.amount
    for p in products:
        for n in p.components:
            if n in p_components:
                p_components[n] += p.components[n] * p.amount
                continue
            p_components[n] = p.components[n] * p.amount

    r_missing = {}
    for i in p_components:
        if i not in r_components:
            r_missing[i] = p_components[i]
        elif r_components[i] < p_components[i]:
            r_missing[i] = p_components[i] - r_components[i]

    p_missing = {}
    for i in r_components:
        if i not in p_components:
            p_missing[i] = r_components[i]
        elif p_components[i] < r_components[i]:
            p_missing[i] = r_components[i] - p_components[i]

    return r_missing, p_missing


class Molecule:
    def __init__(self, chemical="", mass=-1, mol=-1, key=None):
        self.mass = mass
        self.mol = mol
        self.amount = 1
        self.key = key

        self.molarmass = 0
        self.chemical = chemical
        self.components = {}

        if chemical != "":
            self.update()

    def is_fully_defined(self):
        return self.chemical and self.mass != -1 and self.molarmass != 0 and self.mol != -1

    def gather_components(self):
        self.components = {}
        if self.chemical == "":
            return
        l = ""
        l_double = False
        self.amount = 1
        for i in split_chemical_in_parts(self.chemical):
            if isinstance(i, int):
                if l == "":
                    self.amount = i
                elif self.components[l] == 1:
                    self.components[l] = i
                elif l_double:
                    self.components[l] += i - 1
                    l_double = False
                else:
                    self.components[l] += i
                continue
            if i not in self.components:
                self.components[i] = 1
            else:
                self.components[i] += 1
                l_double = True
            l = i

    def calculate_molarmass(self):
        self.molarmass = sum([atom_units[n]*self.components[n] for n in self.components])

    def get_molarmass_string(self):
        if self.molarmass == 0:
            return ""
        return str(round(self.molarmass, 9))

    def get_mass_string(self):
        if self.mass == -1:
            return ""
        return str(round(self.mass, 9))

    def get_mol_string(self):
        if self.mol == -1:
            return ""
        return str(round(self.mol, 9))

    def redefine_chemical_string(self):
        self.chemical = f"{self.amount if self.amount != 1 else ''}" + "".join([f"{i}{self.components[i] if self.components[i] != 1 else ''}" for i in self.components])

    def try_calculate_mass_or_mol(self):
        if self.mass == -1 and self.mol == -1:
            return
        elif self.mass != -1:
            self.mol = self.mass/self.molarmass
        elif self.mol != -1:
            self.mass = self.mol*self.molarmass

    def update(self):
        self.gather_components()
        self.calculate_molarmass()
        self.try_calculate_mass_or_mol()

    def get_SimpleGUI_objects(self):
        return sg.Input(self.chemical, size=(16, 1), k=self.key),\
               sg.Input(f"{self.get_mass_string()}", size=(16, 1), k=f"{self.key}m"),\
               sg.T(f"{self.get_molarmass_string()}", size=(16, 1), k=f"{self.key}M"),\
               sg.Input(f"{self.get_mol_string()}", size=(16, 1), k=f"{self.key}n")


reactants = []
products = []


class Window:
    def __init__(self, reactants=[], products=[]):
        self.reactants = reactants
        self.products = products
        self.values = None

        self.should_exit = False
        self.raw_layout = [[]]
        self.layout = [[]]  # redefined in the method update_layout()
        self.redo_layout()

        self.win = sg.Window(title="Beregningsskema", layout=self.layout, resizable=True, font=(fonttype, fontsize), finalize=True, use_default_focus=False)

        self.win["Update"].block_focus()
        self.win["ReactantInput"].bind("<Return>", "_enter")
        self.win["ProductInput"].bind("<Return>", "_enter")

        self.loop()

    def add_reactant(self, chemical=""):
        self.reactants.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()

    def add_product(self, chemical=""):
        self.products.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()

    def redo_layout(self):
        self.redefine_raw_layout()
        self.update_layout()

    def redefine_raw_layout(self):
        self.raw_layout = [[None, sg.T("", k="MissingReactants", size=(16, 1)), sg.Input("", k="ReactantInput", size=(16, 1), background_color=input_background_color), sg.T("Reactants", enable_events=True, k="addReactant"), sg.Text("|"), sg.T("Products", enable_events=True, k="addProduct"), sg.Input("", k="ProductInput", size=(16, 1), background_color=input_background_color), sg.T("", k="MissingProducts", size=(16, 1))],
                           [sg.T("Molecules:"), None, None, None, sg.Text("->"), None, None, None],
                           [sg.T("m (g)    :"), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("M (g/mol):"), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("n (mol)  :"), None, None, None, sg.Text("|"), None, None, None]]
        i = 4  # i should be equal to the index of the dividing line between reactants and products
        for m in self.reactants:
            if self.raw_layout[1][i-1] is not None:
                self.raw_layout[0] = [None] + self.raw_layout[0]
                for n in range(1, len(self.raw_layout)):
                    self.raw_layout[n] = self.raw_layout[n][:i] + [None] + self.raw_layout[n][i:]
                i += 1
            self.raw_layout[1][i-1], self.raw_layout[2][i-1], self.raw_layout[3][i-1], self.raw_layout[4][i-1] = m.get_SimpleGUI_objects()

        for m in self.products:
            if self.raw_layout[1][i + 1] is not None:
                self.raw_layout[0] = self.raw_layout[0] + [None]
                for n in range(1, len(self.raw_layout)):
                    self.raw_layout[n] = self.raw_layout[n][:i+1] + [None] + self.raw_layout[n][i+1:]
            self.raw_layout[1][i+1], self.raw_layout[2][i+1], self.raw_layout[3][i+1], self.raw_layout[4][i+1] = m.get_SimpleGUI_objects()

    def update_molecules(self):
        self.save_stuff()

        for r in self.reactants + self.products:
            if r.is_fully_defined():
                for p in self.reactants + self.products:
                    if r == p or p.chemical == "":
                        continue
                    p.mol = r.mol * (p.amount / r.amount)
                break
        self.write_molecules()

    def write_molecules(self):
        for r in self.reactants + self.products:
            self.win[r.key](value=r.chemical)
            self.win[f"{r.key}m"](value=r.get_mass_string())
            self.win[f"{r.key}M"](value=r.get_molarmass_string())
            self.win[f"{r.key}n"](value=r.get_mol_string())

    def save_stuff(self):
        try:
            for r in self.reactants + self.products:
                r.chemical = self.values[r.key]
                r.mass = float(self.values[f"{r.key}m"]) if self.values[f"{r.key}m"] else -1
                r.mol = float(self.values[f"{r.key}n"]) if self.values[f"{r.key}n"] else -1
                r.update()
        except ValueError:  # if input field doesn't contain number
            pass

    def reset_amounts(self):
        for r in self.reactants + self.products:
            r.mass = -1
            r.mol = -1
            self.win[f"{r.key}m"](value="")
            self.win[f"{r.key}n"](value="")

    def calculate_mass_diff(self):
        return round(sum([r.mass for r in self.reactants]) - sum([p.mass for p in self.products]), 9)

    def calculate_reactants_mass(self):
        return round(sum([r.mass for r in self.reactants]), 10)

    def mol_mass_defined(self):
        return sum([r.mass == -1 or r.mol == -1 for r in self.reactants + self.products]) == 0

    def restart(self):
        global reactants
        global products
        global continue_program
        reactants = self.reactants
        products = self.products
        self.should_exit = True
        continue_program = True

    def check_balanced(self):
        try:
            self.save_stuff()
        except KeyError:
            return
        r_missing, p_missing = check_balanced(self.reactants, self.products)

        self.win["MissingReactants"](value=" ".join([f"{r_missing[n]}{n}" for n in r_missing]))
        self.win["MissingProducts"](value=" ".join([f"{p_missing[n]}{n}" for n in p_missing]))

        return len(r_missing) == 0 and len(p_missing) == 0

    def loop(self):
        while not self.should_exit:
            event, self.values = self.win.read(timeout=200)
            if event == sg.WIN_CLOSED:
                break

            if event != "__TIMEOUT__":
                print(event)

            if self.check_balanced():
                self.win["BALANCED"].update(text_color="#5B7641")
            else:
                self.win["BALANCED"].update(text_color="#323232")

            if self.mol_mass_defined():
                self.win["MassDiff"](value=self.calculate_mass_diff())
                self.win["RMass"](value=f"{self.calculate_reactants_mass():.8f}g")
                self.win["MassDiff"].update(text_color=sg.theme_text_color())
                self.win["RMass"].update(text_color=sg.theme_text_color())
            else:
                self.win["MassDiff"].update(text_color=disabled_color)
                self.win["RMass"].update(text_color=disabled_color)

            if event == sg.WIN_CLOSED or self.should_exit:
                break
            elif event == "__TIMEOUT__":
                continue
            elif event == "addReactant":
                self.add_reactant()
            elif event == "addProduct":
                self.add_product()
            elif event == "Update":
                self.update_molecules()
            elif event == "Reset":
                self.reactants.clear()
                self.products.clear()
                self.restart()
            elif event == "ResetAmounts":
                self.reset_amounts()
            elif event == "ReactantInput_enter":
                self.add_reactant(self.values["ReactantInput"])
            elif event == "ProductInput_enter":
                self.add_product(self.values["ProductInput"])
            elif event == "Double":
                self.save_stuff()
                for r in self.reactants + self.products:
                    r.amount *= 2
                    r.redefine_chemical_string()
                self.write_molecules()
            elif event == "Half":
                self.save_stuff()
                for r in self.reactants + self.products:
                    r.amount = max(r.amount // 2, 1)
                    r.redefine_chemical_string()
                self.write_molecules()
            elif event == "Auto-balance":
                self.save_stuff()
                self.reactants, self.products = balance_reaction(self.reactants, self.products)
                self.write_molecules()
            elif event[:10] == "rmolecule:":
                chem = event[10:]
                self.add_reactant(chem)
            elif event[:10] == "pmolecule:":
                chem = event[10:]
                self.add_product(chem)

        self.win.close()

    def update_layout(self):
        main_button_panel = [[sg.B("Update", enable_events=True, font=small_font, k="Update"), sg.T("BALANCED", font=small_font, k="BALANCED")],
                             [sg.B("Reset", font=small_font), sg.B("ResetAmounts", font=small_font)]]
        data_panel = [[sg.T("Mass diff (r-p): ", font=small_font), sg.T("0." + "0"*12, k="MassDiff", font=small_font), sg.T("|", font=small_font), sg.T("Mass (r): ", font=small_font), sg.T("0." + "0"*12, k="RMass", font=small_font)],
                     ]
        secondary_button_panel = [[sg.B("Double", font=small_font), sg.B("Auto-balance", font=small_font)],
                                  [sg.B("Half", font=small_font)]]
        layout_prefix = [[sg.Col(main_button_panel), sg.Col(data_panel), sg.Col(secondary_button_panel)]]
        mol_tuple = (("O2", "CO2", "H2O", "N2", "CH4", "C2H6", "C3H8", "C4H10", "C5H12", "C6H14"),
                     ("C7H16", "C8H18", "C9H20", "C10H22"))
        r_add = [[sg.B(n, k=f"rmolecule:{n}", font=small_font) for n in i] for i in mol_tuple]
        p_add = [[sg.B(n, k=f"pmolecule:{n}", font=small_font) for n in i] for i in mol_tuple]
        layout_suffix = [[sg.Col([[sg.Col(r_add, justification="l", expand_x=True), sg.Col(p_add, justification="r", element_justification="r")]], expand_x=True, expand_y=True)]]

        self.layout = [[]]
        for i in range(len(self.raw_layout[0])):
            self.layout[0] += [sg.Col([[sg.Text("") if n[i] is None else n[i]] for n in self.raw_layout], element_justification="c")]
        self.layout = layout_prefix + self.layout + layout_suffix


while continue_program:
    continue_program = False
    Window(reactants, products)
