# Use an official Node.js runtime as a parent image
FROM node:16.13.0

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Install app dependencies, including jwt-decode
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]

