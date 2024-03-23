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
        InlineKeyboardButton(text="Сериалы📼", callback_data="serials")
    ],
    [
        InlineKeyboardButton(text="Аниме🎭", callback_data="anime"),
        InlineKeyboardButton(text="Подборка🛒", callback_data="Compilation")
    ],
    [
        InlineKeyboardButton(text="Подписка📜", callback_data="subscription"),
        InlineKeyboardButton(text="Промокоды🎁", callback_data="promo_codes")
    ]
]

films_button = [
    [
        InlineKeyboardButton(text="Трилерры🔦", callback_data="f_thrillers"),
        InlineKeyboardButton(text="Приключения🏹", callback_data="f_adventures")
    ],
    [
        InlineKeyboardButton(text="Детективы🔍", callback_data="f_detectives"),
        InlineKeyboardButton(text="Семейные👨‍👩‍👧‍👦", callback_data="f_family")
    ],
    [
        InlineKeyboardButton(text="Мелодрамы💖", callback_data="f_melodramas"),
        InlineKeyboardButton(text="Комедии😂", callback_data="f_comedies")
    ],
    [
        InlineKeyboardButton(text="Фантастика👽", callback_data="f_fantasy"),
        InlineKeyboardButton(text="Фэнтази🐲", callback_data="f_fantasy")
    ],
    [
        InlineKeyboardButton(text="Боевики🔫", callback_data="f_fighters"),
        InlineKeyboardButton(text="Криминальные⚖️", callback_data="f_criminal")
    ],
    [
        InlineKeyboardButton(text="Ужасы😱", callback_data="f_horrors"),
        InlineKeyboardButton(text="Драмы🪦", callback_data="f_Dramas")
    ],
    [
        InlineKeyboardButton(text="Биография👨‍🚀", callback_data="f_biography"),
        InlineKeyboardButton(text="Документалка🌍", callback_data="f_documentary")
    ],
    [
        InlineKeyboardButton(text="Вестерны🤠", callback_data="f_westerns"),
        InlineKeyboardButton(text="Мистика🔮", callback_data="f_mysticism")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="f_menu"),

    ]
]

serials_button = [
    [
        InlineKeyboardButton(text="Трилерры🔦", callback_data="s_thrillers"),
        InlineKeyboardButton(text="Приключения🏹", callback_data="f_adventures")
    ],
    [
        InlineKeyboardButton(text="Детективы🔍", callback_data="s_detectives"),
        InlineKeyboardButton(text="Семейные👨‍👩‍👧‍👦", callback_data="s_family")
    ],
    [
        InlineKeyboardButton(text="Мелодрамы💖", callback_data="s_melodramas"),
        InlineKeyboardButton(text="Комедии😂", callback_data="s_comedies")
    ],
    [
        InlineKeyboardButton(text="Фантастика👽", callback_data="s_fantasy"),
        InlineKeyboardButton(text="Фэнтази🐲", callback_data="s_fantasy")
    ],
    [
        InlineKeyboardButton(text="Боевики🔫", callback_data="s_fighters"),
        InlineKeyboardButton(text="Криминальные⚖️", callback_data="s_criminal")
    ],
    [
        InlineKeyboardButton(text="Ужасы😱", callback_data="s_horrors"),
        InlineKeyboardButton(text="Драмы🪦", callback_data="s_Dramas")
    ],
    [
        InlineKeyboardButton(text="Биография👨‍🚀", callback_data="s_biography"),
        InlineKeyboardButton(text="Документалка🌍", callback_data="s_documentary")
    ],
    [
        InlineKeyboardButton(text="Вестерны🤠", callback_data="s_westerns"),
        InlineKeyboardButton(text="Мистика🔮", callback_data="s_mysticism")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="f_menu")
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


anime_button = [
    [
        InlineKeyboardButton(text="Кодомо", callback_data="Codomo"),
        InlineKeyboardButton(text="Сёнэн", callback_data="senen")
    ],
    [
        InlineKeyboardButton(text="Сёдзё", callback_data="shojo"),
        InlineKeyboardButton(text="Сэйнэн", callback_data="seinen")
    ],
    [
        InlineKeyboardButton(text="Дзёсэй", callback_data="josei"),
        InlineKeyboardButton(text="Фэнтези", callback_data="a_fantasy")
    ],
    [
        InlineKeyboardButton(text="Научная фантастика", callback_data="science_fiction"),
        InlineKeyboardButton(text="Космическая опера", callback_data="space_opera")
    ],
    [
        InlineKeyboardButton(text="Апокалиптика", callback_data="the_apocalypse"),
        InlineKeyboardButton(text="Постапокалиптика", callback_data="post_apocalyptic")
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню🔙", callback_data="f_menu")
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

