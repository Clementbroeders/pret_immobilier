def vpm(taux, duree, emprunt):
    '''
    Calcule la mensualité d'un emprunt (hors assurance)
    '''
    taux_mensuel = taux / 12
    duree_mois = duree * 12
    vpm_result = (emprunt * taux_mensuel) / (1 - (1 + taux_mensuel)**(-duree_mois))
    vpm_result = round(vpm_result, 3)
    return vpm_result


def interet(taux, periode, duree, emprunt):
    '''
    Calcule les intérêts d'une période donnée
    '''
    taux_mensuel = taux / 12
    mensualite = vpm(taux, duree, emprunt)
    capital_restant = emprunt
    for i in range(1, periode):
        interet_mois = capital_restant * taux_mensuel
        capital_restant -= (mensualite - interet_mois)
    interet_periode = capital_restant * taux_mensuel
    interet_periode = round(interet_periode, 3)
    return interet_periode


def capacite_emprunt(endettement, salaire, assurance, taux, duree, emprunt):
    '''
    Calcule la capacité d'emprunt en fonction du taux d'endettement
    '''
    mensualite = vpm(taux, duree, emprunt) + (emprunt * assurance / 12)
    mensualite_max = salaire * endettement
    capacite_emprunt = mensualite_max - mensualite
    return capacite_emprunt