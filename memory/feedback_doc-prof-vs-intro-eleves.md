---
name: feedback-doc-prof-vs-intro-eleves
description: Un même atelier peut avoir deux supports distincts — un doc de préparation pédagogique pour l'encadrant, et une présentation de lancement pour les élèves — avec un ton différent mais le même gabarit visuel.
metadata:
  type: feedback
---

Quand un atelier existant n'a qu'un document de préparation pédagogique (destiné à l'enseignant : horaires indicatifs, points de vigilance, grille d'évaluation, matériel à prévoir), un second document distinct peut être demandé pour le jour de lancement, destiné directement aux élèves. Les deux coexistent et ne se remplacent pas.

**Pourquoi :** demande explicite sur l'Atelier Jeux de Plateau — garder `atelier-jeux-de-plateau.html` (prépa encadrant) intact et créer `atelier-jeux-de-plateau-intro.html` à côté, pour la présentation faite aux élèves le jour J.

**Comment l'appliquer :**
- Même système visuel (polices, palette, composants CSS) pour la cohérence entre les deux documents.
- Ton différent : le doc encadrant reste neutre/technique (notes de production, grille d'évaluation, points de vigilance) ; le doc élèves est plus punchy/motivant, avec des exemples concrets qui illustrent les consignes (ex. comparer une "mauvaise" interprétation d'une consigne et une "bonne" via un composant `.compare` à deux colonnes) plutôt que de la décrire abstraitement.
- Si le brief jour-par-jour n'est pas détaillé dans la demande (ex. un atelier qui passe de 5 à 10 jours), répartir en gardant la logique des phases déjà actées plutôt qu'en inventer de nouvelles, et signaler explicitement l'hypothèse de répartition dans le rapport de livraison pour correction.
- Vérifier les données chiffrées (marché, salons, historique) par recherche web plutôt que les inventer, et donner des ordres de grandeur sourcés quand les chiffres varient selon la source.
