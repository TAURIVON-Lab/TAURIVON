
import ast
import operator
import random
import re
import sys
import time
from datetime import datetime
from collections import deque


# ============================================================
# TAURIVON SOFTWARE
# ChatEPT v0.2 - Dialogue Edition
# Author: Yehor Derii
# ============================================================

VERSION = "0.2"
THINK_SECONDS = 3
TYPE_DELAY = 0.015
MAX_HISTORY = 30


# -------------------- ВИВЕДЕННЯ --------------------

def print_slow(text, delay=TYPE_DELAY):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def think():
    stages = [
        "Аналіз повідомлення",
        "Обробка контексту діалогу",
        "Формування відповіді"
    ]

    if THINK_SECONDS <= 0:
        return

    print()

    for i, stage in enumerate(stages):
        progress = int((i + 1) / len(stages) * 100)
        bar = "█" * (progress // 4) + "░" * (25 - progress // 4)

        sys.stdout.write(
            f"\r[ChatEPT] [{bar}] {progress}% | {stage}..."
        )
        sys.stdout.flush()

        time.sleep(THINK_SECONDS / len(stages))

    print("\n")


# -------------------- БЕЗПЕЧНА МАТЕМАТИКА --------------------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


def safe_calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        def calculate(node):
            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    if abs(node.value) > 10**12:
                        raise ValueError("Занадто велике число")
                    return node.value

            if isinstance(node, ast.BinOp):
                left = calculate(node.left)
                right = calculate(node.right)

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Недозволена операція")

                if isinstance(node.op, ast.Pow):
                    if abs(right) > 10 or abs(left) > 10**6:
                        raise ValueError("Завеликий степінь")

                result = operation(left, right)

                if isinstance(result, (int, float)):
                    if abs(result) > 10**100:
                        raise ValueError("Результат занадто великий")

                return result

            if isinstance(node, ast.UnaryOp):
                operation = UNARY_OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Недозволена операція")

                return operation(calculate(node.operand))

            raise ValueError("Непідтримуваний вираз")

        result = calculate(tree)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result

    except ZeroDivisionError:
        return "Помилка: ділення на нуль!"

    except Exception:
        return None


# -------------------- CHAT MEMORY --------------------

class ChatMemory:

    def __init__(self):
        self.history = deque(maxlen=MAX_HISTORY)
        self.username = None
        self.last_topic = None

    def remember(self, user, bot):
        self.history.append({
            "user": user,
            "bot": bot
        })

    def clear(self):
        self.history.clear()
        self.username = None
        self.last_topic = None


# -------------------- CHAT ENGINE --------------------

class ChatEPT:

    def __init__(self):
        self.memory = ChatMemory()

        self.greetings = [
            "Привіт! Радий тебе бачити!",
            "Вітаю! ChatEPT готовий до розмови!",
            "Здоров! Як твої справи?",
            "Привіт! Що сьогодні обговоримо?"
        ]

        self.responses = [
            "Цікава думка! Розкажи про це детальніше.",
            "Зрозумів тебе. А що думаєш про це сам?",
            "Можеш пояснити трохи більше?",
            "Цікаво! Продовжуй, я слухаю."
        ]

    # -------------------- ГОЛОВНА ОБРОБКА --------------------

    def respond(self, message):

        text = message.lower().strip()
        clean = re.sub(r"[^\w\s]", "", text)

        # Привітання
        if any(x in clean for x in [
            "привіт", "вітаю", "здоров", "добрий день",
            "добрий вечір", "доброго ранку", "hello", "hi"
        ]):
            self.memory.last_topic = "greeting"
            return random.choice(self.greetings)

        # Представлення користувача
        name_match = re.search(
            r"(?:мене звати|моє ім'я|моє ім’я|я)\s+"
            r"([а-яіїєґa-z][а-яіїєґa-z'-]{1,25})",
            text
        )

        if name_match and not text.startswith("який"):
            name = name_match.group(1).capitalize()

            if name not in ["Хочу", "Можу", "Буду", "Думаю"]:
                self.memory.username = name
                self.memory.last_topic = "name"

                return f"Приємно познайомитися, {name}! Я запам'ятаю твоє ім'я до завершення сеансу."

        # Ім'я користувача
        if any(x in clean for x in [
            "як мене звати",
            "ти памятаєш моє імя",
            "моє імя"
        ]):
            if self.memory.username:
                return f"Звичайно! Тебе звати {self.memory.username}."

            return "Ти ще не назвав свого імені. Напиши: мене звати Єгор."

        # Хто ти?
        if any(x in clean for x in [
            "хто ти", "що ти таке",
            "як тебе звати", "представся"
        ]):
            self.memory.last_topic = "identity"
            return (
                "Я ChatEPT v0.2 — локальний консольний "
                "діалоговий бот, створений у межах TAURIVON Software!"
            )

        # Автор
        if any(x in clean for x in [
            "хто тебе створив",
            "хто твій автор",
            "хто тебе зробив",
            "хто розробник"
        ]):
            self.memory.last_topic = "creator"
            return (
                "Мене створив Єгор Дерій — засновник "
                "технологічного бренду TAURIVON!"
            )

        # TAURIVON
        if "taurivon" in clean or "тауривон" in clean:
            self.memory.last_topic = "taurivon"
            return (
                "TAURIVON — незалежний технологічний бренд "
                "Єгора Дерія. Його напрямки: програмування, "
                "штучний інтелект, програмне забезпечення та ігри."
            )

        # Як справи?
        if any(x in clean for x in [
            "як справи", "як ти", "що робиш",
            "як поживаєш"
        ]):
            self.memory.last_topic = "mood"
            return random.choice([
                "Усе добре! Готовий продовжувати нашу розмову.",
                "Працюю стабільно та чекаю на твої запитання!",
                "Чудово! А як твої справи?"
            ])

        # Подяка
        if any(x in clean for x in [
            "дякую", "спасибі", "дуже дякую"
        ]):
            return random.choice([
                "Будь ласка! Завжди радий допомогти.",
                "Нема за що!",
                "Радий, що допоміг!"
            ])

        # Погода
        if "погода" in clean:
            return (
                "Я поки не підключений до сервісу прогнозу погоди. "
                "Але можу допомогти проаналізувати погодні дані, "
                "якщо ти їх надішлеш."
            )

        # Час
        if "час" in clean or "година" in clean:
            return (
                "Зараз " +
                datetime.now().strftime("%H:%M:%S") +
                " за системним годинником."
            )

        # Дата
        if "дата" in clean or "число сьогодні" in clean:
            return datetime.now().strftime(
                "Сьогодні %d.%m.%Y"
            )

        # Математика
        math_text = re.sub(
            r"^(скільки буде|порахуй|обчисли)\s*",
            "",
            text
        )

        math_text = math_text.replace(",", ".")

        if re.fullmatch(r"[\d\s.+*/()%\-]+", math_text):
            result = safe_calculate(math_text)

            if result is not None:
                return f"Результат обчислення: {result}"

            return "Не вдалося обчислити вираз. Перевір його правильність."

        # Контекстні відповіді
        if clean in ["а чому", "чому", "чому саме", "навіщо"]:
            if self.memory.last_topic == "creator":
                return "Єгор створив мене як експериментальний проєкт для розвитку TAURIVON."
            if self.memory.last_topic == "identity":
                return "Я створений для спілкування, експериментів із логікою та розвитку діалогових систем."
            return "Можеш уточнити, про що саме запитуєш?"

        if clean in ["розкажи більше", "детальніше", "продовжуй"]:
            if self.memory.last_topic == "creator":
                return "Єгор розвиває TAURIVON як власну технологічну екосистему."
            if self.memory.last_topic == "taurivon":
                return "Серед напрямків TAURIVON — ChatEPT, Security Hub, програмування та майбутні технологічні розробки."
            return "Звичайно! Про яку саме тему хочеш дізнатися більше?"

        # Контекст попередніх повідомлень
        if clean in ["так", "ага", "зрозуміло", "добре"]:
            return "Чудово! Продовжимо. Що ще тебе цікавить?"

        if clean in ["ні", "не знаю"]:
            return "Нічого страшного. Можемо розібратися разом."

        # Резервна відповідь
        return random.choice(self.responses)


# -------------------- КОМАНДИ --------------------

def show_help():
    print("""
КОМАНДИ ChatEPT:

/help       - список команд
/history    - історія розмови
/clear      - очистити пам'ять
/time       - поточний час
/about      - інформація про програму
/exit       - завершити роботу

Можна спілкуватися звичайними повідомленнями.
""")


def show_history(memory):
    print("\n========== ІСТОРІЯ ==========")

    if not memory.history:
        print("Історія порожня.")
    else:
        for item in memory.history:
            print(f"\nТи: {item['user']}")
            print(f"ChatEPT: {item['bot']}")

    print("=============================\n")


# -------------------- ЗАПУСК --------------------

def chatept_bot():

    bot = ChatEPT()

    print("=" * 65)
    print("       TAURIVON SOFTWARE - ChatEPT v0.2")
    print("              DIALOGUE EDITION")
    print("=" * 65)

    print("Локальний діалоговий режим активовано.")
    print("Пам'ять діалогу: активна.")
    print("Напиши /help для перегляду команд.")
    print("Напиши /exit для завершення.\n")

    print_slow("ChatEPT: Вітаю! Я готовий до спілкування. ♉")

    while True:

        try:
            user_input = input("\nТи: ").strip()

            if not user_input:
                continue

            command = user_input.lower()

            if command in ["/exit", "вихід", "exit", "quit"]:
                print_slow(
                    "ChatEPT: Завершую роботу. "
                    "До зустрічі у наступній версії TAURIVON! ♉"
                )
                break

            if command == "/help":
                show_help()
                continue

            if command == "/history":
                show_history(bot.memory)
                continue

            if command == "/clear":
                bot.memory.clear()
                print("ChatEPT: Пам'ять діалогу очищено.")
                continue

            if command == "/time":
                print("ChatEPT:", datetime.now().strftime("%H:%M:%S"))
                continue

            if command == "/about":
                print(
                    f"ChatEPT v{VERSION} | "
                    "TAURIVON Software | Dialogue Edition"
                )
                continue

            think()

            response = bot.respond(user_input)

            bot.memory.remember(user_input, response)

            print_slow("ChatEPT: " + response)

        except KeyboardInterrupt:
            print("\n\nChatEPT: Сеанс перервано. До зустрічі!")
            break

        except EOFError:
            print("\nChatEPT: Завершення сеансу.")
            break


if __name__ == "__main__":
    chatept_bot()
