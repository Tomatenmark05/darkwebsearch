

**Functions:**

- Secure authentication via Supabase
- Containerised with docker
- Interface between user and other microservices
- Fallback system (provides default examples if the manager is unavailable)
- Logs describing the current status


**Starting the microservice:**

- Starting the microservice (docker-compose up --build).
- Afterwards, you can access the website http://localhost:3000 (or use the respective ip if it's not running locally).
- The user logs in with their Supabase account (test user: elena.huber14@gmail.com, Paw0rd).
- After successful authentication, you will be taken to the GUI interface where you can start a search. If Manager is running, you will receive the respective results. If Manager is not available, you will receive 5 defined default values.
- The user can then log out using the LOGOUT button.
- Shut down the microservice afterwards (docker-compose down).


**Logs:**

Die Anwendung schreibt detaillierte Logs direkt in die Docker-Container-Ausgabe. Diese sind in Echtzeit über das Terminal einsehbar (docker logs -f darknet-gui). Example:

darknet-gui    | ========================================
darknet-gui    | === DEBUG: Vorbereitung für Manager Request ===
darknet-gui    | Search query: vpn
darknet-gui    | User: elena.huber14@gmail.com (ID: 1721695e-9c49-4bfd-90c4-5d1d58944c6f)
darknet-gui    | Manager URL: http://manager:8000
darknet-gui    | === DEBUG: Sende Request an Manager ===
darknet-gui    | URL: http://manager:8000/search
darknet-gui    | Method: POST
darknet-gui    | Headers: Content-Type: application/json, Accept: application/json
darknet-gui    | Body: {
darknet-gui    |   "query": "vpn",
darknet-gui    |   "user": {
darknet-gui    |     "id": "1721695e-9c49-4bfd-90c4-5d1d58944c6f",
darknet-gui    |     "email": "elena.huber14@gmail.com"
darknet-gui    |   }
darknet-gui    | }
darknet-gui    | ========================================
darknet-gui    | === DEBUG: Response vom Manager ===
darknet-gui    | Status: 200 OK
darknet-gui    | Response Data: []...
darknet-gui    | ========================================


**Tests:**