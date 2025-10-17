# **Scenarios**


## Scenario 1 - User Search
**Scenario name:** User Search in Aggregated Darkweb Data

**Goal:**  
Allow a logged-in user to search the indexed dark web data for specific keywords.  
The system returns matching results already collected by continuously running crawlers and processed by the analysis service.

**Involved services:**

- **Darknet-Browser** – handles user input and displays search results
- **Manager** – receives the query, queries the database, and returns matching entries
- **Crawler** – runs continuously, collecting new data from dark web sources
- **Data Analysis** – continuously processes and enriches crawled data (e.g., tagging, scoring)
    
**Happy path:**

1. The user logs in via Darknet-Browser (Supabase).
2. The user submits a search query through the Darknet-Browser.
3. The Manager queries the database for relevant analyzed data.
4. The Manager returns the results to the Darknet-Browser.
5. The Darknet-Browser displays the results on the Client.

**Error cases:**

1. `400 Bad Request` – invalid or missing query parameter.
2. `503 Service Unavailable` – Darknet-Browser cannot reach the Backend (Manager).
3. `429 Too Many Requests` – user exceeds search rate limit.


## Scenario 2 – Continuous Crawl & Analyse Process
**Scenario Name:** Continuous data collection and analysis workflow involving the Manager, Crawler, and Data Analysis services.

**Goal:**  
Enable an automated and continuous workflow for collecting, processing, and storing dark web data.
The Manager coordinates between the Crawler and the Data Analysis service to ensure that newly gathered data is enriched and stored for later search


**Involved Services:**

- **Manager** – Orchestrates the workflow, manages the database, initiates crawling and analysis jobs, and receives and stores results.
- **Crawler** – Collects raw data from specified dark web sources and sends it back to the Manager.
- **Data Analysis** – Processes, enriches, and categorizes crawled data (e.g., tagging, scoring, identifying entities).



**Happy Path:**

1. The Manager initiates a new crawling job by sending a request to the Crawler service.
2. The Crawler retrieves new data from defined dark web sources.
3. Once data collection is complete, the Crawler sends the raw data back to the Manager.
4. The Manager validates the received data and forwards it to the Data Analysis service, starting a new analysis job.
5. The Data Analysis service processes the data (e.g., enrichment, tagging, risk scoring) and returns the processed results to the Manager.
6. The Manager stores the final, enriched results in the Database for further use or visualization.
