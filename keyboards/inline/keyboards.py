from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def show_tasks(user_tasks: list) -> InlineKeyboardMarkup:
    """Создание клавиатуры для отображения задач пользователя."""
    keyboard = []

    for item in user_tasks:
        keyboard.append([InlineKeyboardButton(f"{'✅' if item.is_complited else '⏳'} {item.title}", callback_data=f'show_task|{item.id}')])

    keyboard.append([InlineKeyboardButton('➕ Создать задачу', callback_data='create_task')])
    return InlineKeyboardMarkup(keyboard)

async def cancel_create() -> InlineKeyboardMarkup:
    """Создание клавиатуры с кнопкой отмены действия."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('❌ Отменить', callback_data='cancel_create')]
    ])

async def manage_task(task_id: int, status: bool) -> InlineKeyboardMarkup:
    """Создание клавиатуры для управления задачами."""
    buttons = []

    if not status:
        buttons.append(InlineKeyboardButton('✅ Завершить', callback_data=f'finish_task|{task_id}'))

    buttons.append(InlineKeyboardButton('🗑 Удалить', callback_data=f'delete_task|{task_id}'))

    return InlineKeyboardMarkup([
        buttons, 
        [InlineKeyboardButton('◀️ Назад ', callback_data='cancel_create')]
    ])

