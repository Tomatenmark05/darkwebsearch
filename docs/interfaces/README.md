# Microservices API Interfaces

This directory contains OpenAPI 3.0.3 specifications for all microservices in the Darkwebsearch platform.

## Overview

The Darkwebsearch platform consists of four microservices, each with its own API:

1. **Manager** - Orchestrates the system and handles search queries
2. **Crawler** - Scrapes data from dark web sites
3. **Data Analysis** - Analyzes crawled data and generates tags
4. **Darknet Browser** - Frontend GUI with Supabase authentication

## API Specifications

### Manager API (`openapi-manager.yaml`)
**Owner:** Mark Sperle  
**Tech Stack:** Python (Flask), MySQL

The Manager service orchestrates the entire system:
- **POST /search** - Handles search queries from the frontend
- **POST /crawl** - Receives crawled data from the Crawler service

### Crawler API (`openapi-crawler.yaml`)
**Owner:** Lukas Troedsson  
**Tech Stack:** Python (Flask), Selenium, MySQL

The Crawler service scrapes dark web sites:
- **POST /crawl/start** - Start a new crawl job
- **GET /crawl/status/{job_id}** - Check status of a crawl job
- **POST /crawl/stop/{job_id}** - Stop a running crawl job
- **GET /settings** - Get crawler settings
- **PUT /settings** - Update crawler settings
- **GET /health** - Health check endpoint

Features:
- Rate limiting support
- Respects robots.txt and sitemaps
- JavaScript rendering with Selenium
- Configurable crawl depth and concurrency
- Optional multithreading

### Data Analysis API (`openapi-data-analysis.yaml`)
**Owner:** Johannes Wutte  
**Tech Stack:** Python, MySQL

The Data Analysis service processes crawled data:
- **POST /analyze** - Submit data for analysis
- **GET /analyze/status/{job_id}** - Check status of an analysis job
- **GET /analyze/results/{job_id}** - Get analysis results
- **GET /settings** - Get analysis settings
- **PUT /settings** - Update analysis settings
- **GET /health** - Health check endpoint

Analysis capabilities:
- Keyword extraction
- Sentiment analysis
- Content classification
- Entity extraction (PERSON, ORGANIZATION, LOCATION, etc.)
- Risk scoring
- Tag generation
- Optional multithreading

### Darknet Browser API (`openapi-darknet-browser.yaml`)
**Owner:** Huber Elena  
**Tech Stack:** SvelteKit, Supabase Auth

The frontend GUI service:
- **POST /api/search** - Perform search queries (proxies to Manager)
- **GET /api/search/history** - Get user's search history
- **POST /api/auth/login** - User login with Supabase
- **POST /api/auth/logout** - User logout
- **POST /api/auth/register** - User registration
- **POST /api/auth/refresh** - Refresh access token
- **GET /api/user/profile** - Get user profile

Features:
- Supabase JWT authentication
- Search filters (tags, date range, risk score)
- Pagination support
- Rate limiting (429 error)
- Search history tracking

## Service Communication Flow

### Search Flow
```
User → Darknet Browser → Manager → [returns results]
```

### Crawl & Analysis Flow
```
Manager → Crawler → [crawls data] → Manager → Data Analysis → [returns tags] → Manager
```

## Authentication

- **Manager, Crawler, Data Analysis**: Use JWT Bearer token authentication
- **Darknet Browser**: Uses Supabase JWT authentication for users

## Error Handling

All services follow RFC 7807 Problem Details for HTTP APIs:
- **400 Bad Request** - Invalid or missing parameters
- **401 Unauthorized** - Authentication required/failed
- **404 Not Found** - Resource not found
- **429 Too Many Requests** - Rate limit exceeded
- **503 Service Unavailable** - Service or database unavailable

## Development

To view and edit these OpenAPI specifications, you can use:
- [Swagger Editor](https://editor.swagger.io/)
- [Stoplight Studio](https://stoplight.io/studio)
- VS Code with OpenAPI extension

## Implementation Notes

1. All services should implement health check endpoints for monitoring
2. Services should respect rate limiting to prevent abuse
3. All timestamps should use ISO 8601 format
4. Authentication tokens should be passed in the Authorization header
5. Services should log all requests and errors for debugging
6. Database connections should include retry logic and connection pooling
