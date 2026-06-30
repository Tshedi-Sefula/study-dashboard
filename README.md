# study-dashboard
--------------------------
A production-inspired full-stack Study Activity Dashboard that enables learning officers to monitor student engagement, quiz performance, and study activity. Built with FastAPI, PostgreSQL, React, TypeScript, and Tailwind CSS. Developed as part of the Bag Learning Software Development Internship technical assessment.
 

## Database Setup and Seed

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Add your `.env` file (see `.env.example`)

3. Run migrations and seed:
```bash
   supabase db push && cd backend && python3 -m seed && cd ..
```
