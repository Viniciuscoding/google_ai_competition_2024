frontend:
	cd transcribler-frontend && npm i && npm run dev

backend:
	cd transcribler-backend && flask --app app.py run

backend-v2:
	cd transcribler-backend-FastAPI && uvicorn main:app --reload