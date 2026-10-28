# Simulation de combat a 4 statistiques (Force / PV / Initiative / Defense)
# Extension de l'exercice 3 stats : meme budget total (10 points), 4eme stat Defense
# qui interagit MULTIPLICATIVEMENT avec la Force adverse (contrairement aux PV qui
# se soustraient simplement d'un pool) :
#   degats effectifs = max(1, Force_attaquant - Defense_defenseur)
# => la valeur d'un point de Defense depend de la Force de l'adversaire en face,
#    ce qu'un modele de cout purement additif ne peut pas capturer.

import itertools
import csv
import numpy as np

TOTAL = 10  # meme budget que l'exercice 3 stats

def combatants(total, n_stats=4):
    """Toutes les repartitions de `total` points en `n_stats` stats, chacune >= 1."""
    result = []
    def rec(remaining, slots, current):
        if slots == 1:
            if remaining >= 1:
                result.append(tuple(current + [remaining]))
            return
        for v in range(1, remaining - (slots - 1) + 1):
            rec(remaining - v, slots - 1, current + [v])
    rec(total, n_stats, [])
    return result

def fight(c1, c2):
    """c = (Force, PV, Init, Defense). Retourne 1, 2 ou 0 (egalite)."""
    f1, pv1, i1, d1 = c1
    f2, pv2, i2, d2 = c2
    hp1, hp2 = pv1, pv2
    dmg_1_to_2 = max(1, f1 - d2)
    dmg_2_to_1 = max(1, f2 - d1)

    if i1 == i2:
        while hp1 > 0 and hp2 > 0:
            hp1, hp2 = hp1 - dmg_2_to_1, hp2 - dmg_1_to_2
        if hp1 <= 0 and hp2 <= 0:
            return 0
        return 1 if hp1 > 0 else 2
    else:
        attacker_is_1 = i1 > i2
        while True:
            if attacker_is_1:
                hp2 -= dmg_1_to_2
                if hp2 <= 0:
                    return 1
                hp1 -= dmg_2_to_1
                if hp1 <= 0:
                    return 2
            else:
                hp1 -= dmg_2_to_1
                if hp1 <= 0:
                    return 2
                hp2 -= dmg_1_to_2
                if hp2 <= 0:
                    return 1

combs = combatants(TOTAL, 4)
print(f"Nombre de combattants distincts (4 stats, total={TOTAL}, chacune >=1) : {len(combs)}")

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

win_rate = {c: w / (w + l + d) for c, (w, l, d) in stats.items()}

rates = np.array([win_rate[c] for c in combs])
rmin, rmax = rates.min(), rates.max()
mana = 1 + 6 * (rates - rmin) / (rmax - rmin)
mana_rounded = np.round(mana).astype(int)

# --- Export CSV pour le tableur des eleves ---
out_path = r"C:\Users\user\AppData\Local\Temp\claude\c--Claude-EARTSUP\9e6dcd0f-c025-45ae-aca5-c6825f59ab76\scratchpad\combat-sim\combattants_4stats.csv"
with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Force", "PV", "Initiative", "Defense", "Victoires", "Defaites", "Nuls",
                "TauxVictoire", "CoutManaBrut", "CoutMana"])
    order = sorted(range(len(combs)), key=lambda i: -rates[i])
    for i in order:
        c = combs[i]
        wn, ln, dn = stats[c]
        w.writerow([c[0], c[1], c[2], c[3], wn, ln, dn,
                    round(rates[i] * 100, 1), round(mana[i], 2), mana_rounded[i]])
print(f"CSV exporte : {out_path}")

# --- Resume rapide + verification de l'hypothese d'interaction ---
print(f"\nMeilleur profil : {combs[order[0]]}  taux={rates[order[0]]*100:.1f}%")
print(f"Pire profil     : {combs[order[-1]]}  taux={rates[order[-1]]*100:.1f}%")

F = np.array([c[0] for c in combs], dtype=float)
PV = np.array([c[1] for c in combs], dtype=float)
I = np.array([c[2] for c in combs], dtype=float)
D = np.array([c[3] for c in combs], dtype=float)
y = rates

def r2(X):
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coeffs
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot, coeffs

print("\n--- Verification : la Defense a-t-elle besoin d'un terme d'interaction avec la Force ? ---")
X_no_interaction = np.column_stack([np.ones_like(F), F, PV, I, D, F**2, PV**2, I**2, D**2])
r2_no, _ = r2(X_no_interaction)
print(f"R^2 SANS interaction F*D : {r2_no:.4f}")

X_with_interaction = np.column_stack([np.ones_like(F), F, PV, I, D, F**2, PV**2, I**2, D**2, F*D])
r2_with, _ = r2(X_with_interaction)
print(f"R^2 AVEC interaction F*D : {r2_with:.4f}")
print(f"Gain de R^2 du seul fait d'ajouter F*D : {r2_with - r2_no:+.4f}")
