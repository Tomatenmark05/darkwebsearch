### **Scenario Scope**

**Scenario name:** User Search in Aggregated Darkweb Data

**Goal:**  
Allow a logged-in user to search the indexed dark web data for specific keywords.  
The system returns matching results already collected by continuously running crawlers and processed by the analysis service.

**Involved services:**

- **SvelteKit GUI** – handles user input and displays search results
- **Manager** – receives the query, queries the database, and returns matching entries
- **Crawler** – runs continuously, collecting new data from dark web sources
- **Data Analysis** – continuously processes and enriches crawled data (e.g., tagging, scoring)
    
**Happy path:**

1. The user logs in via Supabase.
2. The user submits a search query through the GUI.
3. The Manager queries the database for relevant analyzed data.
4. The Manager returns the results to the GUI.

**Error cases:**

1. `400 Bad Request` – invalid or missing query parameter.
2. `503 Service Unavailable` – Manager cannot reach the database or analysis service.
3. `429 Too Many Requests` – user exceeds search rate limit. 