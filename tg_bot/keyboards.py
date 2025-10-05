from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# клавиатура "добавить расход"
kb_expense = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить расход", callback_data="add_expense")]
    ]
)

# Функция для динамического создания клавиатуры категорий
def get_category_keyboard(categories):
    """
    categories: список словарей с ключами 'id' и 'name'
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat["name"], callback_data=f"category:{cat['id']}")]
            for cat in categories
        ]
    )
