import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Чтобы начать работу введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\nНапример: доллар рубль 100\n\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text, )


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверный ввод параметров!\n\nВведите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\nНапример: доллар рубль 100')

        quote, base, amount = values
        if float(amount) < 0:
            raise ConvertionException('Значение не должно быть отрицательным!')

        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:

        text = f'Цена за {amount} {keys.get(quote)}: {float(amount) * float(total_base)} {keys.get(base)}\n' \
               f'Цена за 1 {keys.get(quote)}: {float(total_base)} {keys.get(base)}'
        bot.send_message(message.chat.id, text)


bot.polling()

