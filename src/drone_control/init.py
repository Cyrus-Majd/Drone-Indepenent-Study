class Drone_Control:
    def __init__(self, multiplier):
        print("I BREATHE")
        self.multiplier = multiplier
        pass

    def climb(self, amount):
        amount = amount * self.multiplier
        print("climbing " + amount)
        pass

    def descending(self, amount):
        amount = amount * self.multiplier

        print("descending " + amount)
        pass

    def turn_right(self, radius):
        radius = radius * self.multiplier

        print("turning right" + radius)
        pass

    def turn_left(self, radius):
        radius = radius * self.multiplier

        print("turning left" + radius)
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
