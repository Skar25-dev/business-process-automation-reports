
import random
from typing import Union, List, Dict

from faker.providers import BaseProvider

CATEGORIES: List = [
  "Books",
  "Movies",
  "Music",
  "Games",
  "Electronics",
  "Computers",
  "Home",
  "Garden",
  "Tools",
  "Grocery",
  "Health",
  "Beauty",
  "Toys",
  "Kids",
  "Baby",
  "Clothing",
  "Shoes",
  "Jewelery",
  "Sports",
  "Outdoors",
  "Automotive",
  "Industrial"
]

MATERIALS: List = [
  "Steel",
  "Wooden",
  "Concrete",
  "Plastic",
  "Cotton",
  "Granite",
  "Rubber",
  "Metal",
  "Soft",
  "Fresh",
  "Frozen"
]

PRODUCT_DATA: Dict[str, List] = {
    'material': MATERIALS,
    'product': [
        "Chair",
        "Car",
        "Computer",
        "Keyboard",
        "Mouse",
        "Bike",
        "Ball",
        "Gloves",
        "Pants",
        "Shirt",
        "Table",
        "Shoes",
        "Hat",
        "Towels",
        "Soap",
        "Tuna",
        "Chicken",
        "Fish",
        "Cheese",
        "Bacon",
        "Pizza",
        "Salad",
        "Sausages",
        "Chips"
    ],
    'adjective': [
        "Small",
        "Ergonomic",
        "Rustic",
        "Intelligent",
        "Gorgeous",
        "Incredible",
        "Fantastic",
        "Practical",
        "Sleek",
        "Awesome",
        "Generic",
        "Handcrafted",
        "Handmade",
        "Licensed",
        "Refined",
        "Unbranded",
        "Tasty",
        "New",
        "Gently Used",
        "Used",
        "For repair"
    ]
}


class Provider(BaseProvider):
    """Provider for Faker which adds fake ecommerce product information."""

    def ecommerce_name(self) -> str:
        """Fake product names."""
        product = self.random_element(PRODUCT_DATA['product'])
        adjective = self.random_element(PRODUCT_DATA['adjective'])
        material = self.random_element(PRODUCT_DATA['material'])

        choices = [
            product,
            " ".join([adjective, product]),
            " ".join([material, product]),
            " ".join([adjective, material, product]),
        ]

        names = random.choices(choices, k=1)
        return names[0]

    def ecommerce_material(self) -> str:
        return self.random_element(MATERIALS)

    def ecommerce_category(self) -> str:
        return self.random_element(CATEGORIES)

    def ecommerce_price(self, as_int: bool = True) -> Union[int, float]:
        n = self.random_int(min=100, max=99999999)
        return round(n, 2) if as_int else n / 100
