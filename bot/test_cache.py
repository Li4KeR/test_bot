""" NAILS BLOCK """
@dp.callback_query_handler(lambda call: "main_nails" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    """основное меню ногти"""
    await call.message.edit_text(
        text="Выберете мастера или дату, "
             "когда хотите посетить мастера\n"
             "Так же можете посмотреть прайс."
    )
    await call.message.edit_reply_markup(reply_markup=nails)
    await call.answer()


@dp.callback_query_handler(lambda call: "main_nails" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    """основное меню ногти"""
    await call.message.edit_text(
        text="Выберете мастера или дату, "
             "когда хотите посетить мастера\n"
             "Так же можете посмотреть прайс."
    )
    await call.message.edit_reply_markup(reply_markup=nails)
    await call.answer()

    @dp.callback_query_handler(Text(startswith="nails_master"))
    async def callbacks_num(call: types.CallbackQuery):
        """меню с информацией мастера ногтей"""
        master_id = call.data.split("nails_master")[1]
        """ some func for pars data master """
        master_name = "Алла"
        free_dates = "даты? потом парс времени?"
        master_details = "Могу то, могу сё. Еще инфа и тп."

        menu_master = types.InlineKeyboardMarkup(row_width=2)

        menu_master.add(
            InlineKeyboardButton(text="Подробнее", callback_data=f"nails_master_info_{master_id}"),
            InlineKeyboardButton(text=f"Календарь", callback_data=f"nails_master_calendar_id_{master_id}"),
            InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
        )
        """ end func """
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main"))
        await call.message.edit_text(text=f"Мастер {master_name}\n{master_details}")
        await call.message.edit_reply_markup(reply_markup=menu_master)
        await call.answer()