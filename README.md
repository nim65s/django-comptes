Comptes
=======
[![Build Status](https://travis-ci.org/nim65s/django-comptes.svg?branch=master)](https://travis-ci.org/nim65s/django-comptes)
[![Coverage Status](https://coveralls.io/repos/github/nim65s/django-comptes/badge.svg?branch=master)](https://coveralls.io/github/nim65s/django-comptes?branch=master)


But
---
Ceci est une application de gestion de petits comptes entre amis, nottament pour des occasions précises, telles qu’une semaine de vacances… Ou de dur labeur à la Ferté Bernard.

Principe
--------
Quand quelqu’un règle pour quelque chose qui bénéficie à plusieurs personne, comme un pot de Nutella ou la facture d’une Pizzeria, on l’entre comme une «Dette».

L’application calcule alors un «Solde», où la banque est en fait le groupe de personne : un solde positif indique que le groupe nous doit de l’argent (c’est toujours bien, un solde positif…)

Pour rééquilibrer la balance (ou toute autre raison), on peut également entrer des «Remboursements», qui correspondent à une quantité d’argent donnée directement à une personne par une autre.

Une fois l’évènement finis, les gens se remboursent, on cloture l’«Occasion» et on n’en parle plus.

Perso
-----
Cette application est prévue pour fonctionner avec mon site web personnel, http://perso.saurel.me (http://bit.saurel.me/perso), mais rien ne vous empêche d’essayer de l’utiliser ailleurs, et/ou de contribuer !


Améliorations prévues
---------------------

* La notion d’«Occasion» n’est clairement pas indispensable, il est tout à fait possible de la rendre optionnelle

* Pour l’instant, le moyen d’entrer des infos est l’interface d’administration de Django…
  Il faudrait passer à un système où chaque personne qui paye un coup à d’autres puisse ajouter une «Dette», et toutes les personnes concernées auraient à confirmer la dette.
