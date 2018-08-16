from transect.domain.domain import Domain


class Series(Domain):

    def __init__(self, payer=None, payee=None):
        self.table_name = 'series'
        self.properties = {'payer': payer, 'payee': payee}
