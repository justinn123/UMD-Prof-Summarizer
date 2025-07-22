# UMD Professor Summarizer
Planet Twerp is a web application that summarizes and provides insight about professors at the University of Maryland. It is built with Flask, LangChain, Tailwind, and Planet Terp data. The application currently uses Groq to run language models due to its free access, but it can easily be configured to work with other LLM providers such as OpenAI.

## Project Status
The Planet Twerp currently supports querying insights for individual professors. The next steps include refining the query functionality to allow users to specify whether they want insights on all courses taught by a professor or only a selected subset. Future improvements will include adding functionality to identify and analyze professors who teach similar courses, as well as providing side-by-side comparisons between professors and the courses they teach.

## Screenshots
<img width="1917" height="899" alt="Image" src="https://github.com/user-attachments/assets/deda871c-788a-4625-8008-12e1f2080ba6" />

<img width="598" height="293" alt="Image" src="https://github.com/user-attachments/assets/a1f4134e-34e3-49ad-a76a-55c53b1ea087" />

<img width="602" height="342" alt="Image" src="https://github.com/user-attachments/assets/025c5eda-5ca3-4a57-a0af-ac6e94847180" />

## Installation and Setup

### Clone Git Repo
First clone the GitHub repo and create Docker image.
```
$ git clone https://github.com/justinn123/UMD-Prof-Summarizer.git
$ docker build -t your-image-name
```

### Create .env file
You need to create a .env file to store the secret key for the Flask app, the Groq API key for langchain, and a redis url for caching data.\
To generate secret key:

```
$ python
>>> import os
>>> os.urandom(12).hex()
```
To get Groq API key, go to https://console.groq.com/keys\
To setup Redis with Upstash, follow instructions here: https://console.upstash.com/redis 

After getting the required keys, add to your .env file:
```shell
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
REDIS_URL="your_redis_url"
```
### Run the container
Create a container from the image you built earlier
```
$ docker run -p 5000:5000 your-image-name
```
Then go to: http://localhost:5000
