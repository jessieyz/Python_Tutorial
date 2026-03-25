car = {
    "brand": "Tesla",
    "model": "Model 3",
    "year": 2020
}

if "model" in car:
  print("Yes, 'model' is one of the keys in the car dictionary.")

x = car.keys()

print(x)

car["color"] = "red"
car["year"] = 2021

print(x)

y = car.values()

print(y)

z = car.items()

print(z)

# Print all key names in the dictionary, one by one
for x in car:
  print(x)

# Print all keys in the dictionary, one by one
for x in car.keys():
  print(x)

# Print all values in the dictionary, one by one
for x in car:
  print(car[x])

# Print the values using the values() method
for x in car.values():
  print(x)

# Print all key-value pairs in the dictionary, one by one
for x in car:
  print(x, car[x])

# Loop through both keys and values, by useing the items() method
for x, y in car.items():
  print(x, y)

# Make a copy of the dictionary with the copy() method
car_copy = car.copy()
print(car_copy)

# Make a copy of the dictionary with the dict() constructor
car_copy2 = dict(car)

# nested dictionaries

# Create a dictionary that contains three dictionaries
cars = {
  "car1": {
    "brand": "Tesla",
    "model": "Model 3",
    "year": 2020
  },
  "car2": {
    "brand": "Ford",
    "model": "Mustang",
    "year": 2021
  },
  "car3": {
    "brand": "Chevrolet",
    "model": "Camaro",
    "year": 2022
  }
}

# Create three dictionaries, then create one dictionary that will contain them
car1 = {
  "brand": "Tesla",
  "model": "Model 3",
  "year": 2020
}

car2 = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 2021
}

car3 = {
  "brand": "Chevrolet",
  "model": "Camaro",
  "year": 2022
}

cars = {
  "car1": car1,
  "car2": car2,
  "car3": car3
}

# Print the year of the second car
print(cars["car2"]["year"])

# Loop through the keys and values of all nested dictionaries
for car_key, car_value in cars.items():
    print(car_key)
    for key, value in car_value.items():
        print(" ", key, ":", value)
# w3schools way
for x, obj in cars.items():
    print(x)
    for y in obj:
        print(y + ":", obj[y])

# use setdefault() to provide default values
car1.setdefault("color", "unknown")
car2.setdefault("color", "unknown")
car3.setdefault("color", "unknown")
print(cars)
