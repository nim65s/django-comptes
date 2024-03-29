# Comptes

[![PyPI version](https://badge.fury.io/py/django-comptes.svg)](https://pypi.org/project/django-comptes)
[![Tests](https://github.com/nim65s/django-comptes/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/django-comptes/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/django-comptes/master.svg)](https://results.pre-commit.ci/latest/github/nim65s/django-comptes/master)
[![codecov](https://codecov.io/gh/nim65s/django-comptes/branch/master/graph/badge.svg?token=75XO2X5QW0)](https://codecov.io/gh/nim65s/django-comptes)
[![Maintainability](https://api.codeclimate.com/v1/badges/a0783da8c0461fe95eaf/maintainability)](https://codeclimate.com/github/nim65s/django-comptes/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## But

Ceci est une application de gestion de petits comptes entre amis, nottament pour des occasions précises, telles qu’une semaine de vacances… Ou de dur labeur à la Ferté Bernard.

## Principe

Quand quelqu’un règle pour quelque chose qui bénéficie à plusieurs personne, comme un pot de Nutella ou la facture d’une Pizzeria, on l’entre comme une «Dette».

L’application calcule alors un «Solde», où la banque est en fait le groupe de personne : un solde positif indique que le groupe nous doit de l’argent (c’est toujours bien, un solde positif…)

Pour rééquilibrer la balance (ou toute autre raison), on peut également entrer des «Remboursements», qui correspondent à une quantité d’argent donnée directement à une personne par une autre.

Une fois l’évènement finis, les gens se remboursent, on cloture l’«Occasion» et on n’en parle plus.

## Perso

Cette application est prévue pour fonctionner avec mon site web personnel, https://saurel.me, mais rien ne vous empêche d’essayer de l’utiliser ailleurs, et/ou de contribuer !
