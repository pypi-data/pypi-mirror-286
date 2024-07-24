

class InsulationAndWindows():


    def __init__(self,**kwargs):
        self.eemCost = kwargs.get("eemCost",None)
        self.buildingConstructionYear = kwargs.get(
            "buildingConstructionYear","Before 1945"
        )
        self.floorNumber = kwargs.get(
            "floorNumber",
            1
        )
        self.windowToWallRatio = kwargs.get(
            "windowToWallRatio",
            0.2
        )