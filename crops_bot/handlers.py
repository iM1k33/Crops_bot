from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from .commands import ask_gpt
from .limiter import check_rate_limit, add_request, get_usage_stats


router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    start_text = (
        "🌾 *Welcome to Sunrise Crops Wiki Bot!*\n"
        "Ask me anything about agricultural crops!\n\n"
        "Example: 'Tell me about wheat cultivation'\n\n"
        "Use /help for more information"
    )
    await message.answer(start_text, parse_mode="Markdown")
        
    

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "❔*Sunrise Crops Wiki Bot Help*\n\n"
        "I'm an agricultural crop expert powered by Wikipedia knowledge.\n"
        "Knowledge base includes 3111 sections of 366 articles.\n\n"
        "*Available commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/stats - Show your usage statistics\n\n"
        "*How to use:*\n"
        "Simply ask any question about agricultural crops, for example:\n"
        "- Tell me about wheat cultivation\n"
        "- What is number one country for cultivating mangoes?\n"
        "*Limits:*\n"
        "You can make up to 5 requests per hour and 20 per day."
    )
    await message.answer(help_text, parse_mode="Markdown")

@router.message(Command("stats"))
async def stats_command(message: Message):
    user_id = message.from_user.id
    stats = get_usage_stats(user_id)
    response = (
        f"📊 *Your Usage Statistics*\n\n"
        f"Requests today: {stats['daily']}/20\n"
        f"Requests this hour: {stats['hourly']}/5"
    )
    await message.answer(response, parse_mode="Markdown")
    
@router.message(F.text)
async def handle_text_message(message: Message):
    user_id = message.from_user.id
    
    # Проверяем ограничения
    allowed, limit_type = check_rate_limit(user_id)
    if not allowed:
        if limit_type == "hourly":
            await message.answer("⚠️ You've reached the hourly limit (5 requests). Please try again later.")
        else:
            await message.answer("⚠️ You've reached the daily limit (20 requests). Please try again tomorrow.")
        return
    
    # Добавляем запрос в статистику
    add_request(user_id)
    
    # Отправляем статус "печатает..."
    typing_message = await message.answer("⏳ Processing your request...")
    
    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
        )
    
    try:
        # Продолжаем показывать индикатор
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action="typing"
        )
        
        response = ask_gpt(message.text)
        
        # Удаляем сообщение "Processing..."
        await typing_message.delete()
        
        await message.answer(response)
    except Exception as e:
        # Удаляем сообщение "Processing..." в случае ошибки
        await typing_message.delete()
        await message.answer("🚨 Sorry, I encountered an error processing your request. Please try again later.")
        print(f"Error processing message: {e}")
