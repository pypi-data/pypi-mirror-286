"""Asynchronous Python client for Mealie."""

from aiomealie.exceptions import (
    MealieConnectionError,
    MealieError,
    MealieAuthenticationError,
    MealieValidationError,
    MealieBadRequestError,
    MealieNotFoundError,
)
from aiomealie.mealie import MealieClient
from aiomealie.models import (
    About,
    StartupInfo,
    GroupSummary,
    Theme,
    BaseRecipe,
    RecipesResponse,
    Mealplan,
    MealplanResponse,
    MealplanEntryType,
    MutateShoppingItem,
    ShoppingList,
    ShoppingListsResponse,
    ShoppingItem,
    ShoppingItemsResponse,
    UserInfo,
    Recipe,
    Instruction,
    Ingredient,
    Tag,
    Statistics,
)

__all__ = [
    "About",
    "MealieConnectionError",
    "MealieError",
    "MealieAuthenticationError",
    "MealieBadRequestError",
    "MealieNotFoundError",
    "MealieValidationError",
    "MealieClient",
    "StartupInfo",
    "GroupSummary",
    "Theme",
    "BaseRecipe",
    "Recipe",
    "Instruction",
    "Ingredient",
    "Tag",
    "RecipesResponse",
    "Mealplan",
    "MealplanResponse",
    "MealplanEntryType",
    "ShoppingItem",
    "Statistics",
    "MutateShoppingItem",
    "ShoppingItemsResponse",
    "ShoppingList",
    "ShoppingListsResponse",
    "UserInfo",
]
