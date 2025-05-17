class ProductIntelligence:

    number_of_copies = 0

    def __init__(self, product_name: str, supply_volume: int, origin_сountry: str):
        self._product_name= product_name
        self._supply_volume = supply_volume
        self._origin_сountry = origin_сountry
        number_of_copies += 1

    @property
    def product_name(self):
        return self._product_name

    
    @property
    def supply_volume(self):
        return self._supply_volume

    @supply_volume.setter
    def supply_volume(self, value):
        self._supply_volume = value

    @property
    def origin_сountry(self):
        return self._origin_сountry

    @origin_сountry.setter
    def origin_сountry(self, value):
        self._origin_сountry = value

    def get_info(self):
        return f"Название: {self.product_name}, Объем: {self.supply_volume}, Производитель: {self.origin_сountry}"