# API Communication Diagram

## Service Interactions

```
┌─────────────────┐
│     User        │
└────────┬────────┘
         │
         │ 1. Login/Register
         │ 2. Search Query
         ▼
┌─────────────────┐
│ Darknet Browser │ (SvelteKit + Supabase Auth)
│   (Frontend)    │
└────────┬────────┘
         │
         │ POST /api/search
         ▼
┌─────────────────┐
│    Manager      │ (Flask + MySQL)
│  (Orchestrator) │
└────┬───────┬────┘
     │       │
     │       │ POST /analyze
     │       │ (analysis job)
     │       ▼
     │   ┌──────────────┐
     │   │Data Analysis │ (Python + MySQL)
     │   │  (Analyzer)  │
     │   └──────┬───────┘
     │          │
     │          │ Returns:
     │          │ - Tags
     │          │ - Categories
     │          │ - Risk scores
     │          │ - Sentiment
     │          │ - Keywords
     │          │
     │ POST /crawl/start
     │ (crawl job)
     ▼
┌─────────────────┐
│    Crawler      │ (Flask + Selenium + MySQL)
│   (Scraper)     │
└────────┬────────┘
         │
         │ POST /crawl
         │ (crawled data)
         ▼
┌─────────────────┐
│    Manager      │
│  (Data Store)   │
└─────────────────┘
```

## Endpoint Flow

### 1. User Search Flow
```
User → Darknet Browser: Login (POST /api/auth/login)
Darknet Browser → Supabase: Authenticate
Supabase → Darknet Browser: JWT Token

User → Darknet Browser: Search (POST /api/search)
Darknet Browser → Manager: Search (POST /search) [with JWT]
Manager → Database: Query indexed data
Manager → Darknet Browser: Results
Darknet Browser → User: Display results
```

### 2. Continuous Crawl & Analysis Flow
```
Manager → Crawler: Start Crawl (POST /crawl/start)
Crawler → Dark Web Sites: Scrape content
Crawler → Manager: Submit Data (POST /crawl)
Manager → Database: Store raw data

Manager → Data Analysis: Analyze (POST /analyze)
Data Analysis → Process: Extract keywords, tags, sentiment
Data Analysis → Manager: Return Results (GET /analyze/results/{job_id})
Manager → Database: Update with analysis data
```

### 3. Settings Management Flow
```
Admin → Manager: Access Settings UI
Manager → Crawler: Get Settings (GET /settings)
Manager → Data Analysis: Get Settings (GET /settings)
Manager → Admin: Display Settings UI

Admin → Manager: Update Settings
Manager → Crawler: Update (PUT /settings)
Manager → Data Analysis: Update (PUT /settings)
```

## Authentication Flow

### Darknet Browser (Users)
- Uses Supabase JWT tokens
- Flow: Register → Login → Receive JWT → Use JWT for all API calls

### Internal Services (Manager, Crawler, Data Analysis)
- Use Bearer token authentication
- Services authenticate with each other using service-to-service JWT tokens

## Error Handling Scenarios

### Search Errors
- **400 Bad Request**: Invalid query parameter
- **401 Unauthorized**: Missing or invalid JWT token
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Manager or database unavailable

### Crawl Errors
- **400 Bad Request**: Invalid URL or parameters
- **404 Not Found**: Crawl job not found
- **503 Service Unavailable**: Crawler service down

### Analysis Errors
- **400 Bad Request**: Invalid data format
- **404 Not Found**: Analysis job not found
- **503 Service Unavailable**: Analysis service down

## Data Flow Schema

```
┌──────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐
│ Dark Web │ --> │ Crawler │ --> │ Manager  │ --> │ Storage │
│  Sites   │     │         │     │          │     │ (MySQL) │
└──────────┘     └─────────┘     └──────────┘     └─────────┘
                                       │
                                       v
                                  ┌──────────┐
                                  │  Data    │
                                  │ Analysis │
                                  └──────────┘
                                       │
                                       v
                                  ┌─────────┐
                                  │ Storage │
                                  │ (MySQL) │
                                  └─────────┘
                                       │
                                       v
                                  ┌─────────┐
                                  │ Darknet │
                                  │ Browser │
                                  └─────────┘
                                       │
                                       v
                                  ┌─────────┐
                                  │  User   │
                                  └─────────┘
```

## Key Features by Service

### Darknet Browser
- User authentication with Supabase
- Search interface
- Result pagination
- Search history
- Profile management

### Manager
- Central orchestration
- Search query handling
- Data storage coordination
- Service communication hub

### Crawler
- Selenium-based web scraping
- Rate limiting
- robots.txt compliance
- Configurable crawl depth
- Job queue management
- Health monitoring

### Data Analysis
- Keyword extraction
- Sentiment analysis
- Content classification
- Entity recognition (NER)
- Risk scoring
- Tag generation
- Health monitoring
