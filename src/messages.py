start_msg = "🌕 Добро пожаловать, {username} \n\n" \
            "🌖 Бот работает в штатном режиме \n" \
            "🌗 Если не появились вспомогательные кнопки \n" \
            "🌘 Введите /start \n\n" \

profile_msg = "👤 <b>Логин:</b> @{username}\n" \
              "🔑 <b>ID:</b> {user_id}\n" \
              "🕑 <b>Регистрация:</b> {registration_date}\n\n" \
              "💲 <b>Баланс:</b> {balance}"

refill_methods_msg = "💰 Выберите способ пополнения"

card_payment_msg = "💰 Введите сумму пополнения"

crypto_payment_msg = "💰 Введите сумму пополнения (от 100 руб.)"

wrong_refill_value = "❌ Данные были введены неверно.\n"\
                     "💰 Введите сумму для пополнения средств"

help_msg = f"❗ Правила:\n\n" \
           f"<b>1.</b> Пользователь согласен, что время обработки заявки занимает до 1 рабочего дня.\n\n" \
           f"поддержки/доступа к боту без дальнейшей помощи в разбирательстве вашей проблемы.\n\n" \
           f"<b>1.2</b> Фиксируйте покупку на видео. Начинайте запись видео до того как " \
           f"нажали на кнопку \"купить\", не завершая запись продолжайте проверку товара, " \
           f"если есть такая возможность. При невалидности товара замена " \
           f"выдаётся при наличии пруфов в течение 30 минут после покупки.\n\n" \
           f"<b>1.3</b> Возврат средств происходит только на баланс бота.\n\n" \
           f"<b>1.4</b> В случае, если способ получения фиксят и товар не выдан -  осуществляется возврат. " \
           f"Если товар выдан и был отобран самой компанией - возврат не осуществляется\n\n" \
           f"<b>1.5</b> Приобретая товар, вы обязуетесь воспользоваться услугой в течение 24ч"

catalog_msg = 'Выберите категорию:'

items_msg = 'Выберите товар:'

item_msg = "<b>Покупка товара</b>\n\n"\
           "<b>Название:</b> {name}\n"\
           "<b>Стоимость:</b> {price}\n\n"\
           "<b>Описание:</b> \n{description}"

purchases_msg = "🕑 Дата покупки: {order_date}\n"\
                "🛒 Товар: {item_name}\n"\
                "💰 Цена: {price}\n\n"

no_purchases_msg = '❗ У вас отсутствуют покупки'

buy_item_msg = "<b>Вы действительно хотите купить этот товар?</b>\n\n"\
               "<b>🛒 Товар</b>: {item_name}\n"\
               "<b>💰 Сумма к оплате:</b> {price}"

cancelled_purchase_msg = "❗ <b>У вас недостаточно средств на счету</b>"

succeed_purchase_msg = "✅ <b>Покупка прошла успешно</b>\n\n"\
                       "<b>Товар:</b> {item_name}\n"\
                       "<b>Сумма покупки:</b> {price}\n"\
                       "<b>Покупатель:</b> @{username} ({user_id})\n"\
                       "<b>Дата покупки:</b> {order_date}"
