---
name: feedback-export-pdf
description: Méthode validée pour livrer un support wiki en version PDF partageable, avec sauts de page ciblés sur les ruptures logiques.
metadata:
  type: feedback
---

Quand l'utilisateur demande "une version partageable pdf" :

1. Ajouter une feuille de style `@media print` au document (masquer `.toc`, passer `.layout` en une seule colonne, `background-image:none`, `break-inside:avoid-page` sur `section` et `.seq`).
2. Ajouter une classe utilitaire `.pb-before { break-before:page; page-break-before:always; }` et l'appliquer aux points de rupture logique désignés par l'utilisateur (ex. début d'un nouveau sous-thème dense, début d'une nouvelle séquence, clôture) — pas systématiquement à chaque section.
3. Générer le PDF en headless depuis le fichier HTML local (pas depuis l'URL publiée) :
   `chrome.exe --headless=new --disable-gpu --no-sandbox --print-to-pdf="sortie.pdf" --no-pdf-header-footer "file:///chemin/vers/fichier.html"`
   (Edge fonctionne aussi avec les mêmes flags si Chrome est absent.)
4. Déposer une copie sur le Bureau (`C:\Users\user\Desktop\`) avec un nom de fichier lisible, en plus du fichier de travail — c'est ce que l'utilisateur considère comme "partageable", pas un chemin temporaire.
5. Republier l'artifact avec les mêmes styles d'impression, pour que la version en ligne et le PDF restent synchronisés.

**Pourquoi :** demande explicite après validation du contenu de "Écosystème du jeu vidéo", puis ajustement des points de rupture ("Saut de page au niveau de : ...").

**Comment l'appliquer :** à chaque fois qu'un support atteint un état validé par l'utilisateur ("je suis satisfait du résultat"), proposer spontanément l'export PDF si l'utilisateur mentionne vouloir le partager ou l'imprimer.
