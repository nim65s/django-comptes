Hello :)

{% if object.scribe %}{{ object.scribe }}{% else %}Un admin{% endif %} a ajouté la Dette suivante:

- Créancier:     {{ object.creancier }}
- Montant total: {{ object.montant|floatformat:2 }} €
- Débiteurs:     {{ object.debiteurs_list }}
- Date:          {{ object.moment }}
- Description:   {{ object.description }}

Cette dette augmente donc le solde de {{ object.creancier }} de {{ object.montant|floatformat:2 }} €,
puis diminue celui de {{ object.debiteurs_list|safe }} de {{ object.part|floatformat:2 }} €.

Plus d’infos directement sur le site: {{ object.get_full_url }}

@+ !


--
  Cet email a été envoyé automatiquement. Il est inutile d’y répondre.
