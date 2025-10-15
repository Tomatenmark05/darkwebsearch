# Darkwebsearch API Interfaces - Summary

## Overview
This directory contains complete OpenAPI 3.0.3 specifications for all four microservices in the Darkwebsearch platform.

## Files

| File | Service | Endpoints | Description |
|------|---------|-----------|-------------|
| `openapi-manager.yaml` | Manager | 2 | Orchestrates services and handles searches |
| `openapi-crawler.yaml` | Crawler | 6 | Scrapes dark web sites with Selenium |
| `openapi-data-analysis.yaml` | Data Analysis | 6 | Analyzes data and generates tags |
| `openapi-darknet-browser.yaml` | Darknet Browser | 7 | Frontend GUI with Supabase auth |
| `README.md` | Documentation | - | Comprehensive interface documentation |
| `API_DIAGRAM.md` | Documentation | - | Service interaction flows and diagrams |

## Quick Stats

- **Total Services**: 4
- **Total Endpoints**: 23
- **Authentication Methods**: 2 (JWT Bearer, Supabase JWT)
- **Tech Stack**: Python (Flask), SvelteKit, Selenium, MySQL, Supabase

## Service Owners

| Service | Owner | Tech Stack |
|---------|-------|------------|
| Manager | Mark Sperle | Python (Flask), MySQL |
| Crawler | Lukas Troedsson | Python (Flask), Selenium, MySQL |
| Data Analysis | Johannes Wutte | Python, MySQL |
| Darknet Browser | Huber Elena | SvelteKit, Supabase Auth |

## Key Features

### Manager
- Search query handling
- Service orchestration
- Data storage coordination

### Crawler
- JavaScript rendering with Selenium
- Rate limiting
- robots.txt compliance
- Configurable crawl depth
- Job queue management

### Data Analysis
- Keyword extraction
- Sentiment analysis
- Content classification
- Entity recognition
- Risk scoring
- Tag generation

### Darknet Browser
- User authentication
- Search interface with filters
- Search history
- Profile management
- Rate limiting

## API Standards

All APIs follow these standards:
- OpenAPI 3.0.3 specification
- RFC 7807 Problem Details for errors
- ISO 8601 for timestamps
- JWT Bearer authentication
- RESTful design principles
- Health check endpoints

## Usage

To view these specifications:
1. Use [Swagger Editor](https://editor.swagger.io/)
2. Import the YAML files
3. Explore endpoints and schemas

To implement:
1. Generate server stubs using OpenAPI Generator
2. Implement business logic
3. Add database integration
4. Deploy with Docker

## Integration Flow

```
User → Darknet Browser → Manager → Crawler/Data Analysis → Database → Results
```

## Next Steps

1. Implement server stubs from OpenAPI specs
2. Set up database schemas
3. Implement authentication
4. Add logging and monitoring
5. Deploy to production environment
6. Add API versioning
7. Create API documentation portal

## Notes

- All services use MySQL databases
- Authentication is required for all endpoints (except health checks and registration)
- Services should implement retry logic and circuit breakers
- Rate limiting should be enforced at the API gateway level
- All services should log requests and errors

## Support

For questions or issues with these interfaces:
1. Check the README.md for detailed documentation
2. Review API_DIAGRAM.md for service flows
3. Contact the respective service owner
4. Create an issue in the repository
