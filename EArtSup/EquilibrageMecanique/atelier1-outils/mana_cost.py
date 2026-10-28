import itertools
import numpy as np

def combatants(total):
    result = []
    for f in range(1, total - 1):
        for pv in range(1, total - f):
            init = total - f - pv
            if init >= 1:
                result.append((f, pv, init))
    return result

def fight(c1, c2):
    f1, pv1, i1 = c1
    f2, pv2, i2 = c2
    hp1, hp2 = pv1, pv2
    if i1 == i2:
        while hp1 > 0 and hp2 > 0:
            hp1, hp2 = hp1 - f2, hp2 - f1
        if hp1 <= 0 and hp2 <= 0:
            return 0
        return 1 if hp1 > 0 else 2
    else:
        attacker_is_1 = i1 > i2
        while True:
            if attacker_is_1:
                hp2 -= f1
                if hp2 <= 0:
                    return 1
                hp1 -= f2
                if hp1 <= 0:
                    return 2
            else:
                hp1 -= f2
                if hp1 <= 0:
                    return 2
                hp2 -= f1
                if hp2 <= 0:
                    return 1

def win_rates(total):
    combs = combatants(total)
    stats = {c: [0, 0, 0] for c in combs}
    for c1, c2 in itertools.product(combs, combs):
        if c1 == c2:
            continue
        r = fight(c1, c2)
        if r == 1:
            stats[c1][0] += 1; stats[c2][1] += 1
        elif r == 2:
            stats[c2][0] += 1; stats[c1][1] += 1
        else:
            stats[c1][2] += 1; stats[c2][2] += 1
    out = {}
    for c, (w, l, d) in stats.items():
        n = w + l + d
        out[c] = w / n
    return out

TOTAL = 10
wr = win_rates(TOTAL)
combs = sorted(wr.keys())

# --- Cout en mana : rescale lineaire du taux de victoire sur une echelle 1-7 (classique TCG) ---
rates = np.array([wr[c] for c in combs])
rmin, rmax = rates.min(), rates.max()
mana = 1 + 6 * (rates - rmin) / (rmax - rmin)   # 1 .. 7
mana_rounded = np.round(mana).astype(int)

print(f"=== Cout en mana (echelle 1-7) pour les {len(combs)} combattants (total={TOTAL}) ===")
print(f"{'Force':>5} {'PV':>4} {'Init':>5} {'TauxV':>7} {'Mana(brut)':>11} {'Mana':>5}")
order = sorted(range(len(combs)), key=lambda i: -rates[i])
for i in order:
    f, pv, init = combs[i]
    print(f"{f:>5} {pv:>4} {init:>5} {rates[i]*100:>6.1f}% {mana[i]:>11.2f} {mana_rounded[i]:>5}")

# --- Regression : approcher le taux de victoire par une formule des stats brutes ---
F = np.array([c[0] for c in combs], dtype=float)
PV = np.array([c[1] for c in combs], dtype=float)
I = np.array([c[2] for c in combs], dtype=float)
y = rates

def fit_and_report(name, X, labels):
    coeffs, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coeffs
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    print(f"\n--- Modele : {name}  (R^2 = {r2:.4f}) ---")
    for lab, c in zip(labels, coeffs):
        print(f"  {lab:>10} : {c: .5f}")
    return coeffs, r2

# Modele lineaire simple : prix = a*F + b*PV + c*Init + d
X_lin = np.column_stack([np.ones_like(F), F, PV, I])
fit_and_report("lineaire (1, F, PV, Init)", X_lin, ["const", "F", "PV", "Init"])

# Modele quadratique complet (avec interactions)
X_quad = np.column_stack([
    np.ones_like(F), F, PV, I,
    F**2, PV**2, I**2,
    F*PV, F*I, PV*I
])
coeffs_q, r2_q = fit_and_report(
    "quadratique complet (1, F, PV, I, F^2, PV^2, I^2, F*PV, F*I, PV*I)",
    X_quad,
    ["const", "F", "PV", "I", "F^2", "PV^2", "I^2", "F*PV", "F*I", "PV*I"]
)

# Modele quadratique reduit (sans interactions, juste les carres)
X_quad_simple = np.column_stack([np.ones_like(F), F, PV, I, F**2, PV**2, I**2])
fit_and_report(
    "quadratique simple (1, F, PV, I, F^2, PV^2, I^2)",
    X_quad_simple,
    ["const", "F", "PV", "I", "F^2", "PV^2", "I^2"]
)
