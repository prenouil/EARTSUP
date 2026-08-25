---
name: facettes-exemples-jeux
description: Facettes des cartes d'exemple de jeu — préférer genre + taille/budget + "type de vue" (tag court et évocateur) plutôt qu'éditeur/studio et plateforme.
metadata:
  type: feedback
---

Dans les cartes `.example-card` (`example-grid`), l'utilisateur préfère ne PAS afficher l'éditeur/studio ni la plateforme comme facettes. Il garde le genre et la taille/budget, et ajoute un tag "type de vue" : un mot ou une expression courte et évocatrice (2D, FPS, TPS Action, Isométrique, Verticalité, Mignon, Plans fixes, Vue du dessus...) qui capture soit l'angle caméra soit une esthétique/sensation marquante de gameplay — pas une catégorie rigide.

**Pourquoi :** L'éditeur/studio et la plateforme n'apportent rien de pédagogique dans ce contexte ; un tag de type de vue est plus parlant visuellement et aide les étudiants à se projeter dans le jeu (cf. retouche de la section "Notions clés — les familles de designer" du support Remise à niveau Bachelor 3, où toutes les cartes sont passées de 4 facettes éditeur/plateforme/genre/taille à 3 facettes genre/taille/type de vue).

**Comment l'appliquer :** Pour toute nouvelle carte d'exemple de jeu ou refonte d'une section existante avec ce composant, structurer les facettes comme `<span>genre</span><span>taille ou budget</span><span>type de vue</span>` (l'ordre des deux premières spans reste tel quel, le type de vue est ajouté en dernier). Ne pas ajouter éditeur/studio/plateforme sauf demande explicite contraire. Inventer un tag cohérent avec le jeu réel si l'utilisateur ne le précise pas, dans le même esprit concis et un peu accrocheur que ses propres exemples.
