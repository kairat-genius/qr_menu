FROM node:20-alpine
WORKDIR /app

# Копируем только package.json и package-lock.json
COPY package.json package-lock.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы
COPY . .

# Открываем порт
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "dev"]