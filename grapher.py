import math
import re
import codecs
import sys

# why arent these in math in the first place?
def sec(x):
    return 1 / math.cos(x)

def csc(x):
    return 1 / math.sin(x)

def cot(x):
    return 1 / math.tan(x)

math.sec = sec
math.csc = csc
math.cot = cot

def get_float(prompt):
    return float(input(prompt))

# linear map val∈[valmin, valmax] |→ out∈[outmin, outmax]
def scale(val,  valmin,  valmax,  outmin,  outmax):
    return (
        (val - valmin) / (valmax - valmin)
        * (outmax - outmin) + outmin
    )

def place_at_coordinate(value, x, y, field):
    field[y] = field[y][0:x] + value + field[y][x + len(value):]
    return field

def eval_fn(fn, x):
    ret: float
    try:
        ret = eval(fn)
    except ValueError:
        # negative number in a log or root probably
        ret = float("nan")
    return ret

print("enter a formula to graph in terms of x, or HELP for help")

def get_fn():
    return input("y(x) = ")

fn = get_fn()
if len(fn) is 0:
    fn = "2sinx"

if fn == "HELP":
    print("""enter a formula to graph in terms of x
functions like sin, tan, ln, floor, and sqrt are allowed
as are pi and e. exponentiation is allowed (e.g. x^2) but for non-integer
exponents e.g. pow(x, 2.2) should be used instead. parsing is not that advanced,
so don’t get too surprised if something wacky happens. as with c; when in
doubt, add more parenthesis. (sinx^2 will parse as sin(x)^2, for example, and
sin^2 x will probably crash the program)
EXAMPLE: y(x) = 2sinx
EXAMPLE: y(x) = ln(0.5x^2)
EXAMPLE: y(x) = (x - 3)(x)(x + 2) / 10""")
    fn = get_fn()


# replace stuff like 2tan(4x) with 2*tan(4*x)
fn = re.sub(r"(\d+)([a-zA-Z]+)", r"\1 * \2", fn)

# ln = log
fn = re.sub(r"ln", r"log", fn)

# when you type (x + 2)(x - 2) you probably meant to multiply them right?
fn = re.sub(r"\)\(", r")*(", fn)

# replace stuff like tan x or tanx with tan(x), which python can evaluate
# sorry this is so long, please ignore, it's literally every 1-arg math method
fn = re.sub(r"""\b(ceil|fabs|factorial|floor|frexp|fsum|isfinite|
|isinf|isnan|modf|trunc|exp|expm1|log|log1p|log2|log10|sqrt|acos|asin|atan|cos|
|sin|tan|degrees|radians|acosh|asinh|atanh|cosh|sinh|tanh|erf|erfc|gamma|lgamma|
|sec|csc|cot)\s*x\b""", r"\1(x)", fn)

# replace stuff like tan(x) with math.tan(x), which python can evaluate sorry
# this is so long, please ignore, it's literally every math method
fn = re.sub(r"""\b(ceil|copysign|fabs|factorial|floor|fmod|frexp|fsumg|gcd|
|isclose|isfinite|isinf|isnan|ldexp|modf|trunc|exp|expm1|log|log1p|log2|log10|
|pow|sqrt|acos|asin|atan|atan2|cos|hypot|sin|tan|degrees|radians|acosh|asinh|
|atanh|cosh|sinh|tanh|erf|erfc|gamma|lgamma|pi|e|tau|inf|nan|sec|csc|cot)\b""",
r"math.\1", fn)

# so stuff like log(x)sin(x) works as expected
fn = re.sub(r"\)\s*math", r") * math", fn)

# replace ^ with **
fn = re.sub(r"\^", r"**", fn)

coords = []
slopes = []

# window info for console output
win_w = 79
win_h = 23
win_cx = math.floor(win_w / 2)
win_cy = math.floor(win_h / 2)

# graph data
domain_min = -5
domain_max = 5
range_min = -5
range_max = 5

dx = scale(1 / win_w, 0, win_w, 0, domain_max - domain_min)
for i in range(0, win_w):
    x = scale(i, 0, win_w, domain_min, domain_max)
    coords.append(eval_fn(fn, x))
    slopes.append((eval_fn(fn, x + dx) - eval_fn(fn, x)) / (dx))

# initialize a 2d list of win_h lines of strings each win_w wide
graph = []
graph.append("─" * win_w)
for i in range(0, win_h - 2):
    graph.append("│" + " " * (win_w - 1) + "│")
graph.append("─" * win_w)
graph = place_at_coordinate("┌", 0,     win_h - 1, graph)
graph = place_at_coordinate("┐", win_w, win_h - 1, graph)
graph = place_at_coordinate("┘", win_w, 0,         graph)
graph = place_at_coordinate("└", 0,     0,         graph)

for i in range(0, win_w):
    # line for x axis
    graph = place_at_coordinate("─", i, win_cy, graph)
    # if we have a number to plot, plot it
    if not math.isnan(coords[i]):
        char = "●"
        if not math.isnan(slopes[i]):
            if   abs(slopes[i]) >= 2 and slopes[i - 1] >= 0:
                char = "▌"
            elif abs(slopes[i]) >= 2 and slopes[i - 1] < 0:
                char = "▐"
            elif slopes[i] >= 0.75:
                # char = "╱"
                char = "▞"
            elif slopes[i] <= -0.75:
                char = "▚"
            # elif slopes[i - 1] >= 0:
                # char = "▄"
            else: # slopes[i - 1] <= 0
                char = "▀"
        height = math.floor(scale(coords[i], range_min, range_max, 0, win_h))
        if height > 0 and height < win_h:
            graph = place_at_coordinate(char, i, height, graph)

for i in range(0, win_h):
    graph = place_at_coordinate("│", win_cx, i, graph)

for i in range(domain_min, domain_max):
    x_tick = math.floor(scale(i, domain_min, domain_max, 0, win_w))
    graph = place_at_coordinate("┼", x_tick, win_cy, graph)
    graph = place_at_coordinate(str(i), x_tick, win_cy + 1, graph)

for i in range(range_min, range_max):
    y_tick = math.floor(scale(i, range_min, range_max, 0, win_h))
    graph = place_at_coordinate("┼", win_cx, y_tick, graph)
    graph = place_at_coordinate(str(i), win_cx + 2, y_tick, graph)

graph = place_at_coordinate("├", 0,      win_cy,    graph)
graph = place_at_coordinate("┤", win_w,  win_cy,    graph)
graph = place_at_coordinate("┬", win_cx, win_h - 1, graph)
graph = place_at_coordinate("┴", win_cx, 0,         graph)

# origin
graph = place_at_coordinate("┼", win_cx, win_cy, graph)

for j in range(win_h - 1, -1, -1):
    print(graph[j])
