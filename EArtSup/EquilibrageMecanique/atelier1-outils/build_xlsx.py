# Construit le tableur Excel pour l'Atelier 1 (variante 4e stat Defense).
# Les eleves manipulent les formules de regression (LINEST) eux-memes dans
# l'onglet "Regression" pour observer le R^2 evoluer -- c'est le coeur de
# l'exercice, donc le tableur fournit les DONNEES deja calculees (round-robin)
# mais PAS la regression finale toute faite.

import itertools
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

TOTAL = 10

def combatants(total, n_stats=4):
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
    f1, pv1, i1, d1 = c1
    f2, pv2, i2, d2 = c2
    hp1, hp2 = pv1, pv2
    dmg12 = max(1, f1 - d2)
    dmg21 = max(1, f2 - d1)
    if i1 == i2:
        while hp1 > 0 and hp2 > 0:
            hp1, hp2 = hp1 - dmg21, hp2 - dmg12
        if hp1 <= 0 and hp2 <= 0:
            return 0
        return 1 if hp1 > 0 else 2
    else:
        attacker_is_1 = i1 > i2
        while True:
            if attacker_is_1:
                hp2 -= dmg12
                if hp2 <= 0: return 1
                hp1 -= dmg21
                if hp1 <= 0: return 2
            else:
                hp1 -= dmg21
                if hp1 <= 0: return 2
                hp2 -= dmg12
                if hp2 <= 0: return 1

combs = combatants(TOTAL, 4)
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

order = sorted(combs, key=lambda c: -(stats[c][0] / sum(stats[c])))

wb = openpyxl.Workbook()

# ---------- Onglet Lisez-moi ----------
ws0 = wb.active
ws0.title = "Lisez-moi"
title_font = Font(bold=True, size=14)
h2_font = Font(bold=True, size=12)
wrap = Alignment(wrap_text=True, vertical="top")

ws0["A1"] = "Atelier 1 — Construire sa baseline depuis zéro (variante Défense)"
ws0["A1"].font = title_font
ws0.column_dimensions["A"].width = 100

lines = [
    "",
    "CONTEXTE",
    "Dans l'exercice de cours, on a montré que Force / PV / Initiative n'ont pas la même valeur "
    "dans un système de combat à 10 points. Un modèle de coût LINÉAIRE (cout = a·F + b·PV + c·Init) "
    "n'expliquait que 25% de la puissance réelle (R²=0,25). Un modèle QUADRATIQUE (avec F², PV², Init²) "
    "expliquait 93% (R²=0,93).",
    "",
    "LE PROBLÈME DE CET ATELIER",
    "On ajoute une 4e statistique : la DÉFENSE. Elle ne fonctionne pas comme les autres : elle réduit "
    "les dégâts reçus d'un combat à l'autre (dégâts effectifs = max(1, Force attaquant - Défense défenseur)). "
    "Sa valeur dépend donc de la Force de l'adversaire en face — c'est une INTERACTION, pas un effet isolé.",
    "",
    "VOTRE TÂCHE",
    "1. Ouvrez l'onglet 'Données' : 84 combattants (Force/PV/Init/Défense répartis sur 10 points, "
    "chaque stat >= 1), déjà confrontés les uns aux autres (6972 combats simulés), avec leur taux de "
    "victoire réel en colonne P.",
    "2. Ouvrez l'onglet 'Régression'. Quatre modèles y sont préparés, chacun avec une formule LINEST "
    "qui calcule le R² (qualité de prédiction) pour un jeu de colonnes prédictives différent :",
    "   - Modèle 1 : F, PV, Init, Défense (linéaire simple)",
    "   - Modèle 2 : + les carrés de chaque stat (quadratique, sans interaction)",
    "   - Modèle 3 : + le terme d'interaction Force × Défense",
    "   - Modèle 4 : + trois autres interactions 'au hasard' (Force×PV, Init×Défense, PV×Défense)",
    "3. Observez l'évolution du R² d'un modèle à l'autre. Notez où le gain est réel et où il ne l'est pas.",
    "4. Dans l'onglet 'Régression', ligne 'Votre conclusion', répondez en une phrase : pourquoi le "
    "modèle 3 apporte un vrai gain alors que les interactions du modèle 4 n'en apportent (presque) pas ?",
    "5. Pour aller plus loin : copiez un bloc de formule LINEST et essayez vos propres combinaisons de "
    "colonnes (onglet Données, colonnes E à L) pour voir si vous trouvez un modèle encore meilleur.",
    "",
    "Les colonnes E à L de l'onglet Données sont déjà calculées (carrés et produits croisés) pour que "
    "vous puissiez construire vos propres plages sans recalculer à la main.",
]
r = 2
for line in lines:
    cell = ws0.cell(row=r, column=1, value=line)
    if line and not line.startswith(" ") and line.isupper() is False and line in (
        "CONTEXTE", "LE PROBLÈME DE CET ATELIER", "VOTRE TÂCHE"
    ):
        pass
    if line in ("CONTEXTE", "LE PROBLÈME DE CET ATELIER", "VOTRE TÂCHE"):
        cell.font = h2_font
    cell.alignment = wrap
    ws0.row_dimensions[r].height = 15 if len(line) < 80 else 30
    r += 1

# ---------- Onglet Données ----------
ws1 = wb.create_sheet("Données")
headers = ["Force", "PV", "Initiative", "Defense",
           "F^2", "PV^2", "Init^2", "Def^2",
           "F x Def", "F x PV", "Init x Def", "PV x Def",
           "Victoires", "Defaites", "Nuls", "TauxVictoire"]
for j, h in enumerate(headers, start=1):
    c = ws1.cell(row=1, column=j, value=h)
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="24211B")
    c.font = Font(bold=True, color="FFFFFF")

for i, comb in enumerate(order, start=2):
    f, pv, init, d = comb
    w, l, dr = stats[comb]
    n = w + l + dr
    ws1.cell(row=i, column=1, value=f)
    ws1.cell(row=i, column=2, value=pv)
    ws1.cell(row=i, column=3, value=init)
    ws1.cell(row=i, column=4, value=d)
    ws1.cell(row=i, column=5, value=f"=A{i}^2")
    ws1.cell(row=i, column=6, value=f"=B{i}^2")
    ws1.cell(row=i, column=7, value=f"=C{i}^2")
    ws1.cell(row=i, column=8, value=f"=D{i}^2")
    ws1.cell(row=i, column=9, value=f"=A{i}*D{i}")
    ws1.cell(row=i, column=10, value=f"=A{i}*B{i}")
    ws1.cell(row=i, column=11, value=f"=C{i}*D{i}")
    ws1.cell(row=i, column=12, value=f"=B{i}*D{i}")
    ws1.cell(row=i, column=13, value=w)
    ws1.cell(row=i, column=14, value=l)
    ws1.cell(row=i, column=15, value=dr)
    ws1.cell(row=i, column=16, value=f"=M{i}/(M{i}+N{i}+O{i})")

last_row = len(order) + 1
for col in range(1, 17):
    ws1.column_dimensions[get_column_letter(col)].width = 10

# ---------- Onglet Regression ----------
ws2 = wb.create_sheet("Regression")
ws2.column_dimensions["A"].width = 45
ws2.column_dimensions["B"].width = 16
ws2.column_dimensions["C"].width = 60

ws2["A1"] = "Modèle"
ws2["B1"] = "R² (qualité de prédiction)"
ws2["C1"] = "Colonnes utilisées (onglet Données)"
for cell in ("A1", "B1", "C1"):
    ws2[cell].font = Font(bold=True)

rows_def = [
    ("Modèle 1 — linéaire simple", f"Données!A2:D{last_row}", "A:D  (F, PV, Init, Def)"),
    ("Modèle 2 — quadratique sans interaction", f"Données!A2:H{last_row}", "A:H  (+ F², PV², Init², Def²)"),
    ("Modèle 3 — + interaction Force x Defense", f"Données!A2:I{last_row}", "A:I  (+ F x Def)"),
    ("Modèle 4 — + 3 interactions supplémentaires", f"Données!A2:L{last_row}", "A:L  (+ F x PV, Init x Def, PV x Def)"),
]
r = 2
for label, xrange, desc in rows_def:
    ws2.cell(row=r, column=1, value=label)
    ws2.cell(row=r, column=2, value=f"=INDEX(LINEST(Données!$P$2:$P${last_row},{xrange},TRUE,TRUE),3,1)")
    ws2.cell(row=r, column=3, value=desc)
    r += 1

r += 1
ws2.cell(row=r, column=1, value="Gain R² du Modèle 2 au Modèle 3 (ajout F x Def) :").font = Font(bold=True)
ws2.cell(row=r, column=2, value=f"=B4-B3")
r += 1
ws2.cell(row=r, column=1, value="Gain R² du Modèle 3 au Modèle 4 (3 interactions 'au hasard') :").font = Font(bold=True)
ws2.cell(row=r, column=2, value=f"=B5-B4")

r += 3
ws2.cell(row=r, column=1, value="Votre conclusion (à compléter en classe) :").font = Font(bold=True)
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 4, end_column=3)
ws2.cell(row=r + 1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
ws2.cell(row=r + 1, column=1).fill = PatternFill("solid", fgColor="F4F1E8")

wb.active = 0
out = r"C:\Users\user\AppData\Local\Temp\claude\c--Claude-EARTSUP\9e6dcd0f-c025-45ae-aca5-c6825f59ab76\scratchpad\combat-sim\atelier1_defense.xlsx"
wb.save(out)
print("Workbook saved:", out)
print("Combattants:", len(combs), "  derniere ligne de donnees:", last_row)
