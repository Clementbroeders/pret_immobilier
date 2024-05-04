import pandas as pd
from utils.calculs import vpm, interet

def create_table(taux, emprunt, duree, taux_assurance, date_debut_pret):
    '''
    Crée un tableau d'amortissement du prêt immobilier (par mois) en déduisant la mensualité de l'assurance
    '''

    mensualite_hors_assurance = vpm(taux, duree, emprunt)  # Calcul de la mensualité hors assurance
    
    data = pd.DataFrame(range(1, duree*12+1), columns=['numero_mois'])
    data['annee'] = (data['numero_mois'] - 1) // 12 + 1
    
    day_date_debut_pret = pd.to_datetime(date_debut_pret).day
    if day_date_debut_pret == 1:
        data['date_remboursement'] = pd.date_range(date_debut_pret, periods=duree*12, freq='MS') 
    else:
        date_debut_pret_ajusted_month = pd.to_datetime(date_debut_pret) + pd.DateOffset(months=-1)
        data['date_remboursement'] = pd.date_range(date_debut_pret_ajusted_month, periods=duree*12, freq='MS') + pd.DateOffset(days = day_date_debut_pret-1)
    
    data['mensualite_hors_assurance'] = mensualite_hors_assurance
    data['mensualite_interet'] = data.apply(lambda x: interet(taux, x['numero_mois'], duree, emprunt), axis=1)  # Calcul des intérêts
    data['mensualite_capital'] = data['mensualite_hors_assurance'] - data['mensualite_interet']
    data['mensualite_assurance'] = round(emprunt * taux_assurance / 12, 3)  # Calcul de la mensualité de l'assurance
    data['mensualite_globale'] = data['mensualite_hors_assurance'] + data['mensualite_assurance']
    data['reste_a_rembourser'] = emprunt - data['mensualite_capital'].cumsum()

    return data