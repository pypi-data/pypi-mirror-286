from .google import Sheets
from astropy.table import Table

class Inventory(Sheets):

    SHEET_ID = '11k-wMwRTOcVW5vFiIVjOsYpUxVKBq0rCaFOYq0y59qw'

    def devices(self, keep_unused: bool = False) -> Table:

        tab = self.get(self.SHEET_ID, 'Devices!B5:Q', 
            has_colnames=True, strip=True)
        tab.remove_column('Sortable IP')

        if not keep_unused:
            used = ['unused' not in c for c in tab['Comment']]
            tab = tab[used]

        return tab

    def telescope_HWIDs(self) -> Table:

        tab = self.get(self.SHEET_ID, 'HWID!B5:H', 
            has_colnames=True, strip=True)
        tab = tab[tab['N Telescopes'] > 0]

        return tab
