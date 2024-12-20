import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Данные для обучения
messages = [
    "Привет, бот!",          # 1
    "МЯУ",  # 0
    "Помоги мне, пожалуйста.",  # 1
    "?????????",              # 0
    "Здравствуй!",           # 1
    "Удалить это сообщение.", # 0
    "У меня вопрос.",         # 1
    "Спам",                   # 0
    "Как дела, бот?",         # 1
    "........",               # 0
    "Что-то интересное!"      # 1
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # Метки (1 - ответить, 0 - игнорировать)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(messages, labels, test_size=0.3, random_state=42)

# Преобразование текста в числовые признаки
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Обучение модели
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Оценка точности
y_pred = model.predict(X_test_vec)
print(f"Точность модели: {accuracy_score(y_test, y_pred):.2f}")

# Сохранение модели и векторизатора
joblib.dump(model, "bot_response_model.pkl")
joblib.dump(vectorizer, "bot_response_vectorizer.pkl")
print("Модель и векторизатор сохранены в файлы.")

# Загрузка модели и векторизатора
loaded_model = joblib.load("bot_response_model.pkl")
loaded_vectorizer = joblib.load("bot_response_vectorizer.pkl")

# Функция для проверки сообщений
def should_respond_ml(message):
    message_vec = loaded_vectorizer.transform([message])
    prediction = loaded_model.predict(message_vec)
    return prediction[0] == 1  # True, если модель решила отвечать

# Тестирование
test_messages = [
    "мяу",  # Ожидаем True
    "Спам сообщение",     # Ожидаем False
    "Что ты умеешь?",     # Ожидаем True
    "......",             # Ожидаем False
]

for msg in test_messages:
    print(f"Сообщение: \"{msg}\" => Ответить: {should_respond_ml(msg)}")
