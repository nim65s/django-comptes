Hello :)

{% if object.scribe %}{{ object.scribe }}{% else %}Un admin{% endif %} a ajouté le Remboursement suivant:

- Créditeur: {{ object.crediteur }}
- Montant:   {{ object.montant|floatformat:2 }} €
- Crédité:   {{ object.credite }}
- Date:      {{ object.moment }}

Plus d’infos directement sur le site: {{ object.get_full_url }}

@+ !


--
  Cet email a été envoyé automatiquement. Il est inutile d’y répondre.
