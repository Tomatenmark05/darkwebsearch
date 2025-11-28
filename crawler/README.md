# Crawler
This is the crawler service of the dark web search project.
It utilizes a three container setup consisting of a FastAPI, Svelte and Tor container. The Tor container acts as a proxy for the crawling requests to enable access to .onion services. 

At this stage the FastAPI container offers 1 endpoint: 
 - POST /crawl
 - GET /status/{job_id}
 - GET /status -> gets the status of all stored jobs

The GUI has not been implemented yet, because it only provides configuration settings and is not needed yet for basic functionallity.