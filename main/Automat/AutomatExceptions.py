class InvalidItemNumberException(Exception):
    """Informuje o złym numerze produktu"""
    def __init__(self):
        super().__init__("Zły numer produktu")

class NotEnoughMoneyException(Exception):
    """Informuje gdy wrzucilismy za mało pieniedzy"""
    def __init__(self, provided, required):
        super().__init__(f"Za mało pieniedzy (wrzucono: {provided}, żadane: {required}.")

class ExactChangeOnlyException(Exception):
    """Informuje gdy automat nie moze wydac reszty"""
    def __init__(self, amount):
        super().__init__(f"Tylko odliczona gotówka (zostało: {amount}")