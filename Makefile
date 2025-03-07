frontend:
	cd transcribler-frontend && npm i && npm run dev

backend:
	cd transcribler-backend && flask --app app.py run
