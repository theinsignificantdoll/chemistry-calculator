import PySimpleGUI as sg
from decimal import *
import time
import copy
import math

MODE = 1
#        Changes the look and feel of the program;
#          - -1 for true default
#          - 0 for Dark mode
#          - 1 for Light mode
#          - 2 for Light and dark blue
#          - 3 for Light and blue
#          - 4 for Light Grey mode
#          - 5 for Light+ mode
#          - 6 for Light mode 5
#          - 7 for Light mode 6
#          - 8 for Blue mode 3
#          - 9 for Dark blue mode 3
#          - 10 for light and red

# Default values, not necessarily used in any given visual mode
disabled_color = "#B0BABA"
active_color = "#5450c7"
field_active_color = "#c6b388"
input_background_color = "#B0BABA"
titlebar_background_color = "#212121"
user_defined_color = active_color
FORCE_NO_BORDERS = False
PREC = 100  # default 28

chars = {
    "DELTA": "\u0394",
    "delta": "\u03B4",
    "micro": "\u00B5",
    "^+": "\u207A",
    "^-": "\u207B",
    "^0": "\u2080",
    "^1": "\u2081",
    "^2": "\u2082",
    "^3": "\u2083",
    "^4": "\u2084",
    "^5": "\u2085",
    "^6": "\u2086",
    "^7": "\u2087",
    "^8": "\u2088",
    "^9": "\u2089",
}

if MODE == 0:
    sg.theme("DarkBrown4")
    # sg.theme_text_color("#c73530")
    # sg.theme_text_color("#9eb6c5")
    sg.theme_text_color("#f82222")
    sg.theme_border_width(0)
    sg.theme_input_background_color("#2b2b2b")
    sg.theme_input_text_color("#c75450")
    sg.theme_button_color((sg.theme_text_color(), sg.theme_background_color()))
    sg.theme_slider_color(sg.theme_background_color())
    # active_color = "#499c54"
    active_color = "#c75450"
elif MODE == 1:
    sg.theme("LightBrown3")
elif MODE == 2:
    sg.theme("Tan")
elif MODE == 3:
    sg.theme("TanBlue")
elif MODE == 4:
    sg.theme("LightGrey2")
elif MODE == 5:
    sg.theme("GrayGrayGray")
    sg.theme_input_background_color("#FFFFFF")
    # noinspection PyRedeclaration
    field_active_color = "#e0e0e0"
elif MODE == 6:
    sg.theme("Default1")
    sg.theme_input_background_color("#FFFFFF")
elif MODE == 7:
    sg.theme("DefaultNoMoreNagging")
    sg.theme_input_background_color("#FFFFFF")
    # noinspection PyRedeclaration
    field_active_color = "#e0e0e0"
elif MODE == 8:
    sg.theme("Python")
elif MODE == 9:
    sg.theme("PythonPlus")
elif MODE == 10:
    sg.theme("LightBrown13")

if FORCE_NO_BORDERS:
    sg.theme_border_width(0)
    sg.theme_progress_bar_border_width(0)
    sg.theme_slider_border_width(0)


class Unit:
    def __init__(self, multiplier: Decimal, suffix: str, name: str = None):
        self.multiplier = multiplier  # f.x. 1000 for kilograms
        self.suffix = suffix  # f.x. g for gram
        if name is None:
            self.name = suffix
        else:
            self.name = name


SCROLLABLE = None  # if None, SCROLLABLE will automatically be set to True, when the window size is increased
#                    if True, Scrollbars will always appear (and won't go away unless manually turned off)
#                    if False, Scrollbars will not be shown (and won't be automatically enabled)
BALANCE_WARN_TIME = 5  # Given in seconds
DEFAULT_MOLECULE_AMOUNT = 3
USE_CUSTOM_TITLEBAR = False
CONVERT_SHIFTED = False
USE_SUBSCRIPT = True
USE_MOLECULE_ADD = True
USE_ATOM_ADD = True
ATOM_ADD_ELEMENTANALYZER_BUTTON = False  # if None then the button will not be drawn. If True, the button will
#                                         be made with a default state of ON. If false default value is OFF
#                                         Will also be made meaningless if USE_ATOM_ADD == False
ATOM_ADD_ALIGN = True  # Aligns the atom add buttons, making them look more like the periodic table
#                         Also forcefully sets SHOW_ATOM_ADD_GROUPS to False
SHOW_ATOM_ADD_GROUPS = True
FORCE_MONO = True  # Chemical font is unaffected if USE_SUBSCRIPT
CONSTANT_MOL_OVER_VOLUME = "L"
#  Whether [default] mol/L should change to mol/mL,
#   when volume unit is changed [in this case to mL]. If it should not change
#   the variable should be set to the string of the suffix of the preferred volume unit

fontsize = 14
BASE_LEN = 15
MONO_LEN = 16
if not FORCE_MONO:
    MONO_LEN = BASE_LEN
ROUND_TO_DIGITS = 6
ROUND_TO_DIGITS_LONG = 9
ROUND_TO_DIGITS_MAX = 16
ALWAYS_SHOW_DIGITS_LEFT_OF_DOT = True
SHOULD_CLAMP = True
E_MIN = -999999  # defualt -999999
E_MAX = 999999  # default 999999
CAPITAL_E = True
STRIP_TRAILING_ZEROS = True
small_font_subtraction = 4
units = (
    Unit(Decimal(10 ** -12), "pg", "picograms"),
    Unit(Decimal(10 ** -9), "ng", "nanograms"),
    Unit(Decimal(10 ** -6), f"{chars['micro']}g", "micrograms"),
    Unit(Decimal(10 ** -3), "mg", "milligrams"),
    Unit(Decimal(1), "g", "grams"),
    Unit(Decimal(10 ** 3), "kg", "kilograms"),
    Unit(Decimal(10 ** 6), "t", "tons / megagrams"),
)
initial_unit = "g"  # Should be equal to the suffix of the unit that should initially be used.
vol_units = (
    Unit(Decimal(0.001), f"{chars['micro']}L", "microliters"),
    Unit(Decimal(1), "mL", "milliliters"),
    Unit(Decimal(1000), "L", "liters"),
)
initial_vol_unit = "L"
fonttype = "DejaVu Sans"
chemtype = "DejaVu Sans"
monotype = "DejaVu Sans Mono"

ELECTRON_VISUAL = "e\u207B"

#   FONTS THAT I HAVE EXPERIMENTED WITH
#   DejaVu Sans (Mono)
#   Gadugi
#   Lucida Sans Unicode / Lucida Console
#   Noto Sans / Noto Mono / Noto Serif
#   Rubik
#   Sylfaen
#   Tahoma
#   Verdana


tooltips = {
    "MissingMenu:Percentage": "The percentage of missing mass made"
                              "\n up of the specific atom",
    "MissingMenu:Mass": "The amount of missing mass made up of"
                        "\n the specific atom."
                        "\nAtomic Weight of atom * amount of atoms",
    "MissingMenu:TotalUnits": "The amount of mass missing from this side of the arrow",
    "MissingMenu:TotalUnitsIncl": "The total amount of expected mass on this side of the arrow"
                                  "\n(Which just means the amount of mass on the other side of the arrow)",
    "MissingMenu:PercentageMissing": "The percentage of mass which is missing on this side of the arrow"
                                     "\nin comparison to the total amount of expected mass",
    "MissingMenu:PercentagePresent": "The percentage of mass which is present on this side of the arrow"
                                     "\nin comparison to the amount of expected mass"
}


class Atom:
    def __init__(self, atomic_weight: Decimal = 0, shorthand: str = "None", name: str = None,
                 electron_shell: tuple = (0,), atomic_num: int = 0, electronegativity: Decimal = 0,
                 main_group: int = None, group: int = None):
        self.atomic_weight = atomic_weight
        self.shorthand = shorthand
        self.name = shorthand if name is None else name
        self.electron_shell = electron_shell
        self.atomic_num = atomic_num
        self.electronegativity = electronegativity
        self.main_group = main_group
        self.group = group
        if main_group is not None and group is None:
            self.group = main_group if self.main_group <= 2 else self.main_group + 10
        elif main_group is None and group is not None and (group <= 2 or group >= 13):
            self.main_group = self.group if self.group <= 2 else self.group - 10

    def get_electron_shell_string(self):
        return ", ".join([str(i) for i in self.electron_shell])

    def __repr__(self):
        return self.atomic_weight

    def __str__(self):
        return f"{self.shorthand} {self.atomic_weight} {self.name}"


setcontext(Context(clamp=1 if SHOULD_CLAMP else 0, Emin=E_MIN, Emax=E_MAX, capitals=1 if CAPITAL_E else 0, prec=PREC))

#  List of all atoms in the periodic system
atom_list = [
    Atom(shorthand="H", atomic_weight=Decimal("1.00794"), name="Hydrogen",
         electron_shell=(1,), atomic_num=1, electronegativity=Decimal("2.20"),
         main_group=1),

    Atom(shorthand="He", atomic_weight=Decimal("4.0026"), name="Helium",
         electron_shell=(2,), atomic_num=2, electronegativity=Decimal("0"),
         main_group=8),

    Atom(shorthand="Li", atomic_weight=Decimal("6.941"), name="Lithium",
         electron_shell=(2, 1), atomic_num=3, electronegativity=Decimal("0.98"),
         main_group=1),

    Atom(shorthand="Be", atomic_weight=Decimal("9.01218"), name="Beryllium",
         electron_shell=(2, 2), atomic_num=4, electronegativity=Decimal("1.57"),
         main_group=2),

    Atom(shorthand="B", atomic_weight=Decimal("10.811"), name="Boron",
         electron_shell=(2, 3), atomic_num=5, electronegativity=Decimal("2.04"),
         main_group=3),

    Atom(shorthand="C", atomic_weight=Decimal("12.011"), name="Carbon",
         electron_shell=(2, 4), atomic_num=6, electronegativity=Decimal("2.55"),
         main_group=4),

    Atom(shorthand="N", atomic_weight=Decimal("14.00674"), name="Nitrogen",
         electron_shell=(2, 5), atomic_num=7, electronegativity=Decimal("3.04"),
         main_group=5),

    Atom(shorthand="O", atomic_weight=Decimal("15.9994"), name="Oxygen",
         electron_shell=(2, 6), atomic_num=8, electronegativity=Decimal("3.44"),
         main_group=6),

    Atom(shorthand="F", atomic_weight=Decimal("18.9984"), name="Fluor",
         electron_shell=(2, 7), atomic_num=9, electronegativity=Decimal("3.98"),
         main_group=7),

    Atom(shorthand="Ne", atomic_weight=Decimal("20.1797"), name="Neon",
         electron_shell=(2, 8), atomic_num=10, electronegativity=Decimal("0"),
         main_group=8),

    Atom(shorthand="Na", atomic_weight=Decimal("22.98977"), name="Natrium",
         electron_shell=(2, 8, 1), atomic_num=11, electronegativity=Decimal("0.93"),
         main_group=1),

    Atom(shorthand="Mg", atomic_weight=Decimal("24.305"), name="Magnesium",
         electron_shell=(2, 8, 2), atomic_num=12, electronegativity=Decimal("1.31"),
         main_group=2),

    Atom(shorthand="Al", atomic_weight=Decimal("26.98154"), name="Aluminium",
         electron_shell=(2, 8, 3), atomic_num=13, electronegativity=Decimal("1.61"),
         main_group=3),

    Atom(shorthand="Si", atomic_weight=Decimal("28.0855"), name="Silicone",
         electron_shell=(2, 8, 4), atomic_num=14, electronegativity=Decimal("1.90"),
         main_group=4),

    Atom(shorthand="P", atomic_weight=Decimal("30.97376"), name="Phosphor",
         electron_shell=(2, 8, 5), atomic_num=15, electronegativity=Decimal("2.19"),
         main_group=5),

    Atom(shorthand="S", atomic_weight=Decimal("32.066"), name="Sulfur",
         electron_shell=(2, 8, 6), atomic_num=16, electronegativity=Decimal("2.58"),
         main_group=6),

    Atom(shorthand="Cl", atomic_weight=Decimal("35.4527"), name="Chlor",
         electron_shell=(2, 8, 7), atomic_num=17, electronegativity=Decimal("3.16"),
         main_group=7),

    Atom(shorthand="Ar", atomic_weight=Decimal("39.948"), name="Argon",
         electron_shell=(2, 8, 8), atomic_num=18, electronegativity=Decimal("0"),
         main_group=8),

    Atom(shorthand="K", atomic_weight=Decimal("39.0983"), name="Potassium",
         electron_shell=(2, 8, 8, 1), atomic_num=19, electronegativity=Decimal("0.82"),
         main_group=1),

    Atom(shorthand="Ca", atomic_weight=Decimal("40.078"), name="Calcium",
         electron_shell=(2, 8, 8, 2), atomic_num=20, electronegativity=Decimal("1.0"),
         main_group=2),

    Atom(shorthand="Sc", atomic_weight=Decimal("44.95591"), name="Scandium", electron_shell=(2, 8, 9, 2), atomic_num=21,
         electronegativity=Decimal("1.36"), group=3),

    Atom(shorthand="Ti", atomic_weight=Decimal("47.867"), name="Titanium", electron_shell=(2, 8, 10, 2), atomic_num=22,
         electronegativity=Decimal("1.54"), group=4),

    Atom(shorthand="V", atomic_weight=Decimal("50.9415"), name="Vanadium", electron_shell=(2, 8, 11, 2), atomic_num=23,
         electronegativity=Decimal("1.63"), group=5),

    Atom(shorthand="Cr", atomic_weight=Decimal("51.9961"), name="Chromium", electron_shell=(2, 8, 13, 1), atomic_num=24,
         electronegativity=Decimal("1.66"), group=6),

    Atom(shorthand="Mn", atomic_weight=Decimal("54.93805"), name="Manganese", electron_shell=(2, 8, 13, 2),
         atomic_num=25, electronegativity=Decimal("1.55"), group=7),

    Atom(shorthand="Fe", atomic_weight=Decimal("55.845"), name="Iron", electron_shell=(2, 8, 14, 2), atomic_num=26,
         electronegativity=Decimal("1.83"), group=8),

    Atom(shorthand="Co", atomic_weight=Decimal("58.93320"), name="Cobalt", electron_shell=(2, 8, 15, 2), atomic_num=27,
         electronegativity=Decimal("1.88"), group=9),

    Atom(shorthand="Ni", atomic_weight=Decimal("58.6934"), name="Nickel", electron_shell=(2, 8, 16, 2), atomic_num=28,
         electronegativity=Decimal("1.91"), group=10),

    Atom(shorthand="Cu", atomic_weight=Decimal("63.546"), name="Copper", electron_shell=(2, 8, 18, 1), atomic_num=29,
         electronegativity=Decimal("1.9"), group=11),

    Atom(shorthand="Zn", atomic_weight=Decimal("65.39"), name="Zinc", electron_shell=(2, 8, 18, 2), atomic_num=30,
         electronegativity=Decimal("1.65"), group=12),

    Atom(shorthand="Ga", atomic_weight=Decimal("69.723"), name="Gallium",
         electron_shell=(2, 8, 18, 3), atomic_num=31, electronegativity=Decimal("1.81"),
         main_group=3),

    Atom(shorthand="Ge", atomic_weight=Decimal("72.61"), name="Germanium",
         electron_shell=(2, 8, 18, 4), atomic_num=32, electronegativity=Decimal("2.01"),
         main_group=4),

    Atom(shorthand="As", atomic_weight=Decimal("74.92159"), name="Arsenic",
         electron_shell=(2, 8, 18, 5), atomic_num=33, electronegativity=Decimal("2.18"),
         main_group=5),

    Atom(shorthand="Se", atomic_weight=Decimal("78.96"), name="Selenium",
         electron_shell=(2, 8, 18, 6), atomic_num=34, electronegativity=Decimal("2.55"),
         main_group=6),

    Atom(shorthand="Br", atomic_weight=Decimal("79.904"), name="Bromine",
         electron_shell=(2, 8, 18, 7), atomic_num=35, electronegativity=Decimal("2.96"),
         main_group=7),

    Atom(shorthand="Kr", atomic_weight=Decimal("83.798"), name="Krypton",
         electron_shell=(2, 8, 18, 8), atomic_num=36, electronegativity=Decimal("3.0"),
         main_group=8),

    Atom(shorthand="Rb", atomic_weight=Decimal("85.4678"), name="Rubidium",
         electron_shell=(2, 8, 18, 8, 1), atomic_num=37, electronegativity=Decimal("0.82"),
         main_group=1),

    Atom(shorthand="Sr", atomic_weight=Decimal("87.62"), name="Strontium",
         electron_shell=(2, 8, 18, 8, 2), atomic_num=38, electronegativity=Decimal("0.95"),
         main_group=2),

    Atom(shorthand="Y", atomic_weight=Decimal("88.90585"), name="Yttrium", electron_shell=(2, 8, 18, 9, 2),
         atomic_num=39, electronegativity=Decimal("1.22"), group=3),

    Atom(shorthand="Zr", atomic_weight=Decimal("91.224"), name="Zirconium", electron_shell=(2, 8, 18, 10, 2),
         atomic_num=40, electronegativity=Decimal("1.33"), group=4),

    Atom(shorthand="Nb", atomic_weight=Decimal("92.9064"), name="Niobium", electron_shell=(2, 8, 18, 12, 1),
         atomic_num=41, electronegativity=Decimal("1.6"), group=5),

    Atom(shorthand="Mo", atomic_weight=Decimal("95.94"), name="Molybdenum", electron_shell=(2, 8, 18, 13, 1),
         atomic_num=42, electronegativity=Decimal("2.16"), group=6),

    Atom(shorthand="Tc", atomic_weight=Decimal("98.0"), name="Technetium", electron_shell=(2, 8, 18, 13, 2),
         atomic_num=43, electronegativity=Decimal("1.9"), group=7),

    Atom(shorthand="Ru", atomic_weight=Decimal("101.07"), name="Ruthenium", electron_shell=(2, 8, 18, 15, 1),
         atomic_num=44, electronegativity=Decimal("2.2"), group=8),

    Atom(shorthand="Rh", atomic_weight=Decimal("102.9055"), name="Rhodium", electron_shell=(2, 8, 18, 16, 1),
         atomic_num=45, electronegativity=Decimal("2.28"), group=9),

    Atom(shorthand="Pd", atomic_weight=Decimal("106.42"), name="Palladium", electron_shell=(2, 8, 18, 18),
         atomic_num=46, electronegativity=Decimal("2.20"), group=10),

    Atom(shorthand="Ag", atomic_weight=Decimal("107.8682"), name="Silver", electron_shell=(2, 8, 18, 18, 1),
         atomic_num=47, electronegativity=Decimal("1.93"), group=11),

    Atom(shorthand="Cd", atomic_weight=Decimal("112.411"), name="Cadmium", electron_shell=(2, 8, 18, 18, 2),
         atomic_num=48, electronegativity=Decimal("1.69"), group=12),

    Atom(shorthand="In", atomic_weight=Decimal("114.818"), name="Indium",
         electron_shell=(2, 8, 18, 18, 3), atomic_num=49, electronegativity=Decimal("1.78"),
         main_group=3),

    Atom(shorthand="Sn", atomic_weight=Decimal("118.710"), name="Tin",
         electron_shell=(2, 8, 18, 18, 4), atomic_num=50, electronegativity=Decimal("1.96"),
         main_group=4),

    Atom(shorthand="Sb", atomic_weight=Decimal("121.760"), name="Antimony",
         electron_shell=(2, 8, 18, 18, 5), atomic_num=51, electronegativity=Decimal("2.05"),
         main_group=5),

    Atom(shorthand="Te", atomic_weight=Decimal("127.60"), name="Tellurium",
         electron_shell=(2, 8, 18, 18, 6), atomic_num=52, electronegativity=Decimal("2.1"),
         main_group=6),

    Atom(shorthand="I", atomic_weight=Decimal("126.90447"), name="Iodine",
         electron_shell=(2, 8, 18, 18, 7), atomic_num=53, electronegativity=Decimal("2.66"),
         main_group=7),

    Atom(shorthand="Xe", atomic_weight=Decimal("131.29"), name="Xenon",
         electron_shell=(2, 8, 18, 18, 8), atomic_num=54, electronegativity=Decimal("2.6"),
         main_group=8),

    Atom(shorthand="Cs", atomic_weight=Decimal("132.90543"), name="Caesium",
         electron_shell=(2, 8, 18, 18, 8, 1), atomic_num=55, electronegativity=Decimal("0.79"),
         main_group=1),

    Atom(shorthand="Ba", atomic_weight=Decimal("137.327"), name="Barium",
         electron_shell=(2, 8, 18, 18, 8, 2), atomic_num=56, electronegativity=Decimal("0.89"),
         main_group=2),

    Atom(shorthand="Lu", atomic_weight=Decimal("174.9668"), name="Lutetium", electron_shell=(2, 8, 18, 32, 9, 2),
         atomic_num=71, electronegativity=Decimal("1.27"), group=3),

    Atom(shorthand="Hf", atomic_weight=Decimal("178.49"), name="Hafnium", electron_shell=(2, 8, 18, 32, 10, 2),
         atomic_num=72, electronegativity=Decimal("1.3"), group=4),

    Atom(shorthand="Ta", atomic_weight=Decimal("180.9479"), name="Tantalum", electron_shell=(2, 8, 18, 32, 11, 2),
         atomic_num=73, electronegativity=Decimal("1.5"), group=5),

    Atom(shorthand="W", atomic_weight=Decimal("183.84"), name="Tungsten", electron_shell=(2, 8, 18, 32, 12, 2),
         atomic_num=74, electronegativity=Decimal("2.36"), group=6),

    Atom(shorthand="Re", atomic_weight=Decimal("186.207"), name="Rhenium", electron_shell=(2, 8, 18, 32, 13, 2),
         atomic_num=75, electronegativity=Decimal("1.9"), group=7),

    Atom(shorthand="Os", atomic_weight=Decimal("190.23"), name="Osmium", electron_shell=(2, 8, 18, 32, 14, 2),
         atomic_num=76, electronegativity=Decimal("2.2"), group=8),

    Atom(shorthand="Ir", atomic_weight=Decimal("192.217"), name="Iridium", electron_shell=(2, 8, 18, 32, 15, 2),
         atomic_num=77, electronegativity=Decimal("2.20"), group=9),

    Atom(shorthand="Pt", atomic_weight=Decimal("195.08"), name="Platinum", electron_shell=(2, 8, 18, 32, 17, 1),
         atomic_num=78, electronegativity=Decimal("2.28"), group=10),

    Atom(shorthand="Au", atomic_weight=Decimal("196.96654"), name="Gold", electron_shell=(2, 8, 18, 32, 18, 1),
         atomic_num=79, electronegativity=Decimal("2.54"), group=11),

    Atom(shorthand="Hg", atomic_weight=Decimal("200.59"), name="Mercury", electron_shell=(2, 8, 18, 32, 18, 2),
         atomic_num=80, electronegativity=Decimal("2.0"), group=12),

    Atom(shorthand="Tl", atomic_weight=Decimal("204.3833"), name="Thallium",
         electron_shell=(2, 8, 18, 32, 18, 3), atomic_num=81, electronegativity=Decimal("1.62"),
         main_group=3),

    Atom(shorthand="Pb", atomic_weight=Decimal("207.2"), name="Lead",
         electron_shell=(2, 8, 18, 32, 18, 4), atomic_num=82, electronegativity=Decimal("2.33"),
         main_group=4),

    Atom(shorthand="Bi", atomic_weight=Decimal("208.98037"), name="Bismuth",
         electron_shell=(2, 8, 18, 32, 18, 5), atomic_num=83, electronegativity=Decimal("2.02"),
         main_group=5),

    Atom(shorthand="Po", atomic_weight=Decimal("209.0"), name="Polonium",
         electron_shell=(2, 8, 18, 32, 18, 6), atomic_num=84, electronegativity=Decimal("2.0"),
         main_group=6),

    Atom(shorthand="At", atomic_weight=Decimal("210.0"), name="Astatine",
         electron_shell=(2, 8, 18, 32, 18, 7), atomic_num=85, electronegativity=Decimal("2.2"),
         main_group=7),

    Atom(shorthand="Rn", atomic_weight=Decimal("222.0"), name="Radon",
         electron_shell=(2, 8, 18, 32, 18, 8), atomic_num=86, electronegativity=Decimal("0"),
         main_group=8),

    Atom(shorthand="Fr", atomic_weight=Decimal("223.0"), name="Francium",
         electron_shell=(2, 8, 18, 32, 18, 8, 1), atomic_num=87, electronegativity=Decimal("0.7"),
         main_group=1),

    Atom(shorthand="Ra", atomic_weight=Decimal("226.0254"), name="Radium",
         electron_shell=(2, 8, 18, 32, 18, 8, 2), atomic_num=88, electronegativity=Decimal("0.9"),
         main_group=2),

    Atom(shorthand="Lr", atomic_weight=Decimal("266"), name="Lawrencium", electron_shell=(2, 8, 18, 32, 32, 8, 3),
         atomic_num=103, electronegativity=Decimal("0"), group=3),

    Atom(shorthand="Rf", atomic_weight=Decimal("261.0"), name="Rutherfordium", electron_shell=(2, 8, 18, 32, 32, 10, 2),
         atomic_num=104, electronegativity=Decimal("0"), group=4),

    Atom(shorthand="Db", atomic_weight=Decimal("262"), name="Dubnium", electron_shell=(2, 8, 18, 32, 32, 11, 2),
         atomic_num=105, electronegativity=Decimal("0"), group=5),

    Atom(shorthand="Sg", atomic_weight=Decimal("266"), name="Seaborgium", electron_shell=(2, 8, 18, 32, 32, 12, 2),
         atomic_num=106, electronegativity=Decimal("0"), group=6),

    Atom(shorthand="Bh", atomic_weight=Decimal("262"), name="Bohrium", electron_shell=(2, 8, 18, 32, 32, 13, 2),
         atomic_num=107, electronegativity=Decimal("0"), group=7),

    Atom(shorthand="Hs", atomic_weight=Decimal("265"), name="Hassium", electron_shell=(2, 8, 18, 32, 32, 14, 2),
         atomic_num=108, electronegativity=Decimal("0"), group=8),

]

#  Defines the atomic weight of atoms used in calculations
atom_dict = {}
atom_units = {ELECTRON_VISUAL: 0}
for n_outer in atom_list:
    atom_units[n_outer.shorthand] = n_outer.atomic_weight
    atom_dict[n_outer.shorthand] = n_outer

if FORCE_MONO:
    fonttype = monotype
if FORCE_MONO and not USE_SUBSCRIPT:
    chemtype = monotype
    BASE_LEN = MONO_LEN
small_font = (fonttype, fontsize - small_font_subtraction)
mono = (monotype, fontsize)
chemfont = (chemtype, fontsize)
small_chem = (chemtype, fontsize - small_font_subtraction)

current_unit = units[0]
if not ATOM_ADD_ALIGN:
    SHOW_ATOM_ADD_GROUPS = False
for n_outer in units:
    if n_outer.suffix == initial_unit:
        current_unit = n_outer
        break

current_vol_unit = vol_units[0]
for n_outer in vol_units:
    if n_outer.suffix == initial_vol_unit:
        current_vol_unit = n_outer
        break
mol_over_vol = Unit(Decimal(current_vol_unit.multiplier), f"mol/{current_vol_unit.suffix}")
if CONSTANT_MOL_OVER_VOLUME:
    for n_outer in vol_units:
        if CONSTANT_MOL_OVER_VOLUME == n_outer.suffix:
            mol_over_vol = Unit(n_outer.multiplier, f"mol/{CONSTANT_MOL_OVER_VOLUME}")
            break


def update_mol_over_vol():
    if CONSTANT_MOL_OVER_VOLUME:
        return
    global mol_over_vol
    mol_over_vol = Unit(current_vol_unit.multiplier, f"mol/{current_vol_unit.suffix}")


continue_program = True


def make_round(num: Decimal, digits: int = ROUND_TO_DIGITS):
    if not num:
        return num
    log = abs(num).log10()
    if log < 0:
        return Decimal(round(num, int(-1 * math.floor(log)) + digits - 1))
    out = round(num, max(int(digits - math.ceil(log)), 0) if ALWAYS_SHOW_DIGITS_LEFT_OF_DOT
                else int(digits - math.ceil(log)))
    if out % 1 == 0:
        return Decimal(int(out))
    return Decimal(out)


def decimal_to_string(num: Decimal, digits: int = ROUND_TO_DIGITS, rounding=True):
    if rounding:
        string = make_round(num, digits).__str__()
    else:
        string = num.__str__()
    if "." in string and STRIP_TRAILING_ZEROS:
        parts = string.split("E" if CAPITAL_E else "e")
        if len(parts) == 2:
            return parts[0].rstrip("0").rstrip(".") + ("E" if CAPITAL_E else "e") + parts[1]
        return string.rstrip("0").rstrip(".")
    return string


def chem_visual_amount_is_one(chem):
    if len(chem) < 2:
        return False
    return chem[0] == "1" and not chem[1].isdigit()


def chem_name_to_components(name):
    name = [m.split(",") for m in name.split("-")]
    for ind, i in enumerate(name):
        if i[0][0].isdigit():
            for ind2, i2 in enumerate(i):
                name[ind][ind2] = int(name[ind][ind2])
        else:
            name[ind] = name[ind][0]


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
    chem = (chem[len(a):].replace("\u2080", "0").replace("\u2081", "1").replace("\u2082", "2").replace("\u2083", "3")
            .replace("\u2084", "4").replace("\u2085", "5").replace("\u2086", "6").replace("\u2087", "7")
            .replace("\u2088", "8").replace("\u2089", "9").replace("\u207A", "+").replace("\u207B", "-")
            .replace("\u2070", "0").replace("\u00B9", "1").replace("\u00B2", "2").replace("\u00B3", "3")
            .replace("\u2074", "4").replace("\u2075", "5").replace("\u2076", "6").replace("\u2077", "7")
            .replace("\u2078", "8").replace("\u2079", "9"))
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
    if "+" in chem or "-" in chem:
        index_charge_start = 0
        for index, i in enumerate(chem):
            if i in ("+", "-"):
                index_charge_start = index
                break
        pre_charge = chem[:index_charge_start]
        post_charge = chem[index_charge_start:]
        post_charge = (post_charge.replace("+", "\u207A")
                       .replace("-", "\u207B").replace("0", "\u2070").replace("1", "\u00B9").replace("2", "\u00B2")
                       .replace("3", "\u00B3").replace("4", "\u2074").replace("5", "\u2075").replace("6", "\u2076")
                       .replace("7", "\u2077").replace("8", "\u2078").replace("9", "\u2079"))
        chem = pre_charge + post_charge
    chem = chem[len(a):].replace("0", "\u2080").replace("1", "\u2081").replace("2", "\u2082") \
        .replace("3", "\u2083").replace("4", "\u2084").replace("5", "\u2085").replace("6", "\u2086") \
        .replace("7", "\u2087").replace("8", "\u2088").replace("9", "\u2089")
    if amount == 1:
        return chem
    return f"{amount}{chem}"


def convert_shifted(string):
    return string.replace("=", "0").replace("!", "1").replace('"', "2").replace("#", "3").replace("¤", "4"). \
        replace("%", "5").replace("&", "6").replace("/", "7").replace("(", "8").replace(")", "9")


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
        elif c in ("+", "-"):
            splits.append(ind)
            last_type = 1
    if not splits:
        return []

    output = []
    for i in range(len(splits) - 1):
        if chemical[splits[i]].isdigit():
            output.append(int(chemical[splits[i]:splits[i + 1]]))
            continue
        output.append(chemical[splits[i]:splits[i + 1]])

    if chemical[splits[-1]].isdigit():
        output.append(int(chemical[splits[-1]:]))
    else:
        output.append(chemical[splits[-1]:])

    return output


def balance_reaction(reactants, products):
    start_time = time.time()
    states = [[reactants, products]]
    for r in states[0][0] + states[0][1]:
        r.amount = 1
    seen_missing_comb = []
    new_states = []
    already_warned = False

    while True:
        if time.time() - start_time > BALANCE_WARN_TIME and not already_warned:
            if sg.popup_yes_no(f"WARNING: Attempt to balance has taken\nmore than {BALANCE_WARN_TIME}s."
                               "\n\nCancel Auto-balance?", title="Auto-balancing warning") == "Yes":
                break
            already_warned = True
        seen_missing_comb.clear()
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
                        n.get_all_components()
                        if m in n.all_components:
                            new_r = r.copy()
                            new_r[ind] = copy.copy(n)
                            new_r[ind].amount += 1
                            new_states.append([new_r, p])
                continue
            elif p_missing:
                for m in p_missing:
                    for ind, n in enumerate(p):
                        n.get_all_components()
                        if m in n.all_components:
                            new_p = p.copy()
                            new_p[ind] = copy.copy(n)
                            new_p[ind].amount += 1
                            new_states.append([r, new_p])
                continue
            else:
                for m in r + p:
                    m.redefine_chemical_string()
                return r, p
        states = new_states.copy()
        new_states.clear()
    return reactants, products


def sum_charges(lst):
    return sum([i.charge * i.amount for i in lst])


def check_balanced(reactants, products):
    r_components = {}
    p_components = {}
    # The following two for loops could theoretically be replaced by add_dicts() and multiply_dict()
    #   However, letting everything be done in the same loop is probably faster. i think.
    for r in reactants:
        for n in r.get_all_components():
            if n in r_components:
                r_components[n] += r.all_components[n] * r.amount
                continue
            r_components[n] = r.all_components[n] * r.amount
    for p in products:
        for n in p.get_all_components():
            if n in p_components:
                p_components[n] += p.all_components[n] * p.amount
                continue
            p_components[n] = p.all_components[n] * p.amount

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

    r_charge = sum_charges(reactants)
    p_charge = sum_charges(products)
    if r_charge != p_charge:
        if r_charge < p_charge:
            p_missing[ELECTRON_VISUAL] = p_charge - r_charge
        else:
            r_missing[ELECTRON_VISUAL] = r_charge - p_charge

    return r_missing, p_missing


def count_atoms(chems):
    if not (isinstance(chems, list) or isinstance(chems, tuple)):
        chems = (chems,)
    counted = {}
    for n in chems:
        for i in n.get_all_components():
            if i in counted:
                counted[i] += n.all_components[i] * n.amount
                continue
            counted[i] = n.all_components[i] * n.amount
    return counted


def count_units(atoms: dict):
    out = 0
    for i in atoms:
        out += atoms[i] * atom_units[i]
    return out


def add_dicts(*dicts):
    if len(dicts) == 0:
        return 0
    out = dicts[0].copy()
    for n in dicts[1:]:
        for i in n:
            if i in out:
                out[i] += n[i]
                continue
            out[i] = n[i]
    return out


def multiply_dict(dict_1, multiplier):
    out = dict_1.copy()
    for i in out:
        out[i] *= multiplier
    return out


class Molecule:
    def __init__(self, chemical="", mass=-1, mol=-1, key=None):
        self.mass = mass
        self.mol = mol
        self.amount = 1
        self.key = key
        self.charge = 0
        self.mass_is_user_defined = None
        self.mol_is_user_defined = None
        #  None = undefined
        #  False = computer defined / calculated
        #  True = user_defined

        self.molarmass = 0
        self.chemical = chemical
        self.sub_chemicals = []
        self.components = {}
        self.all_components = {}

        if chemical != "":
            self.update()

    def set_chemical(self, new_chemical):
        if new_chemical == self.chemical:
            return False
        self.chemical = new_chemical
        self.gather_components()
        self.calculate_molarmass()
        self.recalculate_mol()
        return True

    def set_mass(self, new_mass):
        if new_mass == self.mass:
            return False
        self.mass = new_mass
        self.recalculate_mol()
        return True

    def set_mol(self, new_mol):
        if new_mol == self.mol:
            return False
        self.mol = new_mol
        self.recalculate_mass()
        return True

    def is_fully_defined(self):
        return self.chemical and self.mass != -1 and self.molarmass != 0 and self.mol != -1

    def is_completely_undefined(self):
        return (not self.chemical) and self.mass == -1 and self.molarmass == 0 and self.mol == -1

    def gather_components(self):
        self.components = {}
        self.sub_chemicals.clear()
        if self.chemical == "":
            return

        if "(" in self.chemical:
            chem_parts = []
            last_significant_ind = -1
            digit_reader = -2
            opened = False
            skip_levels = 0
            for ind, i in enumerate(self.chemical):
                if digit_reader == ind - 1 and i.isdigit():
                    digit_reader = ind
                    chem_parts[-1] = (chem_parts[-1][:ind - last_significant_ind - 1] + i
                                      + chem_parts[-1][ind - last_significant_ind - 1:])
                    last_significant_ind = ind
                if skip_levels != 0:
                    if i == "(":
                        skip_levels += 1
                    elif i == ")":
                        skip_levels -= 1
                elif not opened:
                    if i == "(" or ind + 1 == len(self.chemical):
                        opened = True
                        if len(chem_parts) != 0:
                            chem_parts[0] += self.chemical[last_significant_ind + 1:
                                                           ind if ind != len(self.chemical) - 1 else ind + 1].lstrip(
                                ")")
                        else:
                            chem_parts.append(self.chemical[last_significant_ind + 1:ind].lstrip(")"))
                        last_significant_ind = ind
                elif i == ")":
                    opened = False
                    chem_parts.append(self.chemical[last_significant_ind + 1:ind].lstrip("("))
                    digit_reader = ind
                    last_significant_ind = ind
                elif i == "(":
                    skip_levels += 1

            if len(chem_parts) > 1:
                self.sub_chemicals = [Molecule(i) for i in chem_parts[1:]]

            chem = chem_parts[0] if len(chem_parts) != 0 else self.chemical
        else:
            chem = self.chemical
        prev_char = ""
        prev_char_duplicate = False
        self.amount = 1
        self.charge = 0
        for i in split_chemical_in_parts(chem):
            if isinstance(i, int):
                if prev_char == "":
                    self.amount = i
                elif prev_char == "+":
                    self.charge += i
                elif prev_char == "-":
                    self.charge -= i
                elif self.components[prev_char] == 1:
                    self.components[prev_char] = i
                elif prev_char_duplicate:
                    self.components[prev_char] += i - 1
                    prev_char_duplicate = False
                else:
                    self.components[prev_char] += i
            elif i == "+":
                self.charge += 1
            elif i == "-":
                self.charge -= 1
            elif i not in self.components:
                self.components[i] = 1
            else:
                self.components[i] += 1
                prev_char_duplicate = True
            prev_char = i

    def get_all_components(self):
        self.all_components = add_dicts(self.components,
                                        *[multiply_dict(i.get_all_components(), i.amount)
                                          for i in self.sub_chemicals])
        return self.all_components

    def calculate_molarmass(self):
        self.molarmass = (sum([atom_units[n] * self.components[n] for n in self.components]) * (
                1 / current_unit.multiplier)) \
                         + sum([i.calculate_molarmass() * i.amount for i in self.sub_chemicals])
        return self.molarmass

    def get_molarmass_string(self):
        if self.molarmass == 0:
            return ""
        return decimal_to_string(Decimal(self.molarmass), ROUND_TO_DIGITS_LONG)

    def get_mass_string(self):
        if self.mass == -1:
            return ""
        return decimal_to_string(Decimal(self.mass), ROUND_TO_DIGITS_LONG)

    def get_mol_string(self):
        if self.mol == -1:
            return ""
        return decimal_to_string(Decimal(self.mol), ROUND_TO_DIGITS_LONG)

    def redefine_chemical_string(self):
        self.chemical = (f"{self.amount if self.amount != 1 else ''}" +
                         "".join([f"{i}{self.components[i] if self.components[i] != 1 else ''}"
                                  for i in self.components]) +
                         "".join([f"({i.chemical.lstrip(str(i.amount))}){i.amount}" for i in self.sub_chemicals]) +
                         (f"{'+' if self.charge > 0 else ''}{self.charge if abs(self.charge) > 1 else ''}"
                          if self.charge else ""))

    def try_calculate_mass_or_mol(self):
        if (self.mass == -1 and self.mol == -1) or not self.chemical:
            return
        elif self.mass != -1 and not self.mol_is_user_defined:
            self.mol = self.mass / self.molarmass
        elif self.mol != -1 and not self.mass_is_user_defined:
            self.mass = self.mol * self.molarmass

    def recalculate_mol(self):
        self.mol = -1
        self.try_calculate_mass_or_mol()

    def recalculate_mass(self):
        self.mass = -1
        self.try_calculate_mass_or_mol()

    def reset_amounts(self):
        if self.mass == -1 and self.mol == -1:
            return False
        self.mass = -1
        self.mol = -1
        return True

    def reset(self):
        self.chemical = ""
        self.reset_amounts()
        self.sub_chemicals.clear()
        self.molarmass = 0
        self.components = {}
        self.all_components = {}

    def update(self):
        self.gather_components()
        self.calculate_molarmass()
        self.try_calculate_mass_or_mol()

    def get_sg_objects(self):
        return sg.Input(chem_to_visual(self.chemical), size=(BASE_LEN, 1), k=self.key,
                        font=chemfont, enable_events=True), \
            sg.Input(f"{self.get_mass_string()}", size=(MONO_LEN, 1), k=f"{self.key}m",
                     enable_events=True,
                     text_color=user_defined_color if self.mass_is_user_defined else sg.theme_text_color()), \
            sg.T(f"{self.get_molarmass_string()}", size=(MONO_LEN, 1), k=f"{self.key}M"), \
            sg.Input(f"{self.get_mol_string()}", size=(MONO_LEN, 1), k=f"{self.key}n",
                     enable_events=True,
                     text_color=user_defined_color if self.mol_is_user_defined else sg.theme_text_color())


class ElementAnalyzer:
    def __init__(self, win_object, initial_element=None):
        self.obj = win_object
        self.empty_atom = Atom(Decimal(0), "", "", (0,))
        if initial_element is None:
            self.curr_element_as_atom: Atom = self.empty_atom
        elif isinstance(initial_element, Atom):
            self.curr_element_as_atom: Atom = initial_element
        else:  # Assume initial element is a shorthand
            self.curr_element_as_atom: Atom = atom_dict[initial_element]
        self.curr_element: str = self.curr_element_as_atom.shorthand
        self.mass: Decimal = Decimal(0)
        self.mol: Decimal = Decimal(0)
        self.values = {}
        self.compare_atom = self.empty_atom

        layout = [[sg.T("Atom:"), sg.In(self.curr_element_as_atom.name, k="-ELEMENT_NAME-", enable_events=True,
                                        s=(max([len(n.name) for n in atom_list]), 1)),
                   sg.In(self.curr_element, k="-ELEMENT_SHORTHAND-", enable_events=True, s=(MONO_LEN // 2, 1))],
                  [sg.Col([[sg.T("Atomic mass:"), sg.T(self.curr_element_as_atom.atomic_weight, k="-ATOMIC_MASS-")],
                           [sg.T("Atomic number:"), sg.T(self.curr_element_as_atom.atomic_num, k="-ATOMIC_NUM-")],
                           [sg.T("Main group:"), sg.T(self.curr_element_as_atom.main_group
                                                      if self.curr_element_as_atom.main_group is not None else "",
                                                      k="-MAIN_GROUP-")]]),
                   sg.VSep(),
                   sg.Col([[sg.T("Electron shell:"),
                            sg.T(self.curr_element_as_atom.get_electron_shell_string(), k="-ELECTRON_SHELL-")],
                           [sg.T("Electronegativity:"),
                            sg.T(self.curr_element_as_atom.electronegativity
                                 if self.curr_element_as_atom.electronegativity else "", k="-ELECTRO_NEGATIVITY-")],
                           [sg.T("Group:"), sg.T(self.curr_element_as_atom.group
                                                 if self.curr_element_as_atom.group is not None else "",
                                                 k="-GROUP-")]])],
                  [sg.HSep()],
                  [sg.Col([[sg.T(f"Mass ({current_unit.suffix}): "), sg.In(k="-MASS_FIELD-", enable_events=True,
                                                                           s=(MONO_LEN, 1))],
                           [sg.T("Mol: "), sg.In(k="-MOL_FIELD-", enable_events=True, s=(MONO_LEN, 1))]]),
                   sg.VSep(),
                   sg.Col([[sg.T("Compare:"), sg.In(k="-COMPARE_FIELD-", s=(MONO_LEN // 2, 1), enable_events=True)],
                           [sg.T(f"{chars['DELTA']}EN:"), sg.T(k="-DELTA_EN-"),
                            sg.VSep(), sg.T("EN:"),
                            sg.T(k="-COMPARE_EN-")],
                           [sg.T(f"{chars['delta']}{chars['^+']}:"), sg.T(k="-DELTA+-"),
                            sg.VSep(),
                            sg.T(f"{chars['delta']}{chars['^-']}:"), sg.T(k="-DELTA--")]])]]

        self.win = sg.Window("ElementAnalyzer", layout, font=(fonttype, fontsize), finalize=True)
        self.loop()

    def update_compare(self):
        if self.curr_element_as_atom.electronegativity == 0 or self.compare_atom.electronegativity == 0:
            self.win["-DELTA_EN-"](value="")
            self.win["-DELTA+-"](value="")
            self.win["-DELTA--"](value="")
            self.win["-COMPARE_EN-"](value="")
            return
        val = 0
        if self.compare_atom.electronegativity < self.curr_element_as_atom.electronegativity:
            self.win["-DELTA+-"](value=self.compare_atom.shorthand)
            self.win["-DELTA--"](value=self.curr_element_as_atom.shorthand)
            val = self.curr_element_as_atom.electronegativity - self.compare_atom.electronegativity
        elif self.compare_atom.electronegativity > self.curr_element_as_atom.electronegativity:
            self.win["-DELTA+-"](value=self.curr_element_as_atom.shorthand)
            self.win["-DELTA--"](value=self.compare_atom.shorthand)
            val = self.compare_atom.electronegativity - self.curr_element_as_atom.electronegativity
        else:
            self.win["-DELTA+-"](value="")
            self.win["-DELTA--"](value="")
        self.win["-COMPARE_EN-"](value=self.compare_atom.electronegativity)
        self.win["-DELTA_EN-"](value=val)

    def new_element_name(self):
        self.win["-ELEMENT_SHORTHAND-"](value=self.curr_element_as_atom.shorthand)
        self.win["-ATOMIC_MASS-"](value=self.curr_element_as_atom.atomic_weight)
        self.win["-MAIN_GROUP-"](value=self.curr_element_as_atom.main_group
                                 if self.curr_element_as_atom.main_group is not None else "")
        self.win["-ELECTRON_SHELL-"](value=self.curr_element_as_atom.get_electron_shell_string())
        self.win["-ATOMIC_NUM-"](value=self.curr_element_as_atom.atomic_num)
        self.win["-ELECTRO_NEGATIVITY-"](value=self.curr_element_as_atom.electronegativity
                                         if self.curr_element_as_atom.electronegativity else "")
        self.win["-GROUP-"](value=self.curr_element_as_atom.group
                            if self.curr_element_as_atom.group is not None else "")

    def new_element_shorthand(self):
        self.win["-ELEMENT_NAME-"](value=self.curr_element_as_atom.name)
        self.win["-ATOMIC_MASS-"](value=self.curr_element_as_atom.atomic_weight)
        self.win["-MAIN_GROUP-"](value=self.curr_element_as_atom.main_group
                                 if self.curr_element_as_atom.main_group is not None else "")
        self.win["-ELECTRON_SHELL-"](value=self.curr_element_as_atom.get_electron_shell_string())
        self.win["-ATOMIC_NUM-"](value=self.curr_element_as_atom.atomic_num)
        self.win["-ELECTRO_NEGATIVITY-"](value=self.curr_element_as_atom.electronegativity
                                         if self.curr_element_as_atom.electronegativity else "")
        self.win["-GROUP-"](value=self.curr_element_as_atom.group
                            if self.curr_element_as_atom.group is not None else "")

    def reset_mass_and_mol(self):
        self.reset_mol()
        self.reset_mass()

    def reset_mol(self):
        self.mol = 0
        self.win["-MOL_FIELD-"](value="")

    def calculate_mol(self):
        if self.curr_element_as_atom.atomic_weight == 0:
            self.reset_mol()
            return
        self.mol = self.mass / self.curr_element_as_atom.atomic_weight
        self.win["-MOL_FIELD-"](value=decimal_to_string(self.mol))

    def calculate_mass(self):
        if self.curr_element_as_atom.atomic_weight == 0:
            self.reset_mass()
            return
        self.mass = self.mol * self.curr_element_as_atom.atomic_weight / current_unit.multiplier
        self.win["-MASS_FIELD-"](value=decimal_to_string(self.mass))

    def reset_mass(self):
        self.mass = 0
        self.win["-MASS_FIELD-"](value="")

    def loop(self):
        while True:
            event, self.values = self.win.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "-ELEMENT_NAME-":
                key = self.values["-ELEMENT_NAME-"].lower()
                for i in atom_list:
                    if key == i.name.lower():
                        if self.curr_element_as_atom == i:
                            break
                        self.curr_element_as_atom = i
                        self.curr_element = self.curr_element_as_atom.shorthand
                        self.reset_mass_and_mol()
                        self.new_element_name()
                        break
                else:
                    self.curr_element_as_atom = self.empty_atom
                    self.curr_element = self.curr_element_as_atom.shorthand
                    self.new_element_name()
                    self.reset_mass_and_mol()
                    self.update_compare()
            elif event == "-ELEMENT_SHORTHAND-":
                key = self.values["-ELEMENT_SHORTHAND-"]
                for i in atom_list:
                    if key == i.shorthand:
                        if self.curr_element_as_atom == i:
                            break
                        self.curr_element_as_atom = i
                        self.curr_element = self.curr_element_as_atom.shorthand
                        self.reset_mass_and_mol()
                        self.new_element_shorthand()
                        break
                else:
                    self.curr_element_as_atom = self.empty_atom
                    self.curr_element = self.curr_element_as_atom.shorthand
                    self.reset_mass_and_mol()
                    self.new_element_shorthand()
                self.update_compare()
            elif event == "-MASS_FIELD-":
                try:
                    self.mass = Decimal(self.values["-MASS_FIELD-"]) * current_unit.multiplier
                    self.calculate_mol()
                except InvalidOperation:
                    self.reset_mol()
            elif event == "-MOL_FIELD-":
                try:
                    self.mol = Decimal(self.values["-MOL_FIELD-"])
                    self.calculate_mass()
                except InvalidOperation:
                    self.reset_mass()
            elif event == "-COMPARE_FIELD-":
                if self.curr_element_as_atom.electronegativity != 0:
                    try:
                        self.compare_atom = atom_dict[self.values["-COMPARE_FIELD-"]]
                        self.update_compare()
                    except KeyError:
                        self.compare_atom = self.empty_atom
                        self.update_compare()


class DissolvedWin:
    def __init__(self, side="Reactants", breakdown="Chemical", volume=0, mass=None, win_object=None, ratio=0):
        global current_vol_unit
        self.obj = win_object
        self.ratio = ratio
        self.rmass = 0
        self.mass = mass
        self.percentages = {}
        if self.mass is None:
            self.mass = self.obj.calculate_reactants_mass()
            self.mass = max(self.mass, 0)

        self.side = side
        self.breakdown = breakdown
        self.volume = volume
        self.total_units = 0
        top_settings = [
            [sg.Combo(values=("Reactants", "Products"), default_value=self.side, k="-R/P_CHEMICALS-",
                      enable_events=True),
             sg.Combo(values=[i.name for i in vol_units], default_value=current_vol_unit.name, k="-VOL_UNIT-",
                      enable_events=True, size=(max(*[len(i.name) for i in vol_units]), 1)),
             sg.Combo(values=("Atomic", "Chemical"), default_value=self.breakdown, k="-BREAKDOWN_TYPE-",
                      enable_events=True),
             sg.B("Transfer", pad=(0, 0), font=small_font)]]

        left_measurements = [[sg.T(f"Mass ({current_unit.suffix}):"),
                              sg.In(f"{decimal_to_string(self.mass)}",
                                    size=(MONO_LEN, 1), k="Mass_left", enable_events=True)],
                             [sg.T(f"Volume ({current_vol_unit.suffix}):", k="volString"),
                              sg.In(f"{volume}", size=(MONO_LEN, 1), k="VolumeField", enable_events=True)]]
        right_measurements = [[sg.T(f"Mass ({current_unit.suffix}):"),
                               sg.In(size=(MONO_LEN, 1), k="Mass_right", enable_events=True)],
                              [sg.T(f"Ratio:"), sg.In("0", size=(MONO_LEN, 1), k="Ratio", enable_events=True),
                               sg.T("         ", k="1overRatio")]]
        if breakdown == "Chemical":
            if side == "Reactants":
                self.side_vals = [i for i in self.obj.reactants if not i.is_completely_undefined()]
            else:
                self.side_vals = [i for i in self.obj.products if not i.is_completely_undefined()]

            left_vals_names = [[sg.T("Names")]] + [[sg.T(chem_to_visual(i.chemical),
                                                         font=chemfont)] for i in self.side_vals]
            left_vals_mass = [[sg.T(f"{current_unit.suffix}")]] + [[sg.T("0", k=f"{i.key}lm")] for i in self.side_vals]
            left_vals_molvolume = [[sg.T(f"mol/{current_vol_unit.suffix}", k="lM")]] + [[sg.T("0", k=f"{i.key}lM",
                                                                                              enable_events=True)] for
                                                                                        i in self.side_vals]
            left_vals_percentage = [[sg.T("%")]] + [[sg.T("0%", k=f"{i.key}lp")] for i in self.side_vals]

            right_vals_names = [[sg.T("Names")]] + [[sg.T(chem_to_visual(i.chemical),
                                                          font=chemfont)] for i in self.side_vals]
            right_vals_mass = [[sg.T(f"{current_unit.suffix}")]] + [[sg.T("0", k=f"{i.key}rm")] for i in self.side_vals]
            right_vals_molvolume = [[sg.T(f"mol/{current_vol_unit.suffix}", k="rM")]] + [[sg.T("0", k=f"{i.key}rM",
                                                                                               enable_events=True)] for
                                                                                         i in self.side_vals]
            right_vals_percentage = [[sg.T("%")]] + [[sg.T("0%", k=f"{i.key}rp")] for i in self.side_vals]
        else:
            if side == "Reactants":
                self.side_vals = count_atoms(self.obj.reactants)
            else:
                self.side_vals = count_atoms(self.obj.products)

            left_vals_names = [[sg.T("Names")]] + [[sg.T(f"{self.side_vals[i]} {i}")] for i in self.side_vals]
            left_vals_mass = [[sg.T(f"{current_unit.suffix}", k="lm")]] + [[sg.T("0", k=f"{i}lm")] for i in
                                                                           self.side_vals]
            left_vals_molvolume = [[sg.T(f"mol/{current_vol_unit.suffix}", k="lM")]] + [[sg.T("0", k=f"{i}lM",
                                                                                              enable_events=True)] for
                                                                                        i in self.side_vals]
            left_vals_percentage = [[sg.T("%")]] + [[sg.T("0%", k=f"{i}lp")] for i in self.side_vals]

            right_vals_names = [[sg.T("Names")]] + [[sg.T(f"{self.side_vals[i]} {i}")] for i in self.side_vals]
            right_vals_mass = [[sg.T(f"{current_unit.suffix}", key="rm")]] + [[sg.T("0", k=f"{i}rm")] for i in
                                                                              self.side_vals]
            right_vals_molvolume = [[sg.T(f"mol/{current_vol_unit.suffix}", k="rM")]] + [[sg.T("0", k=f"{i}rM",
                                                                                               enable_events=True)] for
                                                                                         i in self.side_vals]
            right_vals_percentage = [[sg.T("%")]] + [[sg.T("0%", k=f"{i}rp")] for i in self.side_vals]

        left = sg.Col([[sg.Col(left_measurements)],
                       [sg.HSep()],
                       [sg.Col(left_vals_names), sg.Col(left_vals_mass), sg.Col(left_vals_molvolume),
                        sg.Col(left_vals_percentage)]])

        right = sg.Col([[sg.Col(right_measurements)],
                        [sg.HSep()],
                        [sg.Col(right_vals_names), sg.Col(right_vals_mass), sg.Col(right_vals_molvolume),
                         sg.Col(right_vals_percentage)]])

        self.layout = [[sg.Col(top_settings)],
                       [left, sg.VSep(), right]]
        self.update_total_units()
        self.win = sg.Window(title="Dissolved", layout=self.layout, font=(fonttype, fontsize), finalize=True)
        self.loop()

    def update_total_units(self):
        if self.breakdown == "Chemical":
            if len(self.side_vals) == 0:
                self.total_units = 0
                return
            self.total_units = count_units(add_dicts(*[multiply_dict(i.get_all_components(),
                                                                     i.amount) for i in self.side_vals]))
            return
        self.total_units = count_units(self.side_vals)

    def define_mass_from_mol_volume(self, key, left=True):
        desired = sg.popup_get_text(f"Please input the desired {mol_over_vol.suffix}")
        try:
            desired_dec = Decimal(desired)
        except (InvalidOperation, TypeError):
            sg.popup_ok("Sorry! Couldn't convert your input into a number.\n - Did you use a comma instead of a dot?")
            return False
        percent = self.percentages[key]
        if self.breakdown == "Chemical":
            for i in self.side_vals:
                if i.key == key:
                    element = i
                    break
            else:
                return False
        else:
            for i in self.side_vals:
                if i == key:
                    element = i
                    break
            else:
                return False
        if self.breakdown == "Chemical":
            element_mass = element.molarmass
        else:
            element_mass = atom_units[element]
        mol_needed_of_element = desired_dec * self.volume * (current_vol_unit.multiplier / mol_over_vol.multiplier)
        mass_from_element = mol_needed_of_element * element_mass
        total_mass = mass_from_element / percent
        if left:
            self.mass = total_mass
        else:
            self.rmass = total_mass
            self.define_ratio_from_rmass()
        self.write_masses_and_ratio()
        self.update_all()
        return True

    def update_percentages(self):
        if self.breakdown == "Chemical":
            for i in self.side_vals:
                chem_units = count_units(i.get_all_components()) * i.amount
                percent = chem_units / self.total_units
                self.win[f"{i.key}lp"](value=f"{decimal_to_string(percent * 100)}%")
                self.win[f"{i.key}rp"](value=f"{decimal_to_string(percent * 100)}%")
                self.percentages[i.key] = percent
            return
        for i in self.side_vals:
            a_units = atom_units[i] * self.side_vals[i]
            percent = a_units / self.total_units
            self.win[f"{i}lp"](value=f"{decimal_to_string(percent * 100)}%")
            self.win[f"{i}rp"](value=f"{decimal_to_string(percent * 100)}%")
            self.percentages[i] = percent

    def update_units(self):
        # t_win["lm"](value=current_unit.suffix)
        # t_win["rm"](value=current_unit.suffix)
        self.win["lM"](value=f"{mol_over_vol.suffix}")
        self.win["rM"](value=f"{mol_over_vol.suffix}")

    def update_bottom(self):
        if self.breakdown == "Chemical":
            for i in self.side_vals:
                m = self.mass * self.percentages[i.key]
                self.win[f"{i.key}lm"](value=decimal_to_string(m))
                self.win[f"{i.key}rm"](value=decimal_to_string(self.rmass * self.percentages[i.key]))
                if self.volume == 0:
                    self.win[f"{i.key}lM"](value="---")
                    self.win[f"{i.key}rM"](value="---")
                else:
                    self.win[f"{i.key}lM"](value=decimal_to_string((m / i.molarmass *
                                                                    (mol_over_vol.multiplier
                                                                     / current_vol_unit.multiplier)
                                                                    / self.volume)))
                    self.win[f"{i.key}rM"](value=decimal_to_string((((m / i.molarmass) / self.volume) * self.ratio) *
                                                                   (mol_over_vol.multiplier
                                                                    / current_vol_unit.multiplier)))
            return
        for i in self.side_vals:
            m = self.mass * self.percentages[i]
            self.win[f"{i}lm"](value=decimal_to_string(m))
            self.win[f"{i}rm"](value=decimal_to_string(self.rmass * self.percentages[i]))
            if self.volume == 0:
                self.win[f"{i}lM"](value="---")
                self.win[f"{i}rM"](value="---")
            else:
                self.win[f"{i}lM"](value=decimal_to_string((m / atom_units[i]) / self.volume *
                                                           (mol_over_vol.multiplier / current_vol_unit.multiplier)))
                self.win[f"{i}rM"](value=decimal_to_string(((m / atom_units[i]) / self.volume) * self.ratio *
                                                           (mol_over_vol.multiplier / current_vol_unit.multiplier)))

    def update_rmass(self):
        self.rmass = self.ratio * self.mass
        if self.ratio == 0:
            self.rmass = 0
        elif self.rmass == 0:
            self.ratio = 0
        self.write_win_val_but_not_if_zero("Mass_right", self.rmass)

    def define_ratio_from_rmass(self):
        if self.rmass == 0 or self.mass == 0:
            self.ratio = 0
            return
        self.ratio = self.rmass / self.mass

    def write_win_val_but_not_if_zero(self, key, val, digits=ROUND_TO_DIGITS):
        self.win[key](value=decimal_to_string(val, digits) if val != 0 else "")

    def update_one_over_ratio(self):
        if self.ratio != 0:
            self.win["1overRatio"](value=f"1/{decimal_to_string(1 / Decimal(self.ratio))}")
            return
        self.win["1overRatio"](value="")

    def write_masses_and_ratio(self):
        self.write_win_val_but_not_if_zero("Mass_left", self.mass)
        self.write_win_val_but_not_if_zero("Mass_right", self.rmass)
        self.write_win_val_but_not_if_zero("Ratio", self.ratio)

    def update_all(self):
        self.update_rmass()
        self.update_one_over_ratio()
        self.update_bottom()
        self.update_units()

    def transfer_mass(self, use_rmass=False):
        lst = self.obj.reactants if self.side == "Reactants" else self.obj.products
        total_units = Decimal(0)
        mass_to_use = self.rmass if use_rmass else self.mass
        for i in lst:
            total_units += i.molarmass * i.amount
        for i in lst:
            if i.molarmass != 0:
                i.set_mass(mass_to_use * (i.molarmass * i.amount / total_units))

    def loop(self):
        global current_vol_unit
        restart = False
        self.update_total_units()
        self.update_percentages()
        self.update_bottom()
        self.update_all()
        while True:
            event, values = self.win.read()

            print(event)

            if event == sg.WIN_CLOSED:
                break

            elif event == "-R/P_CHEMICALS-":
                if values["-R/P_CHEMICALS-"] != self.side:
                    restart = True
                    self.side = values["-R/P_CHEMICALS-"]
                    break

            elif event == "-BREAKDOWN_TYPE-":
                if values["-BREAKDOWN_TYPE-"] != self.breakdown:
                    restart = True
                    self.breakdown = values["-BREAKDOWN_TYPE-"]
                    break

            elif event == "-VOL_UNIT-":
                new_vol_unit = values["-VOL_UNIT-"]
                for i in vol_units:
                    if i.name == new_vol_unit:
                        diff = current_vol_unit.multiplier / i.multiplier
                        self.volume *= diff
                        self.win["VolumeField"](value=decimal_to_string(self.volume, ROUND_TO_DIGITS_MAX))
                        current_vol_unit = i
                self.win["volString"](value=f"Volume ({current_vol_unit.suffix}):")
                update_mol_over_vol()
                self.update_all()

            elif event == "Ratio":
                field = values["Ratio"]
                try:
                    if "/" in field:
                        field = field.split("/")
                        if len(field) == 2:
                            self.ratio = Decimal(field[0]) / Decimal(field[1])
                    else:
                        self.ratio = Decimal(field)
                except (ValueError, InvalidOperation):
                    self.ratio = 0
                self.update_all()

            elif event == "Mass_left":
                try:
                    self.mass = Decimal(values["Mass_left"])
                except (ValueError, InvalidOperation):
                    self.mass = 0
                self.update_all()

            elif event == "Mass_right":
                try:
                    m = Decimal(values["Mass_right"])
                except (ValueError, InvalidOperation):
                    self.ratio = 0
                    self.rmass = 0
                    self.write_masses_and_ratio()
                    self.update_all()
                else:
                    self.rmass = m
                    self.define_ratio_from_rmass()
                    self.write_masses_and_ratio()
                    self.update_all()

            elif event == "VolumeField":
                try:
                    self.volume = Decimal(values["VolumeField"])
                except (ValueError, InvalidOperation):
                    self.volume = 0
                self.update_all()

            elif event == "Transfer":
                self.win.close()
                self.transfer_mass()
                return True

            elif event[-2:] == "lM":
                self.define_mass_from_mol_volume(event[:-2] if self.breakdown == "Atomic" else int(event[:-2]))
            elif event[-2:] == "rM":
                self.define_mass_from_mol_volume(event[:-2] if self.breakdown == "Atomic" else int(event[:-2]),
                                                 left=False)

        self.win.close()

        if restart:
            return DissolvedWin(side=self.side,
                                breakdown=self.breakdown,
                                volume=self.volume,
                                mass=self.mass,
                                win_object=self.obj,
                                ratio=self.ratio)
        return False


global_reactants = []
global_products = []
position = (None, None)
win_size = (None, None)


def open_missing_menu(missing_dict, other_side_total_units=None):
    total_units = Decimal(sum([missing_dict[n] * atom_units[n] for n in missing_dict]))

    lower_data = [[sg.T(f"Total units: {decimal_to_string(total_units)}", tooltip=tooltips["MissingMenu:TotalUnits"])]]
    if other_side_total_units is not None and other_side_total_units != 0:
        lower_data.append(
            [sg.T(f"Percentage Missing: {decimal_to_string(total_units / other_side_total_units * 100)}%",
                  tooltip=tooltips["MissingMenu:PercentageMissing"])])
        lower_data.append(
            [sg.T(f"Percentage Present: {decimal_to_string((1 - total_units / other_side_total_units) * 100)}%",
                  tooltip=tooltips["MissingMenu:PercentagePresent"])])
        lower_data.append([sg.T(f"Total units (incl. not missing): {decimal_to_string(other_side_total_units)}u",
                                tooltip=tooltips["MissingMenu:TotalUnitsIncl"])])

    left_most_col = sg.Col([[sg.T("Atom")]] + [[sg.T(n)] for n in missing_dict])

    amount_col = sg.Col([[sg.T("Amount")]] + [[sg.T(missing_dict[n])] for n in missing_dict])

    unit_col = sg.Col(
        [[sg.T("Mass", tooltip=tooltips["MissingMenu:Mass"])]]
        + [[sg.T(f"{decimal_to_string(atom_units[n] * missing_dict[n])}u")] for n in missing_dict])

    percentage_of = sg.Col([[sg.T("Percentage of total", tooltip=tooltips["MissingMenu:Percentage"])]] + [
        [sg.T(f"{decimal_to_string((atom_units[n] * missing_dict[n]) / total_units * 100)}%")] for n in
        missing_dict])

    t_layout = [[left_most_col, sg.VSep(), amount_col, sg.VSep(), unit_col, sg.VSep(), percentage_of],
                lower_data]

    t_win = sg.Window(layout=t_layout, title="Missing Window", font=(fonttype, fontsize))

    while True:
        event, values = t_win.read()
        if event == sg.WIN_CLOSED:
            break


class Window:
    def __init__(self, reactants=(), products=()):
        global SCROLLABLE
        self.reactants = reactants
        self.products = products

        self.reactants += [Molecule(key=len(self.reactants) + i)
                           for i in range(max(0, DEFAULT_MOLECULE_AMOUNT - len(self.reactants)))]
        self.products += [Molecule(key=len(self.reactants) + i)
                          for i in range(max(0, DEFAULT_MOLECULE_AMOUNT - len(self.products)))]

        if SCROLLABLE is None:
            SCROLLABLE = True if len(self.reactants) != DEFAULT_MOLECULE_AMOUNT or \
                                 len(self.products) != DEFAULT_MOLECULE_AMOUNT else None

        self.values = None
        self.balanced = False
        self.should_push = False

        self.active_reactant = 0
        self.active_product = 0

        self.should_exit = False
        self.raw_layout = [[]]
        self.layout = [[]]  # redefined in the method update_layout()
        self.redo_layout()

        # noinspection PyTypeChecker
        self.win = sg.Window(title="Beregningsskema", layout=self.layout, resizable=True, font=(fonttype, fontsize),
                             finalize=True, use_default_focus=False,
                             titlebar_background_color=titlebar_background_color,
                             use_custom_titlebar=USE_CUSTOM_TITLEBAR, location=position,
                             size=win_size)

        self.win["Update"].block_focus()
        self.win["ReactantInput"].bind("<Return>", "_enter")
        self.win["ProductInput"].bind("<Return>", "_enter")

        self.loop()

    def add_reactant(self, chemical: str = ""):
        for r in [self.reactants[self.active_reactant]] + self.reactants:  # A bit of a dirty solution
            if r.is_completely_undefined():
                if r.set_chemical(chemical):
                    self.should_push = True
                return False
        self.reactants.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()
        return True

    def add_product(self, chemical: str = ""):
        for p in [self.products[self.active_product]] + self.products:  # A bit of a dirty solution
            if p.is_completely_undefined():
                if p.set_chemical(chemical):
                    self.should_push = True
                return False
        self.products.append(Molecule(chemical=chemical, key=len(self.reactants) + len(self.products)))
        self.restart()
        return True

    def redo_layout(self):
        self.redefine_raw_layout()
        self.update_layout()

    def redefine_raw_layout(self):
        self.raw_layout = [[sg.T(f"{' ' * (MONO_LEN - 10)}Missing:"),
                            sg.T(k="MissingReactantsMolarmass", size=(MONO_LEN, 1), enable_events=True), None, None,
                            None, None,
                            sg.T(f"{' ' * (MONO_LEN - 10)}Missing:"),
                            sg.T(k="MissingProductsMolarmass", size=(MONO_LEN, 1), enable_events=True)],

                           [None,
                            sg.T(k="MissingReactants", size=(MONO_LEN, 1)),
                            sg.Input(k="ReactantInput", size=(BASE_LEN, 1), background_color=input_background_color,
                                     enable_events=True, font=chemfont),
                            sg.T("Reactants", enable_events=True, k="addReactant"),
                            sg.Text("|"),
                            sg.T("Products", enable_events=True, k="addProduct"),
                            sg.Input(k="ProductInput", size=(BASE_LEN, 1), background_color=input_background_color,
                                     enable_events=True, font=chemfont),
                            sg.T(k="MissingProducts", size=(MONO_LEN, 1))],

                           [sg.T("Chemicals  :", font=mono, justification="r"), None, None, None, sg.Text("->"), None,
                            None, None],
                           [sg.T("m (g)      :", font=mono, k="m"), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("M (g/mol)  :", font=mono, k="M"), None, None, None, sg.Text("|"), None, None, None],
                           [sg.T("n (mol)    :", font=mono, k="n"), None, None, None, sg.Text("|"), None, None, None]]
        k = 2  # m should be equal to the amount of rows before the reactants and products fields + 1
        i = 4  # i should be equal to the index of the dividing line between reactants and products
        nones = 3  # amount of None's wherein the program should intitially write the chemicals and their attributes
        for m in self.reactants:
            for u in range(nones, 0, -1):
                if self.raw_layout[k][i - u] is None:
                    self.raw_layout[k][i - u], self.raw_layout[k + 1][i - u], self.raw_layout[k + 2][i - u], \
                        self.raw_layout[k + 3][i - u] = m.get_sg_objects()
                    break
            else:
                for n in range(k):
                    self.raw_layout[n] = [None] + self.raw_layout[n]
                for n in range(k, len(self.raw_layout)):
                    self.raw_layout[n] = self.raw_layout[n][:i] + [None] + self.raw_layout[n][i:]
                i += 1
                self.raw_layout[k][i - 1], self.raw_layout[k + 1][i - 1], self.raw_layout[k + 2][i - 1], \
                    self.raw_layout[k + 3][i - 1] = m.get_sg_objects()

        for m in self.products:
            for u in range(nones, 0, -1):
                if self.raw_layout[k][i + u] is None:
                    self.raw_layout[k][i + u], self.raw_layout[k + 1][i + u], self.raw_layout[k + 2][i + u], \
                        self.raw_layout[k + 3][i + u] = m.get_sg_objects()
                    break
            else:
                for n in range(k):
                    self.raw_layout[n] = self.raw_layout[n] + [None]
                for n in range(k, len(self.raw_layout)):
                    self.raw_layout[n] = self.raw_layout[n][:i + 1] + [None] + self.raw_layout[n][i + 1:]
                self.raw_layout[k][i + 1], self.raw_layout[k + 1][i + 1], self.raw_layout[k + 2][i + 1], \
                    self.raw_layout[k + 3][i + 1] = m.get_sg_objects()

        remove_indexes = []
        for ind, m in enumerate(self.raw_layout[0]):
            remove_indexes.append(ind)
            for n in self.raw_layout:
                if n[ind] is not None:
                    remove_indexes.pop(-1)
                    break

        remove_indexes.reverse()
        for m in remove_indexes:
            for n in self.raw_layout:
                n.pop(m)

    def update_molecules(self):
        fully_defined = []
        for r in self.reactants + self.products:
            if r.is_fully_defined():
                fully_defined.append(r)
        if not fully_defined:
            return

        def sort_func(x):
            return x.mol / x.amount

        fully_defined.sort(key=sort_func)
        r = fully_defined[0]
        for p in self.reactants + self.products:
            if r == p or p.chemical == "":
                continue
            if p.reset_amounts():
                self.should_push = True
            p.mass_is_user_defined = False
            p.mol_is_user_defined = False
            p.mol = r.mol * (Decimal(p.amount) / r.amount)
            p.try_calculate_mass_or_mol()

    def recalculate_chemicals(self):
        for r in self.reactants + self.products:
            r.calculate_molarmass()

    def update_unit(self):
        self.recalculate_chemicals()
        m_string = f"m ({current_unit.suffix})"
        molarmass_string = f"M ({current_unit.suffix}/mol)"
        m_string += " " * (11 - len(m_string)) + ":"
        molarmass_string += " " * (11 - len(molarmass_string)) + ":"
        self.win["m"](value=m_string)
        self.win["M"](value=molarmass_string)

    def multiply_masses(self, multiplier):
        for r in self.reactants + self.products:
            if r.mass == -1:
                continue
            if r.set_mass(r.mass * multiplier):
                self.should_push = True

    def write_molecules(self):
        for r in self.reactants + self.products:
            chem_val = chem_to_visual(r.chemical)
            if chem_val != self.values[r.key] and not (r.amount == 1 and chem_visual_amount_is_one(self.values[r.key])):
                self.win[r.key](value=chem_val)

            self.win[f"{r.key}M"](value=r.get_molarmass_string())

            try:
                written_mass = Decimal(self.values[f"{r.key}m"])
                if r.mass != written_mass:
                    self.win[f"{r.key}m"](value=r.get_mass_string())
            except InvalidOperation:
                self.win[f"{r.key}m"](value=r.get_mass_string())

            try:
                written_mol = Decimal(self.values[f"{r.key}n"])
                if r.mol != written_mol:
                    self.win[f"{r.key}n"](value=r.get_mol_string())
            except InvalidOperation:
                self.win[f"{r.key}n"](value=r.get_mol_string())

    def save_stuff(self):
        try:
            for r in self.reactants + self.products:
                if CONVERT_SHIFTED:
                    r.set_chemical(visual_to_chem(convert_shifted(self.values[r.key])))
                else:
                    r.set_chemical(visual_to_chem(self.values[r.key]))
                try:
                    t_mass = Decimal(self.values[f"{r.key}m"]) if self.values[f"{r.key}m"] else -1
                except InvalidOperation:
                    t_mass = -1
                try:
                    t_mol = Decimal(self.values[f"{r.key}n"]) if self.values[f"{r.key}n"] else -1
                except InvalidOperation:
                    t_mol = -1

                if (t_mass != -1 and r.mass == -1) or (
                        r.mass_is_user_defined and r.mass != t_mass):
                    r.mass_is_user_defined = True
                    r.set_mass(t_mass)

                if (t_mol != -1 and r.mol == -1) or (
                        r.mol_is_user_defined and r.mol != t_mol):
                    r.mol_is_user_defined = True
                    r.set_mol(t_mol)

                if (r.mass_is_user_defined and r.mass == -1) or (r.mol_is_user_defined and r.mol == -1):
                    r.reset_amounts()
                    r.mass_is_user_defined = None
                    r.mol_is_user_defined = None

        except (ValueError, TypeError,
                InvalidOperation):  # if input field doesn't contain a number or if window has been closed
            pass

    def reset_amounts(self):
        for r in self.reactants + self.products:
            if r.reset_amounts():
                self.should_push = True
            r.mass_is_user_defined = None
            r.mol_is_user_defined = None

    def calculate_mass_diff(self):
        return Decimal(sum([0 if r.is_completely_undefined() else r.mass for r in self.reactants])) - \
            Decimal(sum([0 if p.is_completely_undefined() else p.mass for p in self.products]))

    def calculate_reactants_mass(self):
        return Decimal(sum([0 if r.is_completely_undefined() else r.mass for r in self.reactants]))

    def calculate_products_mass(self):
        return sum([0 if p.is_completely_undefined() else p.mass for p in self.products])

    def calculate_reactants_units(self):
        return sum([r.molarmass * r.amount for r in self.reactants])

    def calculate_products_units(self):
        return sum([r.molarmass * r.amount for r in self.products])

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

        if atom in self.reactants[self.active_reactant].components:
            self.reactants[self.active_reactant].components[atom] += 1
        else:
            self.reactants[self.active_reactant].components[atom] = 1
        self.reactants[self.active_reactant].redefine_chemical_string()
        self.reactants[self.active_reactant].update()
        self.should_push = True

    def append_atom_product(self, atom):
        if len(self.products) == 0:
            self.add_product(atom)
            return

        if atom in self.products[self.active_product].components:
            self.products[self.active_product].components[atom] += 1
        else:
            self.products[self.active_product].components[atom] = 1
        self.products[self.active_product].redefine_chemical_string()
        self.products[self.active_product].update()
        self.should_push = True

    def restart(self):
        global global_reactants
        global global_products
        global continue_program
        global position
        global win_size
        position = self.win.CurrentLocation()
        win_size = self.win.Size
        global_reactants = self.reactants
        global_products = self.products
        self.should_exit = True
        continue_program = True

    def check_balanced(self, return_missing=False):
        r_missing, p_missing = check_balanced(self.reactants, self.products)
        if return_missing:
            return r_missing, p_missing
        try:
            r_missing_molarmass = decimal_to_string(Decimal(sum([atom_units[n] * r_missing[n] for n in r_missing])),
                                                    ROUND_TO_DIGITS_LONG)
            p_missing_molarmass = decimal_to_string(Decimal(sum([atom_units[n] * p_missing[n] for n in p_missing])),
                                                    ROUND_TO_DIGITS_LONG)
        except KeyError:
            r_missing_molarmass = "-" * MONO_LEN
            p_missing_molarmass = "-" * MONO_LEN

        m_reactant_val = " ".join([f"{r_missing[n]}{n}" for n in r_missing])
        if len(m_reactant_val) > MONO_LEN:
            m_reactant_val = "-" * MONO_LEN
        m_product_val = " ".join([f"{p_missing[n]}{n}" for n in p_missing])
        if len(m_product_val) > MONO_LEN:
            m_product_val = "-" * MONO_LEN

        self.win["MissingReactants"](value=m_reactant_val)
        self.win["MissingProducts"](value=m_product_val)
        self.win["MissingReactantsMolarmass"](value=f"{r_missing_molarmass}u")
        self.win["MissingProductsMolarmass"](value=f"{p_missing_molarmass}u")

        return len(r_missing) == 0 and len(p_missing) == 0

    def update_mass_and_balance_vals(self):
        if self.check_balanced():
            self.win["BALANCED"].update(text_color=active_color)
            self.balanced = True
        else:
            self.win["BALANCED"].update(text_color=disabled_color)
            self.balanced = False

        if self.mass_defined():
            m_diff = self.calculate_mass_diff()
            self.win["MassDiff"](value=decimal_to_string(m_diff, ROUND_TO_DIGITS_LONG))
            self.win["RMass"](value=f"{decimal_to_string(self.calculate_reactants_mass(), ROUND_TO_DIGITS_LONG)}g")
            self.win["MassDiff"].update(text_color=active_color)
            self.win["RMass"].update(text_color=active_color)
        else:
            self.win["MassDiff"].update(text_color=disabled_color)
            self.win["RMass"].update(text_color=disabled_color)

    def update_user_defined_color(self):
        for r in self.reactants + self.products:
            self.win[f"{r.key}m"].update(
                text_color=user_defined_color if r.mass_is_user_defined else sg.theme_text_color())
            self.win[f"{r.key}n"].update(
                text_color=user_defined_color if r.mol_is_user_defined else sg.theme_text_color())

    def update_active_background_color(self):
        if not USE_ATOM_ADD:
            return
        for r in self.reactants + self.products:
            self.win[r.key].update(background_color=sg.theme_input_background_color())
        self.win[self.reactants[self.active_reactant].key].update(background_color=field_active_color)
        self.win[self.products[self.active_product].key].update(background_color=field_active_color)

    def handle_inputs(self):
        r_val = self.values["ReactantInput"]
        if CONVERT_SHIFTED:
            r_val = convert_shifted(r_val)
        r_val = chem_to_visual(r_val)
        if self.values["ReactantInput"] != r_val:
            self.win["ReactantInput"](value=r_val)

        p_val = self.values["ProductInput"]
        if CONVERT_SHIFTED:
            p_val = convert_shifted(p_val)
        p_val = chem_to_visual(p_val)
        if self.values["ProductInput"] != p_val:
            self.win["ProductInput"](value=p_val)

    def sort_chemicals_by_key(self):
        def sort_func(r):
            return r.key

        self.reactants.sort(key=sort_func)
        self.products.sort(key=sort_func)

    def open_advanced_reactant_missing(self):
        return open_missing_menu(self.check_balanced(return_missing=True)[0], self.calculate_products_units())

    def open_advanced_product_missing(self):
        return open_missing_menu(self.check_balanced(return_missing=True)[1], self.calculate_reactants_units())

    def update_secondary_elements(self):
        self.update_mass_and_balance_vals()
        self.update_active_background_color()
        self.update_user_defined_color()

    def loop(self):
        global USE_SUBSCRIPT
        global CONVERT_SHIFTED
        global SCROLLABLE
        global ATOM_ADD_ELEMENTANALYZER_BUTTON
        global current_unit
        pre_vals = {}
        self.sort_chemicals_by_key()
        self.update_secondary_elements()
        self.update_unit()
        while not self.should_exit:
            event, self.values = self.win.read(timeout=200)
            if event == sg.WIN_CLOSED:
                break

            if event != "__TIMEOUT__" and pre_vals != self.values:
                print(event)

            # ONLY FIELDS THAT CAN BE CHANGED BY THE USER SHOULD HAVE A KEY THAT:
            #  - Starts with a digit
            #  - Is an integer
            if isinstance(event, int) or event[0].isdigit():
                try:
                    self.save_stuff()
                except KeyError:
                    pass
                self.update_secondary_elements()

            if event == sg.WIN_CLOSED or self.should_exit:
                break
            elif event == "__TIMEOUT__":
                continue
            elif isinstance(event, int):
                self.update_mass_and_balance_vals()
                self.should_push = True
            elif event == "addReactant":
                self.add_reactant()
            elif event == "addProduct":
                self.add_product()
            elif event == "Update":
                if self.balanced or sg.popup_yes_no(
                        "Reaction is not balanced.\n\nDo you still wish to proceed?") == "Yes":
                    self.update_molecules()
                    self.update_mass_and_balance_vals()
                    self.should_push = True
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
                self.should_push = True
            elif event == "Reset":
                SCROLLABLE = None
                self.reset_amounts()
                if len(self.reactants) > DEFAULT_MOLECULE_AMOUNT or len(self.products) > DEFAULT_MOLECULE_AMOUNT:
                    self.reactants.clear()
                    self.products.clear()
                    self.restart()
                    break
                for r in self.reactants + self.products:
                    r.reset()

                self.should_push = True
            elif event == "ResetAmounts":
                self.reset_amounts()

            elif event == "r_left":
                self.active_reactant = max(self.active_reactant - 1, 0)
                self.should_push = True
            elif event == "r_right":
                self.active_reactant = min(self.active_reactant + 1, len(self.reactants) - 1)
                self.should_push = True

            elif event == "p_right":
                self.active_product = max(self.active_product - 1, 0)
                self.should_push = True
            elif event == "p_left":
                self.active_product = min(self.active_product + 1, len(self.products) - 1)
                self.should_push = True

            elif event == "Restart":
                self.restart()
                break

            elif event == "MissingReactantsMolarmass":
                self.open_advanced_reactant_missing()

            elif event == "MissingProductsMolarmass":
                self.open_advanced_product_missing()

            elif event == "ReactantInput" or event == "ProductInput":
                self.handle_inputs()

            elif event == "ReactantInput_enter":
                self.add_reactant(visual_to_chem(self.values["ReactantInput"]))
                self.win["ReactantInput"](value="")
            elif event == "ProductInput_enter":
                self.add_product(visual_to_chem(self.values["ProductInput"]))
                self.win["ProductInput"](value="")
            elif event == "Double":
                for r in self.reactants + self.products:
                    if not r.is_completely_undefined():
                        r.amount *= 2
                        r.redefine_chemical_string()
                self.should_push = True
            elif event == "Half":
                for r in self.reactants + self.products:
                    if not r.is_completely_undefined():
                        r.amount = max(r.amount // 2, 1)
                        r.redefine_chemical_string()
                self.should_push = True
            elif event == "Auto-balance":
                self.reactants, self.products = balance_reaction(self.reactants, self.products)
                self.sort_chemicals_by_key()
                self.should_push = True
            elif event == "Reset balance":
                for r in self.reactants + self.products:
                    r.amount = 1
                    r.redefine_chemical_string()
                self.should_push = True
            elif event == "Subscript":
                USE_SUBSCRIPT = not USE_SUBSCRIPT
                self.win["Subscript"].update(text_color=active_color if USE_SUBSCRIPT else disabled_color)
                self.should_push = True
            elif event == "ShiftConvert":
                CONVERT_SHIFTED = not CONVERT_SHIFTED
                self.win["ShiftConvert"].update(text_color=active_color if CONVERT_SHIFTED else disabled_color)
                self.should_push = True
            elif event == "Scrollbars":
                SCROLLABLE = not SCROLLABLE
                self.restart()
            elif event == "-ANALYSE_ATOMS-":
                ATOM_ADD_ELEMENTANALYZER_BUTTON = not ATOM_ADD_ELEMENTANALYZER_BUTTON
                self.win["-ANALYSE_ATOMS-"].update(text_color=active_color
                if ATOM_ADD_ELEMENTANALYZER_BUTTON else
                disabled_color)
            elif event == "ElementAnalyzer":
                ElementAnalyzer(self)
            elif event == "-UNIT_LIST-":
                new_unit = self.values["-UNIT_LIST-"]
                for i in units:
                    if i.name == new_unit:
                        diff = current_unit.multiplier / i.multiplier
                        self.multiply_masses(diff)
                        current_unit = i
                        break
                self.should_push = True
                self.update_unit()

            elif event == "Dissolved":
                if DissolvedWin(win_object=self):
                    self.should_push = True

            else:
                try:
                    if event[:10] == "rmolecule:":
                        chem = event[10:]
                        self.add_reactant(chem)

                    elif event[:10] == "pmolecule:":
                        chem = event[10:]
                        self.add_product(chem)

                except (TypeError, IndexError) as e:
                    print(f"ERROR: {e}")

                try:
                    if event[:6] == "ratom:":
                        if ATOM_ADD_ELEMENTANALYZER_BUTTON:
                            ElementAnalyzer(win_object=self, initial_element=event[6:])
                        else:
                            self.append_atom_reactant(event[6:])

                    elif event[:6] == "patom:":
                        if ATOM_ADD_ELEMENTANALYZER_BUTTON:
                            ElementAnalyzer(win_object=self, initial_element=event[6:])
                        else:
                            self.append_atom_product(event[6:])
                except (TypeError, IndexError) as e:
                    print(f"ERROR: {e}")

                try:
                    if event[0].isdigit() and (event[-1] == "m" or event[-1] == "n"):
                        self.update_mass_and_balance_vals()
                        self.should_push = True
                except (TypeError, IndexError) as e:
                    print(f"ERROR: {e}")

            if self.should_push:
                self.should_push = False
                self.write_molecules()
                self.update_secondary_elements()

        self.win.close()

    def update_layout(self):
        main_button_panel = [[sg.B("Update", font=small_font, k="Update"), sg.B("Switch", font=small_font),
                              sg.T("BALANCED", font=small_font, k="BALANCED", text_color=active_color)],
                             [sg.B("Reset", font=small_font), sg.B("ResetAmounts", font=small_font),
                              sg.B("Restart", font=small_font)]]
        data_panel = [[sg.T("Mass diff (r-p): ", font=small_font), sg.T("0." + "0" * 12, k="MassDiff", font=small_font,
                                                                        text_color=disabled_color)],
                      [sg.T("Mass (r): ", font=small_font), sg.T("0." + "0" * 12, k="RMass", font=small_font,
                                                                 text_color=disabled_color)],
                      ]
        secondary_button_panel = [[sg.B("Double", font=small_font), sg.B("Auto-balance", font=small_font),
                                   sg.B("Dissolved", font=small_font)],
                                  [sg.B("Half", font=small_font), sg.B("Reset balance", font=small_font),
                                   sg.B("ElementAnalyzer", font=small_font)]]

        tertiary_button_panel = [[sg.T("Subscript", k="Subscript",
                                       text_color=active_color if USE_SUBSCRIPT else disabled_color,
                                       font=small_font, enable_events=True),
                                  sg.T("Scrollbars", k="Scrollbars",
                                       text_color=active_color if SCROLLABLE else disabled_color,
                                       font=small_font, enable_events=True)],
                                 [sg.T("Shift Convert", k="ShiftConvert",
                                       text_color=active_color if CONVERT_SHIFTED else disabled_color,
                                       font=small_font, enable_events=True),
                                  sg.T("Analyse Atoms", k="-ANALYSE_ATOMS-",
                                       text_color=active_color if ATOM_ADD_ELEMENTANALYZER_BUTTON else disabled_color,
                                       font=small_font, enable_events=True)
                                  if ATOM_ADD_ELEMENTANALYZER_BUTTON is not None and USE_ATOM_ADD else
                                  sg.T()]]

        drop_down_panel = [[sg.Combo(values=[i.name for i in units], key="-UNIT_LIST-",
                                     size=(max(*[len(i.name) for i in units]), 1),
                                     default_value=current_unit.name, font=small_font, enable_events=True)]]

        layout_prefix = [[sg.Col(main_button_panel), sg.Col(data_panel), sg.Col(secondary_button_panel),
                          sg.Col(tertiary_button_panel), sg.Col(drop_down_panel)]]

        r_lower_control_panel = ()
        p_lower_control_panel = ()
        if USE_ATOM_ADD:
            r_lower_control_panel = ((("<-", "r_left"), ("->", "r_right")),)
            p_lower_control_panel = ((("<-", "p_left"), ("->", "p_right")),)

        mol_tuple = ()
        if USE_MOLECULE_ADD:
            mol_tuple = (("O2", "CO2", "H2O", "N2"),
                         ("CH4", "C2H6", "C3H8", "C4H10", "C5H12", "C6H14", "C7H16", "C8H18", "C9H20", "C10H22"),
                         ("CH3OH", "CH3CH2OH", "C8HF17O3S"))

        atom_add_list = ()
        max_atom_len = 1  # value isn't used unless USE_ATOM_ADD
        if USE_ATOM_ADD:
            atom_add_list = [["-1", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "-18"],
                             ["H", "-2", "", "", "", "", "", "", "", "", "", "", "-13", "-14", "-15", "-16", "-17",
                              "He"],
                             ["Li", "Be", "", "", "", "", "", "", "", "", "", "", "B", "C", "N", "O", "F", "Ne"],
                             ["Na", "Mg", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "-11", "-12", "Al", "Si",
                              "P", "S", "Cl", "Ar"],
                             ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
                              "Se", "Br", "Kr"],
                             ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
                              "Te", "I", "Xe"],
                             ["Cs", "Ba", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
                              "Po", "At", "Rn"],
                             ["Fr", "Ra", "Lr", "Rf", "Db", "Sg", "Bh", "Hs"]]
            max_width = max([len(i) for i in atom_add_list])
            for i in atom_add_list:
                for n in i:
                    if len(n) > max_atom_len and n[0] != "-":
                        max_atom_len = len(n)

            if ATOM_ADD_ALIGN:
                for i in atom_add_list:
                    if len(i) < max_width:
                        i += [""] * (max_width - len(i))

        lower_left_panel_add = [[sg.B(i[0], k=i[1]) for i in m] for m in r_lower_control_panel]
        lower_right_panel_add = [[sg.B(i[0], k=i[1]) for i in m] for m in p_lower_control_panel]

        r_add = [[sg.B(chem_to_visual(n), k=f"rmolecule:{n}", font=small_chem) for n in i] for i in mol_tuple]
        p_add = [[sg.B(chem_to_visual(n), k=f"pmolecule:{n}", font=small_chem) for n in i] for i in mol_tuple]

        if USE_ATOM_ADD:
            ar_add: list[list[sg.Button | sg.Text]] = [[] for _ in range(len(atom_add_list))]
            ap_add: list[list[sg.Button | sg.Text]] = [[] for _ in range(len(atom_add_list))]

            for ind, i in enumerate(atom_add_list):
                for n in i:
                    if n and n[0] != "-":
                        ar_add[ind].append(sg.B(n, s=(max_atom_len if ATOM_ADD_ALIGN else len(n), 1), k=f"ratom:{n}",
                                                font=small_font, p=(2, 5)))
                        ap_add[ind].append(sg.B(n, s=(max_atom_len if ATOM_ADD_ALIGN else len(n), 1), k=f"patom:{n}",
                                                font=small_font, p=(2, 5)))
                    elif SHOW_ATOM_ADD_GROUPS and n and n[0] == "-":
                        ar_add[ind].append(sg.T(n[1:], font=small_font, size=(len(n[1:]), 1), justification="c",
                                                expand_x=True, p=0))
                        ap_add[ind].append(sg.T(n[1:], font=small_font, size=(len(n[1:]), 1), justification="c",
                                                expand_x=True, p=0))
                    elif ATOM_ADD_ALIGN:
                        ar_add[ind].append(sg.T())
                        ap_add[ind].append(sg.T())
            if ATOM_ADD_ALIGN:
                temp_ar_add = [[]]
                temp_ap_add = [[]]
                for i in range(len(ar_add[0])):
                    temp_ar_add[0].append(sg.Col([[n[i]] for n in ar_add]))
                    temp_ap_add[0].append(sg.Col([[n[i]] for n in ap_add]))
                ar_add = temp_ar_add
                ap_add = temp_ap_add
        else:
            ar_add = []
            ap_add = []

        layout_suffix = [[sg.Col([[sg.Col(lower_left_panel_add, justification="l", expand_x=True),
                                   sg.Col(lower_right_panel_add, justification="r", element_justification="r")]],
                                 expand_x=True)],
                         [sg.Col([[sg.Col(r_add, justification="l", expand_x=True),
                                   sg.Col(p_add, justification="r", element_justification="r")]],
                                 expand_x=True, expand_y=True)],
                         [sg.Col([[sg.Col(ar_add, justification="l", expand_x=True),
                                   sg.VSep()
                                   if ATOM_ADD_ALIGN else
                                   sg.Col([[sg.T("|")] for _ in atom_add_list], expand_x=True),
                                   sg.Col(ap_add, justification="r", element_justification="r")]],
                                 expand_x=False if ATOM_ADD_ALIGN else True, expand_y=True)]]

        self.layout = [[]]
        for i in range(len(self.raw_layout[0])):
            self.layout[0] += [sg.Col([[sg.Text() if n[i] is None else n[i]] for n in self.raw_layout],
                                      element_justification="c")]
        self.layout = [[sg.Col(layout_prefix + self.layout + layout_suffix,
                               scrollable=True if SCROLLABLE else False,
                               expand_y=True, expand_x=True, justification="c", element_justification="c",
                               key="MainCol")]]


while continue_program:
    continue_program = False
    Window(global_reactants, global_products)
