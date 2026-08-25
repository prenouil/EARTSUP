---
name: feedback-accueil-epure
description: Sur la page Accueil d'un wiki de cours, ne garder que le déroulé du cours (titre, vue d'ensemble des séances, semaines) — retirer contexte pédagogique, mode d'emploi du wiki et marqueurs de modulabilité.
metadata:
  type: feedback
---

Sur la page "Accueil" (section `id="page-accueil"`) d'un support wiki, l'utilisateur veut retirer :
- le callout "Contexte" qui explique la genèse pédagogique du module (pourquoi ce cours existe, diagnostic des années précédentes, etc.) ;
- la section "Comment utiliser ce wiki" (mode d'emploi du support lui-même : structure des pages, notes personnelles, légende des badges) ;
- les marqueurs de "modulabilité" d'une séance (badge ⚙️ en `span.flex-flag` dans les tableaux d'aperçu ET dans les crumbs `⚙️ modulable` sur les pages de séance concernées, plus toute mention textuelle "modulable"/"diagnostic... modulables").

Quand un badge/notion est retiré, vérifier tout le document (toutes les pages du wiki, pas seulement l'Accueil) pour éliminer les occurrences orphelines, et retirer la règle CSS associée (ex. `.flex-flag`) si elle n'est plus utilisée nulle part après nettoyage.

**Pourquoi :** demande explicite sur "Remise à niveau — Bachelor 3 Game Design" — l'Accueil ne doit garder que ce qui concerne le déroulé du cours (titre, vue d'ensemble des séances, semaines), pas le contexte pédagogique interne ni les instructions d'usage du wiki ni les marqueurs de flexibilité de planning.

**Comment l'appliquer :** par défaut, sur toute page "Accueil" d'un wiki de cours, ne pas y placer de notes d'intention pédagogique, de mode d'emploi du support, ni de badges de modulabilité — les réserver, si nécessaire, aux pages de séance individuelles ou à une discussion hors-support avec l'utilisateur. Si l'utilisateur demande à retirer un concept transversal (comme "modulable"), toujours grep tout le document (styles inclus) avant de republier.
