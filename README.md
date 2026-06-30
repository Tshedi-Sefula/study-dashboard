# study-dashboard
--------------------------
A production-inspired full-stack Study Activity Dashboard that enables learning officers to monitor student engagement, quiz performance, and study activity. Built with FastAPI, PostgreSQL, React, TypeScript, and Tailwind CSS. Developed as part of the Bag Learning Software Development Internship technical assessment.
 

Setting up the Virtual Environment:

1.) in the root of the repo run the following commands
    python3 venv .venv

2.) Activate the environment
    source .venv/bin/activate

3.) Install the dependencies
    python3 -m pip install fastapi uvicorn
    python3 -m pip freeze > requirements.txt

How to populate the db:

## Setup

1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]:5432/postgres

3. Run migrations and seed the database:
```bash
   supabase db push && python3 backend/seed.py
```
