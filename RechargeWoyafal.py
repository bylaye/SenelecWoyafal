REDEVANCE = 429
MAX_TRANCHE_1 = 150
MAX_TRANCHE_2 = 250
PRIX_PAR_TRANCHE = [91.17, 136.49, 149.06]
TAXE_COMMUNAL = 0.025
UNIT = "Kw"
TVA = 0.18

class RechargeWoyafal:
    
    def __init__(self, compteur):
        self.compteur = compteur
        self.historic_achat = {"montant":[], UNIT:[]}
        
    def getCompteur(self):
        return self.compteur
    
    def getHistoricAchat(self):
        return self.historic_achat
