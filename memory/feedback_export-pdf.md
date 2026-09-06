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
4. Déposer une copie dans `C:\Claude\EARTSUP\Pdf\` (pas le scratchpad de session, pas le Bureau) avec un nom de fichier lisible et cohérent avec le support d'origine (ex. `remise-a-niveau.pdf`, `atelier-dev-mobile.pdf`), en plus du fichier de travail — c'est ce que l'utilisateur considère comme "partageable", pas un chemin temporaire.
5. Republier l'artifact avec les mêmes styles d'impression, pour que la version en ligne et le PDF restent synchronisés.
6. Pour un support construit en onglets JS (`.page{display:none}` + `.page.active{display:block}`, ex. Remise à niveau) plutôt qu'en défilement continu : ne pas modifier le fichier source. Travailler sur une copie temporaire avec une règle `@media print{ .page{display:block!important} .page + .page{page-break-before:always} }` (et masquer sidebar/notes/pagenav en print), générer le PDF depuis cette copie, puis la supprimer — seul le PDF final va dans `Pdf\`.

**Pourquoi :** demande explicite après validation du contenu de "Écosystème du jeu vidéo", puis ajustement des points de rupture ("Saut de page au niveau de : ..."). L'emplacement `C:\Claude\EARTSUP\Pdf\` a remplacé le Bureau suite à une demande ultérieure de l'utilisateur ("dorénavant" tous les PDF vont là).

**Comment l'appliquer :** à chaque fois qu'un support atteint un état validé par l'utilisateur ("je suis satisfait du résultat"), proposer spontanément l'export PDF si l'utilisateur mentionne vouloir le partager ou l'imprimer. Dès qu'un nouveau support de cours durable est créé, prévoir aussi son export PDF vers `Pdf\` sans attendre que l'utilisateur le redemande à chaque fois.

**Fusionner deux pages logiques en une seule page imprimée (ex. "fusionne la page 2 et la page 3") :**
1. Générer d'abord un PDF de la version actuelle (méthode ci-dessus, headless Chrome/Edge) et le relire pour identifier précisément quelles sections tombent sur quelle page — ne jamais deviner la pagination à partir du seul code source, `break-inside:avoid-page` et le remplissage naturel des pages rendent ça peu prévisible.
2. Retirer le `.pb-before` séparateur s'il y en a un entre les deux blocs visés.
3. Si les deux blocs ne tiennent toujours pas ensemble après ça, gagner de la place sans couper de contenu en changeant le layout d'empilement vertical (`.stack-cards`, une carte sous l'autre) en grille horizontale (`.col-grid.col-grid--3` ou équivalent) quand le nombre de cartes s'y prête — un simple changement de classe CSS, pas une réécriture de contenu.
4. Si l'espace manque encore, condenser légèrement le texte des puces (couper les clauses secondaires, garder l'info centrale) plutôt que supprimer des puces entières.
5. Toujours regénérer un second PDF après les changements pour confirmer la fusion avant de considérer la tâche terminée.

**Piège rencontré :** la copie locale d'un support (`C:\Claude\EARTSUP\EArtSup\...\*.html`) peut avoir été écrasée par le HTML complet rendu de l'artifact (préambule `frame-runtime`, wrapper `<!doctype><html><head>...<body>` autour du contenu) au lieu de rester la source propre (juste `<title>`, `<style>`, contenu du body). Avant d'éditer un fichier local existant, vérifier qu'il commence bien par `<title>` et pas par `<!doctype html><html><head><!-- frame-runtime -->` — si contaminé, extraire le contenu utile (tout après `<body>` jusqu'à avant `</body></html>`) et retravailler dessus.
