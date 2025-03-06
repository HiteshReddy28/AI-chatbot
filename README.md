# AI Negotiator - Full Project Setup Guide

AI Negotiator is a chatbot application that helps users interact with AI for loan negotiations. This guide will walk you through **installing, setting up, and running the project locally**.

---

## **Prerequisites**
Before starting, make sure you have the following installed:

- **Python (3.8+)** → [Download Here](https://www.python.org/downloads/)
- **PostgreSQL** → [Download Here](https://www.postgresql.org/download/)
- **Node.js (16+)** → [Download Here](https://nodejs.org/)
- **Git** → [Download Here](https://git-scm.com/)

---

## **Step 1: Clone the Repository**
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Negotiator.git
cd AI-Negotiator
```

---

## **Step 2: Set Up PostgreSQL Database**
Your database must be installed locally. Follow these steps:

### **1. Start PostgreSQL**
- **Mac:**  
  ```sh
  brew install postgresql
  brew services start postgresql
  ```

- **Windows:**  
  1. Install PostgreSQL from [this link](https://www.postgresql.org/download/).
  2. Open **pgAdmin** or use **Command Prompt (cmd)**:
     ```sh
     psql -U postgres
     ```

### **2. Create Database & User**
Run these SQL commands inside `psql`:
```sql
CREATE DATABASE ainegotiator;
CREATE USER admin WITH ENCRYPTED PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE ainegotiator TO admin;
```

### **3. Create Required Tables**
Run the following inside **PostgreSQL** (`psql`):
```sql
\c ainegotiator;  -- Connect to the database

CREATE TABLE users (
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    ssn VARCHAR(20),
    loan_amount DECIMAL(10,2)
);

CREATE TABLE chat_sessions (
    session_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES users(client_id) ON DELETE CASCADE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    session_id INT REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    sender VARCHAR(10) CHECK (sender IN ('user', 'bot')),
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

✅ **Now, your database is set up and ready to use.**

---

## **Step 3: Set Up Environment Variables**
Inside the project **root folder**, create a `.env` file:

```ini
DATABASE_URL=postgresql://admin:yourpassword@localhost:5432/ainegotiator
```

🔹 **Replace `yourpassword`** with the actual password you set for the `admin` user.

---

## **Step 4: Install & Run the Backend**
### **1. Navigate to the Backend Folder**
```sh
cd backend
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
```

### **3. Activate the Virtual Environment**
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```

### **4. Install Required Dependencies**
```sh
pip install -r requirements.txt
```

If `requirements.txt` does not exist, manually install:
```sh
pip install fastapi uvicorn psycopg2-binary passlib python-dotenv
```

### **5. Run the Backend**
```sh
uvicorn AiNegotiator:app --reload
```

---

## **Step 5: Install & Run the Frontend**
### **1. Navigate to the Frontend Folder**
```sh
cd ../frontend
```

### **2. Install Dependencies**
```sh
npm install
```

### **3. Start the Frontend**
```sh
npm start
```

✅ **Your app should now be available at:**  
🔗 **http://localhost:3000**

---

## **Step 6: Test the Full Application**
1. **Visit** `http://localhost:3000` and create an account.
2. **Login** and start chatting with the AI chatbot.
3. **Chat history** should be stored in PostgreSQL.
4. **Check stored chats** using:
   ```sql
   SELECT * FROM chat_history;
   ```

---

## **📌 Contribution**
If you’d like to improve this project, follow these steps:

1. **Fork the Repository**  
2. **Create a New Branch**  
   ```sh
   git checkout -b feature-branch
   ```
3. **Make Your Changes & Commit**  
   ```sh
   git add .
   git commit -m "Added a new feature"
   ```
4. **Push to GitHub & Open a Pull Request**  
   ```sh
   git push origin feature-branch
   ```

---

## **📌 License**
This project is open-source and available under the **MIT License**.

---
