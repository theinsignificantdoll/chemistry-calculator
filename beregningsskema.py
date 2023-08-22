import PySimpleGUI as sg
import copy

sg.theme("LightBrown3")
#sg.theme_text_color("#c73530")
#sg.theme_text_color("#9eb6c5")
#sg.theme_text_color("#f82222")
#sg.theme_border_width(0)
#sg.theme_input_background_color("#2b2b2b")
#sg.theme_input_text_color("#c75450")
#sg.theme_button_color((sg.theme_text_color(), sg.theme_background_color()))
disabled_color = "#3c3f41"
#active_color = "#499c54"
active_color = "#c75450"
input_background_color = "#909090"

DEFAULT_MOLECULE_AMOUNT = 3
CONVERT_SHIFTED = True
USE_SUBSCRIPT = True
USE_MOLECULE_ADD = True
USE_ATOM_ADD = True
FORCE_MONO = True  # Chemical font is unaffected if USE_SUBSCRIPT == True
fontsize = 15
BASE_LEN = 15
MONO_LEN = 16
small_font_subtraction = 2
fonttype = "DejaVu Sans"
chemtype = "DejaVu Sans"
monotype = "DejaVu Sans Mono"

#   DejaVu Sans (Mono)
#   Gadugi
#   Lucida Sans Unicode / Lucida Console
#   Noto Sans / Noto Mono / Noto Serif
#   Rubik
#   Sylfaen
#   Tahoma
#   Verdana

if FORCE_MONO:
    fonttype = monotype
if FORCE_MONO and not USE_SUBSCRIPT:
    chemtype = monotype
small_font = (fonttype, fontsize-small_font_subtraction)
mono = (monotype, fontsize)
chemfont = (chemtype, fontsize)
small_chem = (chemtype, fontsize-small_font_subtraction)


atom_units = {
    "H": 1.00794,
    "He": 4.0026,
    "Li": 6.941,
    "Be": 9.01218,
    "B": 10.811,
    "C": 12.011,
    "N": 14.00674,
    "O": 15.9994,
    "F": 18.9984,
    "Ne": 20.1797,
    "Na": 22.98977,
    "Mg": 24.305,
    "Al": 26.98154,
    "Si": 28.0855,
    "P": 30.97376,
    "S": 32.066,
    "Cl": 35.4527,
    "Ar": 39.948,
    "K": 39.0983,
    "Ca": 40.078,
    "Sc": 44.95591,
    "Ti": 47.867,
    "V": 50.9415,
    "Cr": 51.9961,
    "Mn": 54.93805,
    "Fe": 55.845,
    "Co": 58.93320,
    "Ni": 58.6934,
    "Cu": 63.546,
    "Zn": 65.39,
    "Ga": 69.723,
    "Ge": 72.61,
    "As": 74.92159,
    "Se": 78.96,
    "Br": 79.904,
    "Kr": 83.798,
    "Rb": 85.4678,
    "Sr": 87.62,
    "Y": 88.90585,
    "Zr": 91.224,
    "Nb": 92.9064,
    "Mo": 95.94,
    "Tc": 98.0,
    "Ru": 101.07,
    "Rh": 102.9055,
    "Pd": 106.42,
    "Ag": 107.8682,
    "Cd": 112.411,
    "In": 114.818,
    "Sn": 118.710,
    "Sb": 121.760,
    "Te": 127.60,
    "I": 126.90447,
    "Xe": 131.29,
    "Cs": 132.90543,
    "Ba": 137.327,
    "Hf": 178.49,
    "Ta": 180.9479,
    "W": 183.84,
    "Re": 186.207,
    "Os": 190.23,
    "Ir": 192.217,
    "Pt": 195.08,
    "Au": 196.96654,
    "Hg": 200.59,
    "Tl": 204.3833,
    "Pb": 207.2,
    "Bi": 208.98037,
    "Po": 209.0,
    "At": 210.0,
    "Rn": 222.0,
    "Fr": 223.0,
    "Ra": 226.0254,
    "Rf": 261.0,
    "Db": 262,
    "Sg": 266,
    "Bh": 262,
    "Hs": 265,
}


continue_program = True


def print_chemical_reaction(reactants, products):
    string = " + ".join([r.chemical for r in reactants]) + "  ->  " + " + ".join([p.chemical for p in products])
    print(string)


def visual_to_chem(chem, ignore_use_subscript=False):
    if ignore_use_subscript or not USE_SUBSCRIPT:
        return chem
    amount = 1
    a = ""
    for m in chem:
        if not m.isdigit():
            break
        a += m
        amount = int(a)
    chem = chem[len(a):]
    chem = chem.replace("\u207A", "+")
    chem = chem.replace("\u207B", "-")
    chem = chem.replace("\u2070", "0")
    chem = chem.replace("\u00B9", "1")
    chem = chem.replace("\u00B2", "2")
    chem = chem.replace("\u00B3", "3")
    chem = chem.replace("\u2074", "4")
    chem = chem.replace("\u2075", "5")
    chem = chem.replace("\u2076", "6")
    chem = chem.replace("\u2077", "7")
    chem = chem.replace("\u2078", "8")
    chem = chem.replace("\u2079", "9")

    chem = chem.replace("\u2080", "0")
    chem = chem.replace("\u2081", "1")
    chem = chem.replace("\u2082", "2")
    chem = chem.replace("\u2083", "3")
    chem = chem.replace("\u2084", "4")
    chem = chem.replace("\u2085", "5")
    chem = chem.replace("\u2086", "6")
    chem = chem.replace("\u2087", "7")
    chem = chem.replace("\u2088", "8")
    chem = chem.replace("\u2089", "9")
    if amount == 1:
        return chem
    return f"{amount}{chem}"


def chem_to_visual(chem):
    if not USE_SUBSCRIPT:
        return chem
    amount = 1
    a = ""
    for m in chem:
        if not m.isdigit():
            break
        a += m
        amount = int(a)
    chem = chem[len(a):]
    print(chem.__repr__())
    if "+" in chem or "-" in chem:
        index = 0
        for ind, i in enumerate(chem):
            if i in ("+", "-"):
                index = ind
        pre_sign = chem[:index]
        post_include_sign = chem[index:]
        print(post_include_sign)
        post_include_sign = post_include_sign.replace("+", "\u207A")
        post_include_sign = post_include_sign.replace("-", "\u207B")
        post_include_sign = post_include_sign.replace("0", "\u2070")
        post_include_sign = post_include_sign.replace("1", "\u00B9")
        post_include_sign = post_include_sign.replace("2", "\u00B2")
        post_include_sign = post_include_sign.replace("3", "\u00B3")
        post_include_sign = post_include_sign.replace("4", "\u2074")
        post_include_sign = post_include_sign.replace("5", "\u2075")
        post_include_sign = post_include_sign.replace("6", "\u2076")
        post_include_sign = post_include_sign.replace("7", "\u2077")
        post_include_sign = post_include_sign.replace("8", "\u2078")
        post_include_sign = post_include_sign.replace("9", "\u2079")
        chem = pre_sign + post_include_sign
    chem = chem.replace("0", "\u2080")
    chem = chem.replace("1", "\u2081")
    chem = chem.replace("2", "\u2082")
    chem = chem.replace("3", "\u2083")
    chem = chem.replace("4", "\u2084")
    chem = chem.replace("5", "\u2085")
    chem = chem.replace("6", "\u2086")
    chem = chem.replace("7", "\u2087")
    chem = chem.replace("8", "\u2088")
    chem = chem.replace("9", "\u2089")
    if amount == 1:
        return chem
    return f"{amount}{chem}"


def convert_shifted(string):
    return (string.replace("=", "0").replace("!", "1").replace('"', "2").replace("#", "3").replace("¤", "4")
            .replace("%", "5").replace("&", "6").replace("/", "7").replace("(", "8").replace(")", "9"))


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
        elif c.isalpha():
            if c.isupper():
                splits.append(ind)
                last_type = 1
            else:
                continue
        else:  # Assume c is a special character. I.e. "-" or "+"
            splits.append(ind)
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
        self.charge = 0

        self.molarmass = 0
        self.chemical = chemical
        self.components = {}

        if chemical != "":
            self.update()

    def is_fully_defined(self):
        return self.chemical and self.mass != -1 and self.molarmass != 0 and self.mol != -1

    def is_completely_undefined(self):
        return (not self.chemical) and self.mass == -1 and self.molarmass == 0 and self.mol == -1

    def gather_components(self):
        self.components = {}
        if self.chemical == "":
            return
        last_split = ""
        l_double = False
        self.amount = 1
        self.charge = 0
        for i in split_chemical_in_parts(self.chemical):
            if isinstance(i, int):
                if last_split == "":
                    self.amount = i
                elif last_split == "+":
                    self.charge += i - 1  # Minus one beacuse an initial charge was given by the "+" itself
                elif last_split == "-":
                    self.charge -= i - 1  # Minus one beacuse an initial charge was given by the "-" itself
                elif self.components[last_split] == 1:
                    self.components[last_split] = i
                elif l_double:
                    self.components[last_split] += i - 1
                    l_double = False
                else:
                    self.components[last_split] += i
                continue
            if i == "+":
                last_split = i
                self.charge += 1
            elif i == "-":
                last_split = i
                self.charge -= 1
            elif i not in self.components:
                self.components[i] = 1
            else:
                self.components[i] += 1
                l_double = True
            last_split = i

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

    def reset(self):
        self.chemical = ""
        self.mass = -1
        self.molarmass = 0
        self.mol = -1
        self.components = {}

    def update(self):
        self.gather_components()
        self.calculate_molarmass()
        self.try_calculate_mass_or_mol()

    def get_SimpleGUI_objects(self):
        return sg.Input(chem_to_visual(self.chemical), size=(BASE_LEN, 1), k=self.key, font=chemfont, enable_events=True),\
               sg.Input(f"{self.get_mass_string()}", size=(MONO_LEN, 1), k=f"{self.key}m"),\
               sg.T(f"{self.get_molarmass_string()}", size=(MONO_LEN, 1), k=f"{self.key}M"),\
               sg.Input(f"{self.get_mol_string()}", size=(MONO_LEN, 1), k=f"{self.key}n")


reactants = []
products = []


class Window:
    def __init__(self, reactants=[], products=[]):
        self.reactants = reactants
        self.products = products

        self.reactants += [Molecule(key=len(self.reactants)+i) for i in range(max(0, 3 - len(self.reactants)))]
        self.products += [Molecule(key=len(self.reactants)+i) for i in range(max(0, 3 - len(self.products)))]

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
        for r in self.reactants:
            if r.is_completely_undefined():
                r.chemical = chemical
                r.update()
                self.write_molecules()
                return
        self.reactants.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()

    def add_product(self, chemical=""):
        for p in self.products:
            if p.is_completely_undefined():
                p.chemical = chemical
                p.update()
                self.write_molecules()
                return
        self.products.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()

    def redo_layout(self):
        self.redefine_raw_layout()
        self.update_layout()

    def redefine_raw_layout(self):
        self.raw_layout = [[None, sg.T("", k="MissingReactants", size=(16, 1)), sg.Input("", k="ReactantInput", size=(16, 1), background_color=input_background_color), sg.T("Reactants", enable_events=True, k="addReactant"), sg.Text("|"), sg.T("Products", enable_events=True, k="addProduct"), sg.Input("", k="ProductInput", size=(16, 1), background_color=input_background_color), sg.T("", k="MissingProducts", size=(16, 1))],
                           [sg.T("Molecules:", font=mono), None, None, None, sg.Text("->"), None, None, None],
                           [sg.T("m (g)    :", font=mono), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("M (g/mol):", font=mono), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("n (mol)  :", font=mono), None, None, None, sg.Text("|"), None, None, None]]
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
                    p.try_calculate_mass_or_mol()
                break
        self.write_molecules()

    def write_molecules(self):
        for r in self.reactants + self.products:
            self.win[r.key](value=chem_to_visual(r.chemical))
            self.win[f"{r.key}m"](value=r.get_mass_string())
            self.win[f"{r.key}M"](value=r.get_molarmass_string())
            self.win[f"{r.key}n"](value=r.get_mol_string())

    def save_stuff(self):
        try:
            for r in self.reactants + self.products:
                if CONVERT_SHIFTED:
                    r.chemical = visual_to_chem(convert_shifted(self.values[r.key]))
                else:
                    r.chemical = visual_to_chem(self.values[r.key])
                r.mass = float(self.values[f"{r.key}m"]) if self.values[f"{r.key}m"] else -1
                r.mol = float(self.values[f"{r.key}n"]) if self.values[f"{r.key}n"] else -1
                r.update()
        except ValueError:  # if input field doesn't contain number
            pass

    def reset_amounts(self):
        for r in self.reactants + self.products:
            r.mass = -1
            r.mol = -1
        self.write_molecules()

    def calculate_mass_diff(self):
        return round(sum([0 if r.is_completely_undefined() else r.mass for r in self.reactants])
                     - sum([0 if p.is_completely_undefined() else p.mass for p in self.products]), 9)

    def calculate_reactants_mass(self):
        return round(sum([0 if r.is_completely_undefined() else r.mass for r in self.reactants]), 10)

    def mass_defined(self):
        one_defined = False
        for r in self.reactants + self.products:
            if r.is_completely_undefined():
                continue
            one_defined = True
        if one_defined:
            return sum([r.mass == -1 and not r.is_completely_undefined() for r in self.reactants + self.products]) == 0
        return False

    def append_atom_reactant(self, atom):
        if len(self.reactants) == 0:
            self.add_reactant(atom)
            return

        if atom in self.reactants[-1].components:
            self.reactants[-1].components[atom] += 1
        else:
            self.reactants[-1].components[atom] = 1
        self.reactants[-1].redefine_chemical_string()
        self.reactants[-1].update()
        self.write_molecules()

    def append_atom_product(self, atom):
        if len(self.products) == 0:
            self.add_product(atom)
            return

        if atom in self.products[-1].components:
            self.products[-1].components[atom] += 1
        else:
            self.products[-1].components[atom] = 1
        self.products[-1].redefine_chemical_string()
        self.products[-1].update()
        self.write_molecules()

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
        global USE_SUBSCRIPT
        global CONVERT_SHIFTED
        while not self.should_exit:
            event, self.values = self.win.read(timeout=200)
            if event == sg.WIN_CLOSED:
                break

            elif event != "__TIMEOUT__":
                print(event)

            if self.check_balanced():
                self.win["BALANCED"].update(text_color=active_color)
            else:
                self.win["BALANCED"].update(text_color=disabled_color)

            if self.mass_defined():
                m_diff = self.calculate_mass_diff()
                self.win["MassDiff"](value=m_diff if m_diff != 0 else "< 1e-9")
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
            elif isinstance(event, int):
                self.write_molecules()
            elif event == "addReactant":
                self.add_reactant()
            elif event == "addProduct":
                self.add_product()
            elif event == "Update":
                self.update_molecules()
            elif event == "Switch":
                r = self.reactants[:]
                p = self.products[:]
                self.reactants = p
                self.products = r
                if len(self.reactants) != len(self.products):
                    self.restart()
                    break
                for ind, r in enumerate(self.reactants):
                    k = r.key
                    r.key = self.products[ind].key
                    self.products[ind].key = k
                self.write_molecules()
            elif event == "Reset":
                if len(self.reactants) > DEFAULT_MOLECULE_AMOUNT or len(self.products) > DEFAULT_MOLECULE_AMOUNT:
                    self.reactants.clear()
                    self.products.clear()
                    self.restart()
                    break
                for r in self.reactants + self.products:
                    r.reset()
                self.write_molecules()
            elif event == "ResetAmounts":
                self.reset_amounts()
            elif event == "Restart":
                self.restart()
                break
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
            elif event == "Reset balance":
                for r in self.reactants + self.products:
                    r.amount = 1
                    r.redefine_chemical_string()
                self.write_molecules()
            elif event == "Subscript":
                self.save_stuff()
                USE_SUBSCRIPT = not USE_SUBSCRIPT
                self.win["Subscript"].update(text_color=active_color if USE_SUBSCRIPT else disabled_color)
                self.write_molecules()
            elif event == "ShiftConvert":
                CONVERT_SHIFTED = not CONVERT_SHIFTED
                self.win["ShiftConvert"].update(text_color=active_color if CONVERT_SHIFTED else disabled_color)
                self.save_stuff()
                self.write_molecules()
            elif event[:10] == "rmolecule:":
                chem = event[10:]
                self.add_reactant(chem)
            elif event[:10] == "pmolecule:":
                chem = event[10:]
                self.add_product(chem)
            elif event[:6] == "ratom:":
                self.append_atom_reactant(event[6:])
            elif event[:6] == "patom:":
                self.append_atom_product(event[6:])

        self.win.close()

    def update_layout(self):
        main_button_panel = [[sg.B("Update", font=small_font, k="Update"), sg.B("Switch", font=small_font),
                              sg.T("BALANCED", font=small_font, k="BALANCED")],
                             [sg.B("Reset", font=small_font), sg.B("ResetAmounts", font=small_font),
                              sg.B("Restart", font=small_font)]]
        data_panel = [[sg.T("Mass diff (r-p): ", font=small_font), sg.T("0." + "0"*12, k="MassDiff", font=small_font),
                       sg.T("|", font=small_font), sg.T("Mass (r): ", font=small_font), sg.T("0." + "0"*12, k="RMass",
                                                                                             font=small_font)],
                      ]
        secondary_button_panel = [[sg.B("Double", font=small_font), sg.B("Auto-balance", font=small_font)],
                                  [sg.B("Half", font=small_font), sg.B("Reset balance", font=small_font)]]

        tertiary_button_panel = [[sg.T("Subscript", k="Subscript",
                                       text_color=active_color if USE_SUBSCRIPT else disabled_color,
                                       font=small_font, enable_events=True)],
                                 [sg.T("Shift Convert", k="ShiftConvert",
                                       text_color=active_color if USE_SUBSCRIPT else disabled_color,
                                       font=small_font, enable_events=True)]]

        layout_prefix = [[sg.Col(main_button_panel), sg.Col(data_panel), sg.Col(secondary_button_panel),
                          sg.Col(tertiary_button_panel)]]

        mol_tuple = ()
        if USE_MOLECULE_ADD:
            mol_tuple = (("O2", "CO2", "H2O", "N2"),
                         ("CH4", "C2H6", "C3H8", "C4H10", "C5H12", "C6H14", "C7H16", "C8H18", "C9H20", "C10H22"),
                         ("CH3OH", "CH3CH2OH", "CH3CH2CH2OH"))

        atom_tuple = ()
        if USE_ATOM_ADD:
            atom_tuple = (("H", "He"),
                          ("Li", "Be", "B", "C", "N", "O", "F", "Ne"),
                          ("Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"),
                          ("K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
                           "Se", "Br", "Kr"),
                          ("Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
                           "Te", "I", "Xe"),
                          ("Cs", "Ba", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po",
                           "At", "Rn"),
                          ("Fr", "Ra", "Rf", "Db", "Sg", "Bh", "Hs"))

        r_add = [[sg.B(chem_to_visual(n), k=f"rmolecule:{n}", font=small_chem) for n in i] for i in mol_tuple]
        p_add = [[sg.B(chem_to_visual(n), k=f"pmolecule:{n}", font=small_chem) for n in i] for i in mol_tuple]

        ar_add = [[sg.B(n, k=f"ratom:{n}", font=small_font) for n in i] for i in atom_tuple]
        ap_add = [[sg.B(n, k=f"patom:{n}", font=small_font) for n in i] for i in atom_tuple]

        layout_suffix = [[sg.Col([[sg.Col(r_add, justification="l", expand_x=True), sg.Col(p_add, justification="r",
                                                                                           element_justification="r")]],
                                 expand_x=True, expand_y=True)],
                         [sg.Col([[sg.Col(ar_add, justification="l", expand_x=True),
                                   sg.Col([[sg.T("|")] for _ in atom_tuple], expand_x=True),
                                   sg.Col(ap_add, justification="r", element_justification="r")]],
                                 expand_x=True, expand_y=True)]]

        self.layout = [[]]
        for i in range(len(self.raw_layout[0])):
            self.layout[0] += [sg.Col([[sg.Text() if n[i] is None else n[i]] for n in self.raw_layout],
                                      element_justification="c")]
        self.layout = layout_prefix + self.layout + layout_suffix


while continue_program:
    continue_program = False
    Window(reactants, products)
