# import random

# x = random.randrange(1, 6)

# print(f"The number is: {x}")

# def mylabubu() :
#   global x
#   if x == 6:
#     return "Luck=Purple"
#   if x == 5: 
#     return "Hope=Blue"
#   if x == 4:
#     return "Serenity=Green"
#   if x == 3:
#     return "Loyalty=Yellow"
#   if x == 2:
#     return "Happiness=Orange"
#   if x == 1:
#     return "Love=Red"
  
# print(mylabubu())

# def myFunction() :
#   global x
#   if x > 5:
#     return True
#   if x < 2:
#     return True 
#   else: 
#     return False

# print(myFunction())

#--------------------------------------------------------------------------------------------------------------------------------------

# import random
# from typing import Dict

# def labubunumber(j: int) -> str:
#     """
#     Returns the Labubu meaning(s) based on the input number.

#     Args:
#         j (int): A number between 1 and 6.

#     Returns:
#         str: A string containing the corresponding Labubu meaning(s).
#     """
#     meanings: Dict[int, str] = {
#         6: "Luck=Purple",
#         5: "Hope=Blue",
#         4: "Serenity=Green",
#         3: "Loyalty=Yellow",
#         2: "Happiness=Orange",
#         1: "Love=Red"
#     }

#     if j == 6:
#         # Return all meanings in order from 1 to 6
#         return " and ".join([meanings[i] for i in range(1, 7)])
    
#     if j in range(1, 6):  # Ensure `j` is between 1 and 5
#         # Choose `j` random meanings
#         random_choices = random.sample(list(meanings.values()), j)
#         return " and ".join(random_choices)
    
#     return "Invalid input. Please provide a number between 1 and 6."

# # Generate a random number between 1 and 6
# j = random.randint(1, 6)
# print(f"You Got {j} Labubu(s)!")
# print(labubunumber(j))

#----------------------------------------------------------------------------------------------------------------------------------------------------

import random

def get_labubu() -> str:
    """
    Returns one Labubu at a time from a set of 7 kinds, where "ID=Black" 
    has 12 times lower probability of being selected compared to the others.

    Returns:
        str: The selected Labubu.
    """
    labubu_weights = {
        "Love=Red": 12,
        "Happiness=Orange": 12,
        "Loyalty=Yellow": 12,
        "Serenity=Green": 12,
        "Hope=Blue": 12,
        "Luck=Purple": 12,
        "ID=Black": 1  # 12 times less likely
    }

    # Create a weighted list of Labubu kinds
    weighted_labubu_list = [
        labubu for labubu, weight in labubu_weights.items() for _ in range(weight)
    ]

    # Randomly select one Labubu from the weighted list
    return random.choice(weighted_labubu_list)

# Example usage
print("You got:", get_labubu())