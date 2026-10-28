import itertools
from collections import defaultdict

def combatants():
    """Toutes les repartitions de 10 points en Force/PV/Init, chaque stat >= 1."""
    result = []
    for f in range(1, 9):
        for pv in range(1, 10 - f):
            init = 10 - f - pv
            if init >= 1:
                result.append((f, pv, init))
    return result

def fight(c1, c2):
    """Retourne 1 si c1 gagne, 2 si c2 gagne, 0 si egalite (double KO simultane)."""
    f1, pv1, i1 = c1
    f2, pv2, i2 = c2
    hp1, hp2 = pv1, pv2

    if i1 == i2:
        # frappes simultanees chaque round
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

combs = combatants()
print(f"Nombre de combattants distincts (F,PV,Init >=1, somme=10) : {len(combs)}")
print()

stats = {}  # combattant -> [wins, losses, draws]
for c in combs:
    stats[c] = [0, 0, 0]

total_matches = 0
for c1, c2 in itertools.product(combs, combs):
    if c1 == c2:
        continue  # on ignore le miroir exact (toujours nul par symetrie, non informatif)
    total_matches += 1
    result = fight(c1, c2)
    if result == 1:
        stats[c1][0] += 1
        stats[c2][1] += 1
    elif result == 2:
        stats[c2][0] += 1
        stats[c1][1] += 1
    else:
        stats[c1][2] += 1
        stats[c2][2] += 1

print(f"Total de confrontations simulees (hors miroirs) : {total_matches}")
print()

# Tableau complet trie par taux de victoire
print(f"{'Force':>5} {'PV':>4} {'Init':>5} {'V':>4} {'D':>4} {'N':>4} {'TauxV':>7}")
rows = []
for c, (w, l, d) in stats.items():
    n = w + l + d
    rate = w / n
    rows.append((c, w, l, d, rate))
rows.sort(key=lambda r: -r[4])
for c, w, l, d, rate in rows:
    f, pv, init = c
    print(f"{f:>5} {pv:>4} {init:>5} {w:>4} {l:>4} {d:>4} {rate*100:>6.1f}%")

print()
print("=== Analyse : importance relative de chaque stat ===")

# Moyenne du taux de victoire par valeur de chaque stat (toutes choses egales par ailleurs non isolees,
# mais une premiere vue agregee)
for label, idx in [("Force", 0), ("PV", 1), ("Initiative", 2)]:
    by_value = defaultdict(list)
    for c, w, l, d, rate in rows:
        by_value[c[idx]].append(rate)
    print(f"\n--- Taux de victoire moyen par valeur de {label} ---")
    for val in sorted(by_value):
        vals = by_value[val]
        avg = sum(vals) / len(vals)
        print(f"  {label} = {val:>2} : taux moyen = {avg*100:5.1f}%  (sur {len(vals)} combattants)")

# Correlation simple (Pearson) taux de victoire vs chaque stat
def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    return cov / (vx * vy) ** 0.5

rates = [r[4] for r in rows]
forces = [r[0][0] for r in rows]
pvs = [r[0][1] for r in rows]
inits = [r[0][2] for r in rows]

print()
print("=== Correlation (Pearson) entre chaque stat et le taux de victoire ===")
print(f"  Force      vs taux de victoire : r = {pearson(forces, rates): .3f}")
print(f"  PV         vs taux de victoire : r = {pearson(pvs, rates): .3f}")
print(f"  Initiative vs taux de victoire : r = {pearson(inits, rates): .3f}")
