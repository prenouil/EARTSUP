---
name: feedback-revue-veille-continuite
description: chaque séance (sauf la première) ouvre sur une revue calibrée du travail rendu la veille, en recalibrant le reste du séquençage à durée totale fixe
metadata:
  type: feedback
---

Dans un support wiki multi-séances où chaque séance se termine par un livrable "Après-midi" à rendre pour le lendemain, la séance suivante doit ouvrir (bloc en position 0:00 du `table.seq`) sur une revue de ce livrable, sauf la toute première séance du module (pas de veille).

**Pourquoi :** demande explicite de l'utilisateur sur le support "Remise à niveau — Bachelor 3 Game Design" (fichier `RemiseANiveau/remise-a-niveau.html`) — la continuité pédagogique entre séances doit être visible et exploitée, pas seulement mentionnée en fin de séance précédente.

**Comment l'appliquer :**
- Durée du bloc de revue entre 15 min et 1h, calibrée sur l'ampleur réelle du livrable (jugement de pédagogue, pas un forfait fixe) : un pitch oral rapide ~15 min ; une analyse écrite structurée (grille à plusieurs axes) ~30 min ; un double livrable écrit (ex. deux GDD) jusqu'à 45-60 min. Le format de revue (tour de table rapide, échanges croisés en binômes, présentation individuelle complète) doit lui-même s'adapter à la durée disponible.
- La durée totale affichée de la séance (`<div class="dur">`) ne change jamais — c'est une contrainte d'emploi du temps. Pour absorber le nouveau bloc, rogner quelques minutes (5-15) sur plusieurs blocs de contenu/transition les moins denses (intros, brefs de fin de séance, exemples secondaires), jamais sur l'exercice pratique central de la séance qui doit rester quasi intact.
- Recalculer tous les horaires en cascade après insertion et vérifier que la somme des durées de blocs égale exactement la durée totale affichée.
- Toujours proposer le recalibrage complet (durée du bloc + coupes + horaires en cascade) à valider avant d'éditer le fichier.
- Si une séance a déjà un bloc de restitution/retour qui joue ce rôle (ex. playtest croisé du prototype de la veille), ne pas dupliquer un bloc de revue — signaler que la séance est déjà couverte plutôt que de forcer un ajout.
