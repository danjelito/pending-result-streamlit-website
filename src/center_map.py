class CenterMap:
    def __init__(self) -> None:
        self.center_area = {
            "PP": "JKT 1",
            "SDC": "JKT 1",
            "KG": "JKT 1",
            "NEO": "JKT 1",
            "GC": "JKT 2",
            "LW": "JKT 2",
            "BSD": "JKT 2",
            "TBS": "JKT 2",
            "CP": "JKT 2",
            "KK": "JKT 3",
            "CBB": "JKT 3",
            "SMB": "JKT 3",
            "DG": "BDG",
            "PKW": "SBY",
            "CIK": "CIK",
            "HO": "HO",
            "Street Talk": "Street Talk",
            "Corporate": "Corporate",
            "Online Center": "Online Center",
            "Curioo": "Curioo",
            "RST": "RST",
            "NST": "NST",
        }
        self.center_id = {
            "ID000": "Corporate",
            "ID001": "PP",
            "ID002": "SDC",
            "ID003": "GC",
            "ID005": "KK",
            "ID007": "DG",
            "ID008": "PKW",
            "ID009": "CBB",
            "ID010": "BSD",
            "ID011": "SMB",
            "ID013": "TBS",
            "ID100": "Curioo",
            "ID666": "Online Center",
            "ID777": "RST",
            "ID888": "NST",
        }

    def get_center(self) -> set:
        return set(k for k, v in self.center_area.items())

    def get_area(self) -> set:
        return set(v for k, v in self.center_area.items())

    def get_center_id_map(self) -> dict:
        return self.center_id

    def get_center_area_map(self) -> dict:
        return self.center_area

    def lookup_area(self, center) -> set:
        if center not in self.center_area.keys():
            raise ValueError(
                f"Center {center} is not a valid center. Select one of {set(self.center_area.keys())}"
            )
        return self.center_area[center]

    def lookup_centers(self, area) -> set:
        if area not in self.center_area.values():
            raise ValueError(
                f"Area {area} is not a valid area. Select one of {set(self.center_area.values())}"
            )
        return set(k for k, v in self.center_area.items() if v == area)
