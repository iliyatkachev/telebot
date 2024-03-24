from aiogram.types import InlineKeyboardButton



button = [
        [
            InlineKeyboardButton(text="Возможности✨", callback_data="opportunities"),
            InlineKeyboardButton(text="Служба Поддержки🥸", url="https://t.me/Iltk01")
        ],
        [
            InlineKeyboardButton(text="Видео Гайд🎥", callback_data="videogaid"),
            InlineKeyboardButton(text="Меню📖", callback_data="menu")
        ]
    ]


menu_button = [
    [
        InlineKeyboardButton(text="Статистика🧮", callback_data="stat"),
        InlineKeyboardButton(text="Профиль🪪", callback_data="profile")
    ],
    [
        InlineKeyboardButton(text="Фильмы🎞️", callback_data="films"),
    ],
    [
        InlineKeyboardButton(text="Подборка🛒", callback_data="Compilation")
    ],
    [
        InlineKeyboardButton(text="Подписка📜", callback_data="subscription"),
        InlineKeyboardButton(text="Промокоды🎁", callback_data="promo_codes")
    ]
]

films_button = [
    [
        InlineKeyboardButton(text='Введите фильм иил сериал, который хотите найти', callback_data="films")
    ]
]


admin_button = [
    [
        InlineKeyboardButton(text="Статистика🪪", callback_data="a_stat"),
        InlineKeyboardButton(text="Пользовательское меню🔙", callback_data="a_menu")
    ],
    [
        InlineKeyboardButton(text="Рассылка✔️", callback_data="mailing"),
        InlineKeyboardButton(text="Возможности✨", callback_data="a_opportunities")
    ],
    [
        InlineKeyboardButton(text="Каналы🪬", callback_data="channels")
    ]
]

a_opportunities_button = [
    [
        InlineKeyboardButton(text="Список админов", callback_data="list_admin"),

    ],
    [
        InlineKeyboardButton(text="Добавить админа", callback_data="add_admin"),
        InlineKeyboardButton(text="удалить админа", callback_data="delete_admin")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="back_a_m")
    ]
]

a_stat_button = [
    [
        InlineKeyboardButton(text="Отоброжение пользователей🪬", callback_data="s_full_users")
    ],
    [
        InlineKeyboardButton(text="Блокировка пользователя🗿", callback_data="s_block"),
        InlineKeyboardButton(text="Удаление пользователя❌", callback_data="s_del")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="back_a_m")
    ]
]


back_button = [
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="f_menu")
    ]
]

a_mailing_button = [
    [
        InlineKeyboardButton(text="Добавить✔️", callback_data="a_m_add"),
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="back_a_m")
    ]
]

a_channels_button = [
    [
        InlineKeyboardButton(text="Добавить✔️", callback_data="a_c_add"),
        InlineKeyboardButton(text="удалить❌", callback_data="a_c_delete")
    ],
    [
        InlineKeyboardButton(text='Вернуться в админ меню🔙', callback_data="back_a_m")
    ]
]

admin_menu_button = [
    [
        InlineKeyboardButton(text='Вернуться в админ меню🔙', callback_data="back_a_m")
    ]
]

