import discord
from discord.ext import commands

# Укажите токен вашего бота
TOKEN = 'MTI4OTY3MDI5NjcyMjM0MTk2OQ.GB3rhG.HxHdHj81VsLgBSqlK2hYdpF6o_Lz-BlcRjt4m8'

# Укажите ID роли, которую нужно выдавать
ROLE_ID = 1289670096700309505  # Замените на реальный ID роли

# Укажите ID канала для логов
LOG_CHANNEL_ID = 1289668342441050153  # Замените на реальный ID канала для логов

# Префикс команд
intents = discord.Intents.default()
intents.members = True  # Чтобы бот мог получать информацию о пользователях
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен и готов к работе!')

    # Получаем сервер (guild) на котором бот находится
    for guild in bot.guilds:
        role = guild.get_role(ROLE_ID)
        
        if role is None:
            print("Роль не найдена.")
            return

        # Получаем лог-канал
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel is None:
            print("Лог-канал не найден.")
            return

        # Счётчик для отслеживания количества выданных ролей
        assigned_count = 0

        # Перебираем всех пользователей на сервере
        for member in guild.members:
            # Проверяем, есть ли у пользователя только роль @everyone
            if len(member.roles) == 1:  # Это значит, что кроме @everyone других ролей нет
                try:
                    await member.add_roles(role)
                    assigned_count += 1
                    # Логируем действие
                    await log_channel.send(f"Роль {role.name} была выдана пользователю {member.name}#{member.discriminator}")
                except discord.Forbidden:
                    await log_channel.send(f"Не хватает прав для выдачи роли пользователю {member.mention}")
                except discord.HTTPException as e:
                    await log_channel.send(f"Произошла ошибка при выдаче роли: {e}")

        # Логируем итоговое количество
        await log_channel.send(f'Роль была выдана {assigned_count} пользователям.')

# Запуск бота
bot.run(TOKEN)