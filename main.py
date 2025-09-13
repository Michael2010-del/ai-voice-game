import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
import random 



words_by_level = {
    "easy": [
        "кот", "собака", "дом", "стол", "стул", 
        "мяч", "книга", "рука", "нога", "голова",
        "солнце", "луна", "звезда", "вода", "огонь",
        "мама", "папа", "сын", "дочь", "друг",
        "хлеб", "молоко", "сок", "сыр", "яблоко",
        "груша", "кошка", "птица", "рыба", "цветок"
    ],
    "medium": [
        "школа", "учитель", "ученик", "урок", "тетрадь",
        "карандаш", "ручка", "доска", "класс", "знание",
        "город", "улица", "парк", "магазин", "библиотека",
        "работа", "доктор", "инженер", "программист", "художник",
        "время", "час", "минута", "неделя", "месяц",
        "год", "погода", "дождь", "снег", "ветер"
    ],
    "hard": [
        "университет", "образование", "технология", "информация", "компьютер",
        "программа", "алгоритм", "интернет", "сообщество", "правительство",
        "искусство", "литература", "музыка", "театр", "кинематограф",
        "медицина", "биология", "химия", "физика", "математика",
        "философия", "психология", "экономика", "политика", "история",
        "география", "архитектура", "инженерия", "исследование", "эксперимент"
    ]
}

duration = 3  # секунды записи
sample_rate = 44100

print("🎮" * 30)
print("🎯Говори правильно🎯")
print("🎮" * 30)
print("📜Правила игры:")
print("Тебе покажут слово на русском")
print("Ты должен произнести перевод на английском")
print("У тебя есть 3 жизни")
print("За каждый правильный ответ +10 очков")
print("3 ошибки - игра закончена")
print("🎯Готов проверить свои знания? Поехали!")
print("🎮" * 30)

# Главный игровой цикл
while True:
    # Сброс игры
    score = 0
    lives = 3
    level = ""
    
    print("\n" + "=" * 50)
    print("🎮 НОВАЯ ИГРА!")
    print("=" * 50)
    
    # Выбор уровня сложности
    print("\nВыберите уровень:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Выйти из игры")
    
    choice = input("Введите номер (1-4): ")
    
    if choice == "4":
        print("👋 До свидания!")
        break
    
    if choice == "1":
        level = "easy"
        print("✅ Вы выбрали легкий уровень")
    elif choice == "2":
        level = "medium"
        print("✅ Вы выбрали средний уровень")
    elif choice == "3":
        level = "hard"
        print("✅ Вы выбрали продвинутый уровень")
    else:
        print("❌ Некорректный выбор, установлен легкий уровень")
        level = "easy"
    
    # Игровой раунд
    while lives > 0:
        print(f"\n❤️ Жизни: {lives} | 💯 Очки: {score}")
        print("-" * 40)
        
        # Выбираем случайное слово
        russian_word = random.choice(words_by_level[level])
        print(f"📝 Скажи на английском: {russian_word}")
        
        print("🎤 Говори... (запись 3 секунды)")
        
        # Запись аудио
        try:
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()
            
            # Сохранение и распознавание
            wav.write("output.wav", sample_rate, recording)
            
            recognizer = sr.Recognizer()
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)
            
            try:
                english_text = recognizer.recognize_google(audio, language="en-US")
                print(f"🎤 Ты сказал: {english_text}")
                
                # Перевод обратно для проверки
                try:
                    translated_back = GoogleTranslator(source="auto", target="ru").translate(english_text)
                    print(f"🌍 Обратный перевод: {translated_back}")
                    
                    # Проверка правильности
                    if translated_back.lower() == russian_word.lower():
                        score += 10
                        print("✅ Правильно! +10 очков!")
                        print("🎉 Отлично! Следующее слово...")
                    else:
                        lives -= 1
                        print(f"❌ Неправильно! Правильный ответ: {russian_word}")
                        print(f"💔 Осталось жизней: {lives}")
                        
                except Exception as e:
                    lives -= 1
                    print(f"❌ Ошибка перевода! Осталось жизней: {lives}")
                    
            except sr.UnknownValueError:
                lives -= 1
                print(f"❌ Не удалось распознать речь! Осталось жизней: {lives}")
            except sr.RequestError as e:
                lives -= 1
                print(f"❌ Ошибка сервиса распознавания! Осталось жизней: {lives}")
                
        except Exception as e:
            lives -= 1
            print(f"❌ Ошибка записи звука! Осталось жизней: {lives}")
    
    # Конец раунда
    print("\n" + "🎮" * 30)
    print("🎯 Игра окончена!")
    print(f"💯 Ваш финальный счет: {score} очков")
    print("🎮" * 30)
    
    if score >= 30:
        print("🏆 Отличный результат! Вы молодец!")
    elif score >= 10:
        print("👍 Хорошая попытка! Можете лучше!")
    else:
        print("👎 Не расстраивайтесь! Попробуйте еще раз!")
    
    # Предложение сыграть again
    print("\nХотите сыграть еще раз?")
    play_again = input("Введите 'да' для продолжения или 'нет' для выхода: ")
    
    if play_again.lower() != 'да':
        print("👋 Спасибо за игру! До свидания!")
        break

print("\nИгра завершена!")
