from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.requests import get_hungry_dogs


async def feed_dogs() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    dogs = await get_hungry_dogs()
    for dog in dogs:
        keyboard_builder.button(
            text=f"{dog.name} поела", callback_data="dog_feed"
        )
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Покорми собаню и нажми кнопку",
    )


async def i_will_feeding() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Я ПОКОРМЛЮ", callback_data="i_feed")
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
