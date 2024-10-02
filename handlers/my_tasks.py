from pyrogram import Client, filters
from pyrogram.types import Message,CallbackQuery
from keyboards.inline import keyboards as keyboard
from database.db import DatabaseSession
from states.states import user_data,user_states,States
from models.task import Task

async def handle_my_tasks(client: Client, message: Message) -> None:
    if message.text == '📝 Мои задачи':
        session = DatabaseSession()
        user_tasks = Task.get_tasks_by_owner(session,message.from_user.id)
        print(user_tasks)
        await message.reply(text = '😋 <b>Вы еще не создали ни одной задачи, давайте это сделаем! </b>' if len(user_tasks) == 0 else '✍️ Список Ваших задач:',
                            reply_markup=await keyboard.show_tasks(user_tasks))
    

async def handle_create_task(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id].update({"message_id": callback.message.id})
    user_states[user_id] = States.task_name
    await callback.message.edit_text(text='<b>💡 Введите название задачи</b>',reply_markup=await keyboard.cancel_create())

async def handle_task_name(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    if user_states.get(user_id) == States.task_name:
        user_data[user_id].update({"task_name": message.text})
        user_states[user_id] = States.task_description
        await message.delete()
        print(user_data)
        await client.edit_message_text(chat_id=message.chat.id,message_id=user_data[user_id]['message_id'],text="<b>✍️ Теперь введите описание задачи.</b>")



async def finish_task(client: Client, callback: CallbackQuery) -> None:
    session = DatabaseSession()
    task_id = callback.data.split('|')[1]
    Task.update_task(session=session,
                     task_id=task_id,
                     is_complited=True)
    task = Task.get_task(session, task_id)
    await callback.message.edit_text(text=f"""<b>💡 Название:</b> <code>{task.title}</code>
<b>✍️ Описание:</b> <code>{task.description}</code>
<b>🔘 Статус:</b> <code>{'Завершнено' if task.is_complited else 'В процессе'}</code>

<i>Выберите действие:</i>""",reply_markup=await keyboard.manage_task(task_id,task.is_complited))

async def delete_task(client: Client, callback: CallbackQuery) -> None:
    session = DatabaseSession()
    task_id = callback.data.split('|')[1]
    Task.delete_task(session, task_id)
    user_tasks = Task.get_tasks_by_owner(session,callback.from_user.id)
    await callback.message.edit_text(text = '😋 <b>Вы еще не создали ни одной задачи, давайте это сделаем! </b>' if len(user_tasks) == 0 else '✍️ Список Ваших задач:',
                        reply_markup=await keyboard.show_tasks(user_tasks))
    await callback.answer('✅ Задача успешно удалена!',show_alert=True)

async def show_user_task(client: Client, callback: CallbackQuery) -> None:
    session = DatabaseSession()
    task_id = callback.data.split('|')[1]
    task = Task.get_task(session, task_id)
    await callback.message.edit_text(text=f"""<b>💡 Название:</b> <code>{task.title}</code>
<b>✍️ Описание:</b> <code>{task.description}</code>
<b>🔘 Статус:</b> <code>{'Завершнено' if task.is_complited else 'В процессе'}</code>

<i>Выберите действие:</i>""",reply_markup=await keyboard.manage_task(task_id,task.is_complited))

    
async def handle_task_description(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    if user_states.get(user_id) == States.task_description:
        session = DatabaseSession()
        Task.create_task(session=session,
            title=user_data[user_id]['task_name'],
            description=message.text,
            owner_id=user_id
        )
        await message.delete()
        user_tasks = Task.get_tasks_by_owner(session,message.from_user.id)
        await client.edit_message_text(chat_id=message.chat.id,message_id=user_data[user_id]['message_id'],text='✍️ Список Ваших задач:',reply_markup=await keyboard.show_tasks(user_tasks))
        user_states[user_id] = None

async def handle_cancel_create(client: Client, callback: CallbackQuery) -> None:
    session = DatabaseSession()
    user_states[callback.from_user.id] = None
    user_tasks = Task.get_tasks_by_owner(session,callback.from_user.id)
    await callback.message.edit_text(text = '😋 <b>Вы еще не создали ни одной задачи, давайте это сделаем! </b>' if len(user_tasks) == 0 else '✍️ Список Ваших задач:',
                        reply_markup=await keyboard.show_tasks(user_tasks))




