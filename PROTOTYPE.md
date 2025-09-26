# Darkwebsearch Prototype

This is a fully functional prototype of the Darkwebsearch application as defined in the README.md. The prototype implements all four microservices with their specified functionality.

## 🏗️ Architecture

The application consists of four containerized microservices:

1. **SvelteKit GUI** (Port 3000) - Google-like search interface with Supabase authentication
2. **Manager** (Port 5000) - Orchestrates services, provides management dashboard
3. **Crawler** (Port 5001) - Web crawling with Selenium and rate limiting
4. **Data Analysis** (Port 5002) - AI-powered content analysis with sentiment and categorization

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- At least 4GB RAM available for containers

### Starting the Application

1. **Start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - **SvelteKit GUI**: http://localhost:3000 (Main search interface)
   - **Manager Dashboard**: http://localhost:5000 (Service management)
   - **Crawler API**: http://localhost:5001 (Crawling service)
   - **Analysis API**: http://localhost:5002 (Data analysis service)

### Initial Setup

1. Wait for all services to start (MySQL takes ~30 seconds to initialize)
2. Visit http://localhost:3000 to access the main search interface
3. Visit http://localhost:5000 for the management dashboard
4. Start a crawl from either interface to populate data

## 📋 Features Implemented

### ✅ SvelteKit GUI
- Google-like search interface
- Supabase authentication setup (configurable)
- Responsive design
- Real-time search with results display
- Integration with Manager service API

### ✅ Manager Service
- **REST API** for search queries and crawl management
- **Management Dashboard** with service status monitoring
- **Embedded Settings GUIs** for Crawler and Data Analysis
- **Database Management** with MySQL integration
- **Search Query Caching** for improved performance
- **Service Orchestration** between Crawler and Analysis services

### ✅ Crawler Service
- **Selenium-based crawling** with Chrome headless browser
- **Rate limiting** and **robots.txt respect** (configurable)
- **Link extraction** and **content processing**
- **Multi-threaded crawling** capability
- **Configurable settings** (rate limits, depth, user agent)
- **Background task processing**

### ✅ Data Analysis Service
- **Sentiment Analysis** using TextBlob
- **Content Categorization** with keyword matching
- **Keyword Extraction** using TF-IDF
- **Language Detection**
- **Batch Processing** capabilities
- **Analytics Dashboard** data

## 🗄️ Database Schema

The MySQL database includes tables for:
- `crawled_data` - Stores scraped content and metadata
- `analysis_results` - AI analysis results with tags and sentiment
- `search_queries` - Cached search queries for performance
- `crawler_settings` - Configurable crawler parameters
- `analysis_settings` - Configurable analysis parameters

## 🔧 Configuration

### Environment Variables

Each service can be configured via environment variables in `docker-compose.yml`:

**Database Configuration:**
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`

**Service URLs:**
- `CRAWLER_URL`, `ANALYSIS_URL`, `MANAGER_URL`

**Supabase (GUI):**
- `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY`

### Service Settings

- **Crawler Settings**: Accessible at http://localhost:5000/crawler-settings
- **Analysis Settings**: Accessible at http://localhost:5000/analysis-settings

## 📡 API Endpoints

### Manager Service (Port 5000)
- `POST /api/search` - Search crawled data
- `POST /api/crawl/start` - Start new crawl task
- `GET /api/crawler/status` - Check crawler service health
- `GET /api/analysis/status` - Check analysis service health
- `GET /api/recent-activity` - Get system activity log

### Crawler Service (Port 5001)
- `POST /crawl` - Start crawling task
- `GET /status` - Service health check
- `GET /tasks` - List all crawl tasks
- `GET /tasks/{id}` - Get specific task details

### Data Analysis Service (Port 5002)
- `POST /analyze` - Analyze single content item
- `POST /batch-analyze` - Batch analyze multiple items
- `GET /status` - Service health check
- `GET /analytics` - Get analysis statistics

## 🧪 Testing the Prototype

1. **Start the services** with `docker-compose up --build`
2. **Visit the GUI** at http://localhost:3000
3. **Enter a search query** (e.g., "technology", "security")
4. **Start a crawl** to populate data
5. **Check the Manager Dashboard** at http://localhost:5000
6. **Monitor crawl progress** and view results
7. **Explore analysis results** and categorization

## 🔒 Security Considerations

This is a **prototype** for demonstration purposes. For production use:

- Configure proper Supabase authentication
- Implement proper rate limiting and DDoS protection
- Use secure database credentials
- Add input validation and sanitization
- Implement proper error handling and logging
- Use HTTPS for all communications
- Add monitoring and alerting

## 🛠️ Development

### Adding New Features

1. **Crawler Extensions**: Modify `crawler/app.py` to add new crawling capabilities
2. **Analysis Algorithms**: Extend `data-analysis/app.py` for new analysis types
3. **GUI Components**: Add new Svelte components in `sveltekit-gui/src/`
4. **Database Schema**: Update `mysql-init/01-init.sql` for new tables

### Debugging

- **View Logs**: `docker-compose logs [service-name]`
- **Database Access**: Connect to MySQL on localhost:3306
- **Service Health**: Check `/status` endpoints on each service

## 📊 Performance Notes

- **Crawler**: Limited to 50 URLs per task to prevent resource exhaustion
- **Analysis**: Uses lightweight NLP models for fast processing
- **Database**: Indexed for common search patterns
- **Caching**: Search queries cached for 1 hour

## 🎯 Next Steps

For production deployment:

1. **Scale Services**: Use Kubernetes or Docker Swarm
2. **Database Clustering**: Implement MySQL cluster or migrate to PostgreSQL
3. **Message Queues**: Add Redis/RabbitMQ for task queuing
4. **Monitoring**: Implement Prometheus/Grafana stack
5. **CI/CD Pipeline**: Add automated testing and deployment
6. **Security Hardening**: Implement security best practices
7. **Documentation**: Add API documentation with OpenAPI/Swagger

---

**🎉 Congratulations!** You now have a fully functional darkweb search prototype with all the microservices defined in the README.md specification.