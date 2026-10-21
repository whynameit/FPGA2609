# Plot report figures from the simulation CSV files.
# Usage (from the project root): python sim/plot_waves.py .   -> writes doc/fig/*.png
import csv, sys, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
S = sys.argv[1]; FIG = os.path.join(S, "doc", "fig")
IN_C, OUT_C, INK, MUTED = "#2a6fdb", "#d1495b", "#222222", "#888888"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

def read_csv(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return rows

def timing(fname, title, t_end, step, signals, case_labels, top_note):
    # signals: list of (label, times[], values[], color)
    n = len(signals)
    fig, ax = plt.subplots(figsize=(9, 0.62 * n + 1.3))
    for i, (lab, ts, vs, col) in enumerate(signals):
        y0 = (n - 1 - i) * 1.6
        xs = list(ts) + [t_end]; ys = list(vs) + [vs[-1]]
        ax.step(xs, [y0 + 0.9 * v for v in ys], where="post", color=col, lw=2)
        ax.text(-3, y0 + 0.45, lab, ha="right", va="center", color=INK)
        # value annotation in each segment
        for k in range(len(ts)):
            t1 = ts[k + 1] if k + 1 < len(ts) else t_end
            ax.text((ts[k] + t1) / 2, y0 + 0.9 * vs[k] + (0.12 if vs[k] == 0 else -0.32),
                    str(vs[k]), ha="center", fontsize=7.5, color=MUTED)
    for t in range(0, t_end + 1, step):
        ax.axvline(t, color="#dddddd", lw=0.8, zorder=0)
    ytop = (n - 1) * 1.6 + 1.25
    for k, lab in enumerate(case_labels):
        ax.text(k * step + step / 2, ytop, lab, ha="center", va="bottom", fontsize=8.5, color=INK)
    ax.set_xlim(0, t_end); ax.set_ylim(-0.4, ytop + 0.9)
    ax.set_yticks([]); ax.set_xticks(range(0, t_end + 1, step))
    ax.set_xlabel("time (ns)    [" + top_note + "]")
    for s in ("left", "right", "top"): ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=11, loc="left")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, fname), dpi=200); plt.close(fig)

# ---------- full adder ----------
fa_cases = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
t = [20 * k for k in range(8)]
def fa_expected():
    A = [1 - x[0] for x in fa_cases]; B = [1 - x[1] for x in fa_cases]; C = [1 - x[2] for x in fa_cases]
    Sx = [1 - ((a + b + c) & 1) for a, b, c in fa_cases]; Co = [1 - (1 if a + b + c >= 2 else 0) for a, b, c in fa_cases]
    return A, B, C, Sx, Co
labels_fa = ["ABCin\n%d%d%d" % x for x in fa_cases]
A, B, C, Sx, Co = fa_expected()
note = "pin levels (active-low): key 0 = pressed, led 0 = on"
timing("fa_expected.png", "Expected waveform (designed before coding)", 160, 20,
       [("key_a", t, A, IN_C), ("key_b", t, B, IN_C), ("key_cin", t, C, IN_C),
        ("led_s", t, Sx, OUT_C), ("led_cout", t, Co, OUT_C)], labels_fa, note)
r = read_csv(os.path.join(S, "sim", "full_adder_tb.csv"))
ts = [int(x["Time"]) for x in r]
g = lambda k: [int(x["full_adder_tb." + k]) for x in r]
timing("fa_sim.png", "Simulated waveform (from full_adder_tb.vcd)", 160, 20,
       [("key_a", ts, g("key_a"), IN_C), ("key_b", ts, g("key_b"), IN_C), ("key_cin", ts, g("key_cin"), IN_C),
        ("led_s", ts, g("led_s"), OUT_C), ("led_cout", ts, g("led_cout"), OUT_C)], labels_fa, note)
assert g("led_s") == Sx and g("led_cout") == Co and g("key_a") == A

# ---------- comparator ----------
cp_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
t = [20 * k for k in range(4)]
A = [1 - a for a, b in cp_cases]; B = [1 - b for a, b in cp_cases]
LT = [0 if a < b else 1 for a, b in cp_cases]; EQ = [0 if a == b else 1 for a, b in cp_cases]; GT = [0 if a > b else 1 for a, b in cp_cases]
labels_cp = ["AB=%d%d\n%s" % (a, b, "A=B" if a == b else ("A<B" if a < b else "A>B")) for a, b in cp_cases]
timing("cp_expected.png", "Expected waveform (designed before coding)", 80, 20,
       [("key_a", t, A, IN_C), ("key_b", t, B, IN_C), ("led_lt", t, LT, OUT_C),
        ("led_eq", t, EQ, OUT_C), ("led_gt", t, GT, OUT_C)], labels_cp, note)
r = read_csv(os.path.join(S, "sim", "comparator_1bit_tb.csv"))
ts = [int(x["Time"]) for x in r]
g = lambda k: [int(x["comparator_1bit_tb." + k]) for x in r]
timing("cp_sim.png", "Simulated waveform (from comparator_1bit_tb.vcd)", 80, 20,
       [("key_a", ts, g("key_a"), IN_C), ("key_b", ts, g("key_b"), IN_C), ("led_lt", ts, g("led_lt"), OUT_C),
        ("led_eq", ts, g("led_eq"), OUT_C), ("led_gt", ts, g("led_gt"), OUT_C)], labels_cp, note)
assert g("led_lt") == LT and g("led_eq") == EQ and g("led_gt") == GT

# ---------- block diagrams ----------
def block(fname, mod, ins, outs, inner, pins_in, pins_out):
    fig, ax = plt.subplots(figsize=(9, 3.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax.add_patch(FancyBboxPatch((3.6, 0.5), 2.8, 3.0, boxstyle="round,pad=0.02", fc="#f4f6fa", ec=INK, lw=1.5))
    ax.text(5.0, 3.2, mod, ha="center", fontsize=11, weight="bold")
    for k, line in enumerate(inner):
        ax.text(5.0, 2.55 - 0.42 * k, line, ha="center", fontsize=8.5, family="DejaVu Sans Mono")
    ax.text(5.0, 0.7, "combinational, no clock", ha="center", fontsize=8, color=MUTED)
    def side(names, pins, xbox, xedge, left):
        n = len(names); ys = [2.0 + (n - 1) * 0.55 - 1.1 * k for k in range(n)] if n > 1 else [2.0]
        ys = [2.0 + 0.55 * (n - 1) - 1.1 * k * (2 / max(n - 1, 1)) * (n - 1) / 2 for k in range(n)]
        for nm, pin, y in zip(names, pins, ys):
            ax.add_patch(FancyBboxPatch((xbox, y - 0.25), 1.5, 0.5, boxstyle="round,pad=0.02",
                                        fc="white", ec=IN_C if left else OUT_C, lw=1.3))
            ax.text(xbox + 0.75, y, pin, ha="center", va="center", fontsize=8.5)
            x0, x1 = (xbox + 1.5, xedge) if left else (xedge, xbox)
            ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=12, color=INK, lw=1.2))
            ax.text((x0 + x1) / 2, y + 0.1, nm, ha="center", va="bottom", fontsize=8.5)
    side(ins, pins_in, 0.4, 3.6, True); side(outs, pins_out, 8.1, 6.4, False)
    ax.text(1.15, 3.75, "Buttons (active-low)", ha="center", fontsize=9, color=IN_C)
    ax.text(8.85, 3.75, "LEDs (active-low)", ha="center", fontsize=9, color=OUT_C)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, fname), dpi=200); plt.close(fig)

block("fa_block.png", "full_adder", ["a", "b", "cin"], ["s", "cout"],
      ["s    = a ^ b ^ cin", "cout = a&b | a&cin | b&cin"],
      ["B2 (KEY1)", "B3 (KEY2)", "B4 (KEY3)"], ["led1 (LED0)", "led2 (LED1)"])
block("cp_block.png", "comparator_1bit", ["a", "b"], ["lt", "eq", "gt"],
      ["lt = ~a | b", "eq =  a ^ b", "gt =  a | ~b"],
      ["B2 (KEY1)", "B3 (KEY2)"], ["led1 (LED0)", "led2 (LED1)", "led3 (LED2)"])
print("ok")
