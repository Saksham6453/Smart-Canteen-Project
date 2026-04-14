# Smart-Canteen-Project
Academic Year 2025-2026 | K.R. Mangalam University 

📝 Project Overview
The Smart Canteen Pre-Order System is a digital solution designed to modernize the traditional college canteen experience at K.R. Mangalam University. Currently, students face long queues and significant time wastage during peak hours. This system allows students to browse the menu and place orders digitally from their classrooms, eliminating wait times and ensuring food availability. 

🚀 Key Features

Student Interface: Secure login using college credentials, menu browsing with emojis and descriptions, and real-time order tracking. 


Staff Interface: Centralized dashboard to view incoming orders, update order status (Pending → Preparing → Ready), and manage daily statistics. 


Real-Time Updates: Instant communication between students and canteen staff via a cloud-based database. 

🛠️ Tech Stack

Backend: Python (Flask Framework) 


Database: Vercel Postgres (Production) / SQLite (Local Development) 


Frontend: HTML5, CSS3 (Modern Glassmorphism UI), and Jinja2 Templates 


Deployment: Vercel Cloud Platform 

📂 Project Structure
Plaintext
canteen-project/
├── app.py              # Main Flask application & Database logic
├── requirements.txt    # Python dependencies for Vercel
├── vercel.json         # Vercel configuration for Python
├── static/
│   └── style.css       # Custom UI styling & animations
└── templates/          # HTML views
    ├── login.html      # Authentication page
    ├── menu.html       # Student menu browsing
    ├── cart.html       # Order summary and checkout
    ├── orders.html     # Student order history and status
    └── admin.html      # Staff order management dashboard
⚙️ How to Run Locally
Clone the project to your local machine.

Install dependencies:

Bash
pip install flask
Run the application:

Bash
python app.py
Access the app: Open http://127.0.0.1:5000 in your browser.

👥 Project Team

Grantik Sahni (Roll No: 2501201031) 


Nakul Kumar (Roll No: 2501201006) 


Tanishq Bhardwaj (Roll No: 2501201004) 


Tanvi (Roll No: 2501060072) 


Lakshay Aggarwal (Roll No: 2501201036) 


Sahana Dhingra (Roll No: 2501201039) 

Developed with ❤️ for K.R. Mangalam University.
