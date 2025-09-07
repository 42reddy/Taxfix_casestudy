import random


# -------------------------------
# Domain specific seeds
# -------------------------------

names = ["Joel", "Emmett", "Leon", "Daniel", "Dennis", "Otis", "Tyrone",
         "Perry", "Malaysia", "Peyton", "Marjorie", "Keira", "Nicole",
         "Mia", "Yvette", "Zara", "Aubrey", "Emily"]
countries = ["USA", "Germany", "UK", "France"]
marital_statuses = ["married", "single", "divorced", "widowed"]
hobbies = ["photography", "painting", "cycling", "reading"]
pets = ["cat", "dog", "parrot", "none"]





# Question templates with clearer reasoning chains

question_bank = [
    {"question": "Is {name} eligible for joint filing?",
     "answer_fn": lambda f: "Yes" if (f["is_married"] and
                                      f["spouse_has_zero_income"] and
                                      f["country_allows_joint_filing"]) else "No"},
    {"question": "Does {name} qualify for child benefits?",
     "answer_fn": lambda f: "Yes" if f["has_children"] else "No"},
    {"question": "Does {name} have unusually high medical expenses?",
     "answer_fn": lambda f: "Yes" if f["medical_expenses_exceed_threshold"] else "No"}
]