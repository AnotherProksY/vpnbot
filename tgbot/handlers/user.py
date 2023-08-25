from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ChatType

from loader import bot, db
from tgbot.keyboards.inline import keyboard_start


async def user_start(message: Message):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(f'Привет, @{message.from_user.username} 👋\n\n'
                         'Мы поможем тебе подключить твой личный <b>VPN</b> без рекламы и на огромных скоростях всего за пару кликов!\n\n'
                         'В случае возникноваения каких-либо проблем, ты всегда можешь обратиться в нашу техническую поддержку: <a href="https://t.me/vpnbot_support">отправить сообщение</a>',
                         reply_markup=keyboard_start(), disable_web_page_preview=True)


async def help_handler(message: Message):
    await message.answer(f'Преимущества <b>VPN</b>\n\n'
                         f'<b>VPN</b> позволяет безопасно обмениваться данными и '
                         f'пользоваться интернетом в обход цензуры. Это особенно '
                         f'актуально в текущее время, когда власти пытаются '
                         f'<b>заблокировать</b> внешние ресурсы и технологии VPN.\n\n'
                         f'Мы используем технологию <b>Outline</b>!\n\n'
                         f'<b>Outline</b> не подведет, когда другие VPN откажут: наш сервис '
                         f'не так просто отследить и заблокировать на основе сетей или IP-адресов.\n\n'
                         f'Решение <b>Outline</b> надежнее, поскольку работает на основе протокола, который '
                         f'сложно обнаружить, а следовательно – заблокировать.\n\n'
                         f'<b>Outline</b> - это ПО с открытым исходным кодом, '
                         f'которое прошло проверку организаций '
                         f'<a href="https://s3.amazonaws.com/outline-vpn/static_downloads/ros-report.pdf">Radically Open Security</a> и '
                         f'<a href="https://s3.amazonaws.com/outline-vpn/static_downloads/cure53-report.pdf">Cure53</a>.\n\n'
                         f'<b>Outline</b> использует технологию <a href="https://shadowsocks.org/">Shadowsocks</a>',disable_web_page_preview=True)


async def help_callback_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,
                           f'Преимущества <b>VPN</b>\n\n'
                           f'<b>VPN</b> позволяет безопасно обмениваться данными и '
                           f'пользоваться интернетом в обход цензуры. Это особенно '
                           f'актуально в текущее время, когда власти пытаются '
                           f'<b>заблокировать</b> внешние ресурсы и технологии VPN.\n\n'
                           f'Мы используем технологию <b>Outline</b>!\n\n'
                           f'<b>Outline</b> не подведет, когда другие VPN откажут: наш сервис '
                           f'не так просто отследить и заблокировать на основе сетей или IP-адресов.\n\n'
                           f'Решение <b>Outline</b> надежнее, поскольку работает на основе протокола, который '
                           f'сложно обнаружить, а следовательно – заблокировать.\n\n'
                           f'<b>Outline</b> - это ПО с открытым исходным кодом, '
                           f'которое прошло проверку организаций '
                           f'<a href="https://s3.amazonaws.com/outline-vpn/static_downloads/ros-report.pdf">Radically Open Security</a> и '
                           f'<a href="https://s3.amazonaws.com/outline-vpn/static_downloads/cure53-report.pdf">Cure53</a>.\n\n'
                           f'<b>Outline</b> использует технологию <a href="https://shadowsocks.org/">Shadowsocks</a>',
                           disable_web_page_preview=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], chat_type=ChatType.PRIVATE)
    dp.register_message_handler(help_handler, commands=["help"], chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(help_callback_handler, lambda c: c.data == 'why', chat_type=ChatType.PRIVATE)
