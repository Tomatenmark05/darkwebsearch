# Crawler
This is the crawler service of the dark web search project.
It utilizes a three container setup consisting of a FastAPI, Svelte and Tor container. The Tor container acts as a proxy for the crawling requests to enable access to .onion services. 

At this stage the FastAPI container offers 1 endpoint: 
 - POST /crawl
 - GET /status/{job_id}
 - GET /status -> gets the status of all stored jobs

The GUI has not been implemented yet, because it only provides configuration settings and is not needed yet for basic functionallity.

To start the service just use the `docker-compose.yaml` file inside the `/crawler/` directory.
For analysis connection the manager service is also required to run. If the manager service is not ran and one wants to verify the results of the crawl other by using the `/status/{job_id}` endpoint just run `docker logs crawler` and the content of a crawled website will be printed somewhere.

For a simple test case try the .onion address of DuckDuckGo: `https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/`.

> If something doesn't work at first try, wait till the status of the tor container is marked as `unhealthy`. This is because the maintainer of the docker image implemented a flawed health check