# NewsArticlesManagement

This project is a news article management system built using **Flask**, which provides a web interface to track and load the number of articles published by various newspapers. The system includes features to add article counts, view reports of uploaded articles, and receive notifications when the number of articles is below a certain threshold based on historical data.

## Features

- **Article Uploads**: Load article counts for a given newspaper on a specific date.
- **Threshold Check**: Verify if the article count for a newspaper is below a calculated threshold based on the latest 6 months' data.
- **Notifications**: Display on-screen notifications when article counts are below the expected threshold (email or instant messaging notifications).
- **Weekly Report**: Display the number of articles uploaded by each newspaper during the last week.
- **Basic Statistical Model**: Implement basic statistical measures, including threshold checks, coefficient of variation, and interquartile range.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML templates and CSS
- **Database**: MySQL (XAMPP)

## Database Setup

This application uses **MySQL** as the database for storing information about newspapers and their article counts.

To set up the database, follow these steps:

1. **Install XAMPP**: If you haven't installed XAMPP, download and install it from [here](https://www.apachefriends.org/index.html).

2. **Create Database and Tables**:
     - Open phpMyAdmin via XAMPP.
     - Create a new database:
         ```sql
         CREATE DATABASE db_newspaper-analytic
         ```
     - Create the `articles` and `newspapers` tables:
       
         ```sql
         USE db_newspaper-analytic;

         CREATE TABLE newspapers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE
         );

         CREATE TABLE articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            newspaper_id INT NOT NULL,
            date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            article_count INT NOT NULL,
            FOREIGN KEY (newspaper_id) REFERENCES newspapers(id)
         );
         ```
3. **Sample Data (Optional)**:
    You can insert same sample data into the `newspapers` table:
   ```sql
   INSERT INTO newspapers (name) VALUES ('El tiempo'), ('La Nación'), ('O Globo');
   ```

## How to Run the application

### Step 1: Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/blandoncj/NewsArticlesManagement.git
cd NewsArticlesManagement
```

### Step 2: Create a Virtual Environment and Install Dependencies

1. **Create a virtual environment** (recommended):

  ```bash
  python -m venv venv
  ```

2. **Activate the virtual environment**
  - On Windows:

    ```bash
    venv\Scripts\Activate
    ```
  
  - On macOS/Linux:
  
    ```bash
    source venv/bin/activate
    ```
    
3. **Install the required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure Database connection

1. In the root folder, locate or create a `config.py` file to configure your database connection. Here's an example of what should be inside:

   ```python
     class Config:
      SECRET_KEY = 'your_secret_key' 

    class DevelopmentConfig(Config):
        DEBUG = True
        MYSQL_HOST = 'localhost'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = ''
        MYSQL_DB = 'db_newspaper-analytic'
    
    config = {
        'development': DevelopmentConfig
    }
   ```
   Replace with your MySQL credentials

### Step 4: Run the Application

Finally, start the application:

```bash
python main.py
```
The application should be accessible at `http://127.0.0.1:5000`.

## How It Works

1. **Loading Articles**: 
    - Users can select a newspaper and input the number of articles published on a given date. 
    - The system checks the average number of articles published on that day of the week over the past 6 months and compares it with the entered count.
  
2. **Threshold Notification**: 
    - If the number of articles is below a certain threshold (e.g., 80% of the average), the system will display an on-screen notification alerting the user.

3. **Weekly Report**: 
    - The system provides a report displaying the number of articles uploaded by each newspaper during the last 7 days.

4. **Mini Statistical Model**: 
    - The system calculates basic statistics such as averages, coefficients of variation, and interquartile ranges to determine whether the article count for a given newspaper is significantly low.

## Author

This project was created and maintained by **[Jacobo Blandón]**

- GitHub: [blandoncj](https://github.com/blandoncj)
- Email: [jacoboblandon94@gmail.com]

Feel free to reach out if you have any questions or suggestions for improvement!
    
