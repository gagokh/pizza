
from topping import Topping
from pizza import Pizza

CheeseTopping = Topping("cheese", 1)
PepperoniTopping = Topping("pepperoni", 1)
MushroomTopping = Topping("mushroom", 1)

pizza = Pizza("pepperoni", 10, [PepperoniTopping, CheeseTopping, MushroomTopping])

pizza.add_topping(CheeseTopping)
pizza.add_topping(MushroomTopping)


print(pizza.price())