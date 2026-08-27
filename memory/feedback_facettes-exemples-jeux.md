---
name: facettes-exemples-jeux
description: Facettes des cartes d'exemple de jeu — garder studio/éditeur ET plateforme, en plus du genre, de la taille/budget et du "type de vue".
metadata:
  type: feedback
---

Dans les cartes `.example-card` (`example-grid`), l'utilisateur veut TOUJOURS afficher le studio/éditeur et la plateforme comme facettes, en plus du genre, de la taille/budget, et du tag "type de vue" : un mot ou une expression courte et évocatrice (2D, FPS, TPS Action, Isométrique, Verticalité, Mignon, Plans fixes, Vue du dessus...) qui capture soit l'angle caméra soit une esthétique/sensation marquante de gameplay — pas une catégorie rigide.

**Historique :** une préférence inverse (retirer studio/éditeur et plateforme) avait été appliquée une seule fois, sur la section "Notions clés — les familles de designer" du support Remise à niveau Bachelor 3. L'utilisateur est revenu dessus : "c'est une donnée importante que tu indiques à chaque fois." Studio/éditeur et plateforme ont été restaurés sur cette section (en gardant le tag "type de vue" ajouté entre-temps), et cette règle s'applique maintenant partout, y compris pour toute nouvelle carte à créer.

**Comment l'appliquer :** structurer les facettes comme `<span>studio/éditeur</span><span>plateforme</span><span>genre</span><span>taille ou budget</span><span>type de vue</span>` — 5 facettes dans cet ordre. Ne plus jamais retirer studio/éditeur ou plateforme sans confirmation explicite de l'utilisateur, même si une demande ponctuelle de simplification est faite sur une section précise — vérifier d'abord si elle doit s'appliquer partout ou seulement à l'endroit demandé.
