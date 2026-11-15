import time
import sys
import random
from datetime import datetime

def print_slow(text, delay=0.03):
    """Імітує процес друкування тексту штучним інтелектом"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def simulate_thinking():
    """Спеціальний цикл: 50 секунд процесу + пауза + 50 секунд фіналу (разом 100 с)"""
    stages_phase_1 = [
        "Аналіз вхідного тексту...",
        "Пошук збігів у базі знань TAURIVON...",
        "Первинна обробка токенів..."
    ]
    
    stages_phase_2 = [
        "Глибокий синтез нейронних зв'язків...",
        "Фінальна перевірка та форматування відповіді..."
    ]
    
    print()
    
    # Фаза 1: Перші 50 секунд (0% - 50%)
    for i in range(1, 51):
        stage_index = min(int((i / 50) * len(stages_phase_1)), len(stages_phase_1) - 1)
        current_stage = stages_phase_1[stage_index]
        
        percent = int((i / 100) * 100)
        filled_length = int(25 * i // 100)
        bar = '█' * filled_length + '░' * (25 - filled_length)
        
        sys.stdout.write(f"\r[ChatEPT] [{bar}] {percent}% | {i}/100с | {current_stage}   ")
        sys.stdout.flush()
        time.sleep(1)
        
    # Коротка пауза «на роздуми» посередині
    sys.stdout.write(f"\r[ChatEPT] [████████████░░░░░░░░░░░░░] 50% | 50/100с | Пауза для глибокого аналізу...       ")
    sys.stdout.flush()
    time.sleep(3) # Невеличка додаткова пауза (можна прибрати, якщо не потрібна)

    # Фаза 2: Наступні 50 секунд (51% - 100%)
    for i in range(51, 101):
        # Коригуємо індекс для другої фази
        adjusted_i = i - 50
        stage_index = min(int((adjusted_i / 50) * len(stages_phase_2)), len(stages_phase_2) - 1)
        current_stage = stages_phase_2[stage_index]
        
        percent = int((i / 100) * 100)
        filled_length = int(25 * i // 100)
        bar = '█' * filled_length + '░' * (25 - filled_length)
        
        sys.stdout.write(f"\r[ChatEPT] [{bar}] {percent}% | {i}/100с | {current_stage}   ")
        sys.stdout.flush()
        time.sleep(1)
        
    print("\n")

def chatept_bot():
    print("=" * 65)
    print("  TAURIVON SOFTWARE - ChatEPT v0.1 (Two-Stage Thinking)")
    print("  Автор / Засновник: Дерій Єгор")
    print("=" * 65)
    print("ШІ ініціалізовано. Режим очікування: 50с аналізу + 50с фіналу.")
    print("Напиши 'вихід' або 'exit', щоб завершити роботу.\n")

    greetings = [
        "Вітаю! Я ChatEPT 0.1, твоя перша локальна модель від TAURIVON.",
        "Привіт! Я провів повний 100-секундний цикл аналізу твого привітання.",
        "Здоровчик! Мої алгоритми завершили обчислення."
    ]

    creators = [
        "Мене створив геніальний розробник Дерій Єгор у межах екосистеми TAURIVON!",
        "Мій творець — Єгор Дерій. Я є першим продуктом TAURIVON Software."
    ]

    how_are_you = [
        "У мене все чудово, 100 секунд подвійного розрахунку пройшли успішно!",
        "Стабільний політ! Локальна нейромережа працює як годинник.",
        "Чудово! Готовий до наступних завдань."
    ]

    while True:
        try:
            user_input = input("\nТи: ").strip().lower()
            
            if not user_input:
                continue

            if user_input in ["вихід", "exit", "quit", "пака", "бувай"]:
                print_slow("\nChatEPT: Завершую роботу... До зустрічі у версії 0.2! ♉")
                break

            # Запускаємо 100-секундний двоетапний цикл
            simulate_thinking()

            response = ""

            if any(word in user_input for word in ["привіт", "вітаю", "здорово", "hello", "hi"]):
                response = random.choice(greetings)

            elif any(word in user_input for word in ["хто тебе створив", "хто твій автор", "тебе зробив", "єгор"]):
                response = random.choice(creators)

            elif any(word in user_input for word in ["як справи", "як ти", "що робиш"]):
                response = random.choice(how_are_you)

            elif "час" in user_input or "година" in user_input:
                current_time = datetime.now().strftime("%H:%M:%S")
                response = f"Поточний час на системному годиннику (після 100 секунд обчислень): {current_time}"

            elif "тауривон" in user_input or "taurivon" in user_input:
                response = "TAURIVON — це технологічний бренд і екосистема майбутнього, створена Єгором Дерієм!"

            elif "погода" in user_input:
                response = "Я консольний бот, але після 100 секунд роздумів впевнений, що погода сьогодні чудова!"

            elif "+" in user_input or "-" in user_input or "*" in user_input or "/" in user_input:
                try:
                    result = eval(user_input)
                    response = f"Результат обчислення: {result}"
                except:
                    response = "Я бачив цей математичний приклад під час 100-секундного аналізу, але не зміг його порахувати."

            else:
                fallbacks = [
                    "Цікаве запитання! Я думав над ним цілих 100 секунд у два етапи. У версії ChatEPT 0.1 мій словник ще базовий.",
                    "Я проаналізував твій запит на повну потужність процесора. У наступних оновленнях база знань стане ширшою!",
                    "Зрозумів тебе. Записав у свій код для майбутніх оновлень TAURIVON."
                ]
                response = random.choice(fallbacks)

            print_slow(f"ChatEPT: {response}")

        except KeyboardInterrupt:
            print("\n\nChatEPT: Екстрене завершення сеансу. Бувай!")
            break

if __name__ == "__main__":
    chatept_bot()
