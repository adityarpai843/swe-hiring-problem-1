# Use Node.js 16 as the base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy dependency files and install dependencies
COPY package.json package-lock.json . 
RUN npm install

# Copy the rest of the application code
COPY . .

# Run migrations and start the application
CMD ["sh", "-c", "npx sequelize-cli db:migrate && node index.js"]
