FROM python

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt /app/
COPY . /app/


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда для запуска приложения с gunicorn
CMD ["gunicorn", "chat_project.wsgi:application", "--bind", "0.0.0.0:8000"]
