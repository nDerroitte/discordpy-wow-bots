class cotev2:
    def __init__(self):
        self.cote = int(input("Enter rating "))
        self.up= int(input("Enter up "))
        self.calcule_price()

    def calcule_price(self):
        if self.cote + self.up <= 1500:
            self.base_price = ((int(self.up / 100)) * 50000)
        elif 1500 < self.cote + self.up <= 1800:
            self.base_price = ((((1500-self.cote)/100) * 50000) + (((1800-self.cote)-(1500-self.cote))/100) * 200000)
        elif 1800 < self.cote + self.up <= 2000:
            self.base_price = ((((1500-self.cote)/100) * 50000) + ((((1800-self.cote)-(1500-self.cote))/100) * 200000) + ((((2000-self.cote)-((1800-self.cote)-(1500-self.cote))-(1500-self.cote))/100) * 300000))
        else: 
            print(self.base_price)
        return self.base_price

cotev2()
