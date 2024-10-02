<h1>Telegram Task Management Bot</h1>

<h2>1. Общее описание задачи</h2>
<p>Задача cостояла в разработке Telegram-бота, который предоставляет пользователям возможность управлять своими задачами (создавать, редактировать, завершать и удалять их). После регистрации пользователи получают доступ к функционалу бота для управления задачами. Для хранения данных используется база данных, взаимодействие с которой реализовано через ORM SQLAlchemy.</p>

<h2>2. Технологии и инструменты</h2>
<ul>
    <li><strong>Python</strong> — основной язык разработки.</li>
    <li><strong>Pyrogram</strong> — библиотека для взаимодействия с Telegram API.</li>
    <li><strong>SQLAlchemy</strong> — ORM для работы с базой данных.</li>
    <li><strong>PostgreSQL</strong> — система управления базой данных.</li>
    <li><strong>FSM (Finite State Machine)</strong> — для управления состояниями пользователей в боте.</li>
    <li><strong>Docker</strong> — для контейнеризации и удобного развёртывания приложения.</li>
</ul>

<h2>3. Архитектура решения</h2>
<p>Архитектура приложения разделена на несколько ключевых компонентов:</p>
<ul>
    <li><strong>Bot (Pyrogram)</strong> — отвечает за обработку команд и сообщений от пользователей.</li>
    <li><strong>Database (SQLAlchemy)</strong> — обеспечивает взаимодействие с базой данных, управляя пользователями и задачами.</li>
    <li><strong>FSM (Finite State Machine)</strong> — отслеживает состояния пользователей, например, на этапах регистрации.</li>
    <li><strong>Handlers</strong> — обработчики сообщений и команд от пользователей.</li>
</ul>
<p>Диаграмма взаимодействий:</p>
<pre>
User --> [Bot (Pyrogram)] --> [Handlers] --> [Database]
                                  |
                                  v
                          [FSM (State Management)]
</pre>

<h2>4. Основные классы и функции</h2>
<h3>Database:</h3>
<ul>
    <li><strong>Base</strong> — базовый класс для всех моделей данных (User, Task).</li>
    <li><strong>User</strong> — модель пользователя с информацией о <code>user_id</code>, <code>username</code> и <code>name</code>.</li>
    <li><strong>Task</strong> — модель задачи, связанная с пользователем, содержит <code>title</code>, <code>description</code> и статус выполнения.</li>
</ul>

<h3>Handlers:</h3>
<ul>
    <li><strong>start</strong> — обрабатывает команду <code>/start</code>. Приветствует пользователя или начинает регистрацию, если он не зарегистрирован.</li>
    <li><strong>handle_name</strong> — обрабатывает ввод имени пользователя.</li>
    <li><strong>handle_username</strong> — завершает процесс регистрации, сохраняя данные в базу.</li>
</ul>

<h3>FSM:</h3>
<p>Управляет состояниями, такими как <code>name</code>, <code>username</code>, <code>task_name</code>, <code>task_description</code>, помогая отслеживать прогресс пользователей.</p>

<h2>5. Реализованные функции</h2>
<h3>Регистрация:</h3>
<ul>
    <li>Пользователь отправляет команду <code>/start</code>.</li>
    <li>Если пользователь уже зарегистрирован, бот его приветствует, если нет — начинается процесс регистрации.</li>
    <li>Пользователь вводит свое имя и <code>username</code>, которые сохраняются в базе данных.</li>
</ul>

<h3>Управление задачами:</h3>
<ul>
    <li>После регистрации пользователю предоставляется доступ к интерфейсу управления задачами.</li>
    <li>Пользователь может создавать задачи, просматривать, редактировать, завершать или удалять их через инлайн-клавиатуры.</li>
</ul>
<p>Примеры команд:</p>
<ul>
    <li><code>/start</code> — запуск бота.</li>
    <li><strong>📝 Мои задачи</strong> — отображение списка задач пользователя.</li>
</ul>

<h2>6. Структура базы данных и SQL-запросы</h2>

<h3>Таблица <code>users</code>:</h3>
<ul>
    <li><code>id</code> — первичный ключ.</li>
    <li><code>user_id</code> — уникальный идентификатор в Telegram.</li>
    <li><code>username</code> — username пользователя.</li>
    <li><code>name</code> — имя пользователя.</li>
</ul>

<p>Запросы выполняются через методы ORM:</p>
<ul>
    <li><code>User.get_by_user_id</code> — получает пользователя по telegram user_id.</li>
    <li><code>User.get_by_username</code> — Получает пользователя по username.</li>
    <li><code>Task.create</code> — создает нового пользователя.</li>
</ul>

<h3>Таблица <code>tasks</code>:</h3>
<ul>
    <li><code>id</code> — первичный ключ.</li>
    <li><code>title</code> — название задачи.</li>
    <li><code>description</code> — описание задачи.</li>
    <li><code>owner_id</code> — внешний ключ, связывающий задачу с пользователем.</li>
    <li><code>is_completed</code> — флаг завершения задачи.</li>
</ul>

<p>Запросы выполняются через методы ORM:</p>
<ul>
    <li><code>Task.create_task</code> — добавляет задачу.</li>
    <li><code>Task.get_task</code> — возвращает задачу по ID.</li>
    <li><code>Task.update_task</code> — обновляет информацию о задаче.</li>
    <li><code>Task.delete_task</code> — удаляет задачу.</li>
</ul>

<h2>7. Инструкции по развертыванию и запуску приложения</h2>
<p>Для развертывания и запуска проекта, выполните следующие шаги:</p>

<ol>
    <li>
        <strong>Клонирование репозитория:</strong> Склонируйте проект на свой компьютер.
        <pre><code>git clone https://github.com/lvnt1s/Task-Management-Bot.git
cd telegram-task-bot</code></pre>
    </li>
    <li>
        <strong>Создание файла .env:</strong> Создайте файл <code>.env</code> в корне проекта и добавьте в него необходимые переменные окружения:
        <pre><code>API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token</code></pre>
    </li>
    <li>
        <strong>Создание и запуск контейнеров:</strong>
        <ul>
            <li>Убедитесь, что у вас установлен Docker и Docker Compose.</li>
            <li>Для сборки и запуска контейнеров выполните:
                <pre><code>docker-compose up --build</code></pre>
            </li>
        </ul>
    </li>
    <li>
        <strong>Инициализация базы данных:</strong> База данных будет автоматически создана и настроена при первом запуске контейнера.
    </li>
    <li>
        <strong>Работа с ботом:</strong> Бот будет запущен автоматически и готов принимать команды. Вы можете взаимодействовать с ним через Telegram, отправив команду <code>/start</code>.
    </li>
    <li>
        <strong>Мониторинг логов:</strong> Чтобы просмотреть логи работы контейнеров, выполните:
        <pre><code>docker-compose logs -f</code></pre>
    </li>
</ol>

<p>Это позволит вам легко развернуть Telegram-бота вместе с PostgreSQL в изолированных контейнерах.</p>


<h2>8. Дополнительные пояснения</h2>
<ul>
    <li>FSM используется для пошаговой регистрации пользователей и работы с задачами.</li>
    <li>Инлайн-клавиатуры предоставляют удобный интерфейс для взаимодействия с пользователями через Telegram.</li>
</ul>
