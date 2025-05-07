import datetime
import json
import os
import random
import time
from datetime import datetime

import vk_api

# Конфиг
ACCESS_TOKEN = "vk1.a.7f5y8KLmlw2zgS2HN_W5cQxZ3lc0pNjWTYKUluWMOOov7CTIgsmmr30DdAwNHJ7d-4grIWD9g85NN7hQJN3FN3jmum7SWISMbxjJQ7vK9ZxOvKuZMdILEdVJfn66Exxupv3TWB0CbQ1Mm_N3X1LVlJsOpmtAs754ZbfKW9e9ne2uy_7VgMCSB5hg_z9Wr_-RWujTzJ-GOTpIx4fLLBnb0A"
GROUP_ID = "-152447212"
PROGRESS_FILE = "vk_progress.json"
TOTAL_POSTS_ESTIMATE = 130  # Примерное количество постов для статистики
COMMENT_MESSAGES = [
    "Отличный пост! 👍", "Интересно! 😊", "Спасибо за информацию! 🙏",
    "Классно! 🔥", "Лайк! ❤️", "Познавательно! 📚", "Супер! 👏",
    "Замечательно! 🌟", "Прекрасно! 💯", "Мне нравится! 😍",
    "Так-то! 😏", "Норм! 😎", "Пушка! 🚀", "Агонь! 🔥", "Топчик! 🏆",
    "Гоу! 🏃‍♂️", "Хайп! 🎤", "Бомбезно! 💣", "Рофл! 🤣",
    "Почему так? 🤔", "А подробнее? 🧐", "Это как? ❓", "Серьёзно? 😳",
    "И что теперь? 🎯", "Кто согласен? 🙋‍♂️", "Где логика? 🧠",
    "Вау! 😮", "Ого! 😲", "Ух ты! ✨", "Блин... 😅", "Ну и ну! 😼",
    "Как же круто! 🎉", "Обалдеть! 🤯", "Невероятно! 🌀", "Шок! 💥" "Это провал... 🕳️", "Жду продолжения! 📺",
    "Где мои попкорны? 🍿", "Вот это поворот! 🎭", "Спасите! 🆘",
    "Так держать! 💪", "Ты сможешь! 🦾", "Вперёд! ⏩", "Не сдавайся! 🏁",
    "Горжусь! 🥇", "Молодец! 👶", "Ты лучший! 🏅",
    "Звучит как план! 📝", "Я падаю... 🪂", "Это шедевр! 🎨",
    "Гениально! 🧩", "Фантастика! 🦄", "Магия! 🎩", "Космос! 🪐",
    "Спасибо за труд! 👨‍🏫", "Вы лучший педагог! 📖", "Примите благодарность! 🙇",
    "Нам так повезло с вами! 💝", "Ваши посты — огонь! 🔥", "Обожаю ваши материалы! 💌"]

# Дополняем смайлами
COMMENT_MESSAGES += [
                        f"Оцените мой смайл: {random.choice(['💩', '👽', '🍕'])}"] * 10


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"last_post": 0, "processed": 0, "start_time": time.time()}


def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)


def get_all_posts(vk, maxs):
    all_posts = []
    offset = 0
    count = 13

    print("\n⚡ Загрузка постов...")

    while True:
        try:
            chunk = vk.wall.get(owner_id=GROUP_ID, count=count, offset=offset)["items"]
            if not chunk:
                pass
                break
            if offset > maxs - 1:
                break
            all_posts.extend(chunk)
            offset += count

            print(
                f"🔄 Загружено: {len(all_posts)}/{TOTAL_POSTS_ESTIMATE} "
                f"({len(all_posts) / TOTAL_POSTS_ESTIMATE:.1%}) | "
                f"Время: {datetime.now().strftime('%H:%M:%S')}"
            )

            # time.sleep(0.5)

        except Exception as e:
            print(f"⚠ Ошибка: {e}")
            break

    print(f"\n🔥 Всего загружено: {len(all_posts)} постов")
    with open("data.json", "w") as f:
        json.dump(all_posts, f, indent=4)
    return all_posts


def process_post(vk, post, current, total, progress):
    post_id = post["id"]
    print("\n" + "=" * 50)
    print(f"📝 Пост {current}/{total} (ID: {post_id})")

    # Ставим лайк (без капчи)
    """    try:
        vk.likes.add(type="post", owner_id=GROUP_ID, item_id=post_id)
        print("💖 Лайк поставлен!")
    except Exception as e:
        print(f"❌ Ошибка лайка: {e}")"""

    # Пытаемся оставить комментарий (с обработкой капчи)
    comment_attempts = 0
    while comment_attempts < 10:  # 10 попыток на комментарий
        try:
            comment = random.choice(COMMENT_MESSAGES)
            vk.wall.createComment(owner_id=GROUP_ID, post_id=post_id, message=comment)
            print(f"💬 Коммент: «{comment}»")
            comment_attempts += 1
        except Captcha as e:
            print(f"⚠ Капча! Пропускаем комментарий к посту {post_id} {e}")
            time.sleep(7)
        except ApiError as e:
            print(f"❌ Ошибка коммента: {e}")
            time.sleep(5)

    # Обновляем прогресс
    progress['last_post'] = current
    delay = random.uniform(60, 65)
    print(f"⏳ Ждем {delay:.1f} сек...")
    save_progress(progress)
    time.sleep(delay)


def main(maxs):
    # Проверка токена
    if "ваш_токен" in ACCESS_TOKEN:
        print("❌ Вставьте рабочий токен!")
        return

    vk = vk_api.VkApi(token=ACCESS_TOKEN).get_api()
    progress = load_progress()

    try:
        print("\n" + "=" * 50)
        print(f"🚀 Старт обработки группы {GROUP_ID}")
        print(f"⏱ Время: {datetime.now().strftime('%d.%m %H:%M:%S')}")
        print("=" * 50)
        try:
            posts = get_all_posts(vk, maxs)
        except KeyboardInterrupt:
            print("Конец Работы")
            return
        if not posts:
            print("❌ Нет постов для обработки!")
            return

        total = len(posts)
        start_from = progress['last_post']

        print(f"\n🔍 Начинаем с позиции {start_from + 1}/{total}")
        for i in range(start_from, total):
            print("❗ Пост")
            print(posts[i]["text"])
            if "activity" in posts[i]:
                print("💬 Комментарии к посту:")
                for comment in posts[i]["activity"]["comments"]:
                    print(comment["text"])
            try:
                process_post(vk, posts[i], i + 1, total, progress)
            except KeyboardInterrupt:
                print("Конец работы")
                break
            except Exception as e:
                print(e)

        print("\n🎉 Все посты обработаны!")
    except Exception as e:
        print(f"\n🔥 Ошибка: {e}")
    finally:
        print("\nРабота завершена")


if __name__ == "__main__":
    main(129)
