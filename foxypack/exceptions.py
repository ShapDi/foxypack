from foxypack.abc.foxystat import FoxyStat


class DenialAsynchronousService(Exception):
    name_foxystat_subclass: FoxyStat

    def __init__(self, name_foxystat_subclass: FoxyStat) -> None:
        super().__init__()
        self.name_foxystat_subclass = name_foxystat_subclass
