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

    def __kw_recharger(self, montant):
        total_kw_historic = sum(self.historic_achat[UNIT])
        n_kw = 0
        # Si on est toujours dans la premiere tranche
        if total_kw_historic <= MAX_TRANCHE_1:
            m = (MAX_TRANCHE_1 - total_kw_historic) * PRIX_PAR_TRANCHE[0]
            if montant > m:
                n_kw += m / PRIX_PAR_TRANCHE[0]
                montant -= m
                total_kw_historic += n_kw
            else:
                n_kw += montant / PRIX_PAR_TRANCHE[0]
                montant = 0
        # Deuxieme tranche
        if montant > 0:
            if total_kw_historic <= MAX_TRANCHE_2:
                m = (MAX_TRANCHE_2 - total_kw_historic) * PRIX_PAR_TRANCHE[1]
                if montant > m:
                    n_kw += m / PRIX_PAR_TRANCHE[1]
                    # Troisieme tranche
                    montant = montant - (montant*TVA + m)
                    n_kw += montant / PRIX_PAR_TRANCHE[2]
                else:
                    n_kw += montant / PRIX_PAR_TRANCHE[1]
                    montant = 0
            # Troisieme tranche
            else:
                    montant -= montant*TVA
                    n_kw += montant / PRIX_PAR_TRANCHE[2]      
        return n_kw

    def newAchat(self, montant):
        self.historic_achat["montant"].append(montant)
        # Le taxe communal est déduit pour tout recharge.
        montant_deduit = montant * TAXE_COMMUNAL
        # Si il s'agit de la premiere recharge du mois on deduit la redevance.
        if sum(self.historic_achat[UNIT]) == 0:
            montant_deduit += REDEVANCE
        montant -= montant_deduit

        total_kw = self.__kw_recharger(montant)
        self.historic_achat[UNIT].append(total_kw)
        return total_kw
