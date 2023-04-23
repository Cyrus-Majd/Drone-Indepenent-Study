class Drone_Control:
    def __init__(self, multiplier):
        print("I BREATHE")
        self.multiplier = multiplier
        pass

    def climb(self, amount):
        amount = amount * self.multiplier
        print("climbing " + amount)
        pass

    def descend(self, amount):
        amount = amount * self.multiplier

        print("descending " + amount)
        pass

    def turn_right(self, deg):
        deg = deg * self.multiplier

        print("turning right" + deg)
        pass

    def turn_left(self, deg):
        deg = deg * self.multiplier

        print("turning left" + deg)
        pass

    def forwards(self, amount):
        amount = amount * self.multiplier

        print("forwarding" + amount)
        pass

    def back(self, amount):
        amount = amount * self.multiplier

        print("backwardsing" + amount)
        pass

    print("i am mohamad")
