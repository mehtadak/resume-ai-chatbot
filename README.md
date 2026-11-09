## Technologies & Tools Used

We will be using the following tech stack when developing AI Agents this semester; importantly, we will not be providing lecture content to cover this tech stack directly. Rather, we assume that senior-level CS students are either already familiar with some (or all) of these tools, or will be able to pick up knowledge gaps through a combination of AI-assisted self-learning and review of code templates shared by the instructional team. For each of the tools used, we provide links to static resources students can use for learning (but note that AI tools are often as good, or better than the resources below).

| Category | Technology | Description | Learning Resources |
|----------|------------|-------------|-------------------|
| **Frontend** | [Vue.js 3](https://vuejs.org/) | Progressive JavaScript framework for building user interfaces | [Official Tutorial](https://vuejs.org/tutorial/), [Vue Mastery](https://www.vuemastery.com/) |
|  | [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework for rapid UI development | [Official Documentation](https://tailwindcss.com/docs), [Tailwind UI](https://tailwindui.com/) |
| **Backend** | [Flask](https://flask.palletsprojects.com/) | Lightweight Python web framework | [Official Tutorial](https://flask.palletsprojects.com/en/2.3.x/quickstart/), [Real Python Flask Guide](https://realpython.com/tutorials/flask/) |
|  | [PostgreSQL](https://www.postgresql.org/) | Advanced open-source relational database | [Official Tutorial](https://www.postgresql.org/docs/current/tutorial.html), [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) |
| **AI** | [OpenAI API](https://platform.openai.com/) | GPT models for natural language processing | [API Documentation](https://platform.openai.com/docs), [OpenAI Cookbook](https://github.com/openai/openai-cookbook) |
| **DevOps** | [Docker](https://www.docker.com/) | Containerization platform for consistent development environments | [Official Tutorial](https://docs.docker.com/get-started/), [Docker Hub](https://hub.docker.com/) |
| **Communication** | [Socket.IO](https://socket.io/) | Real-time bidirectional communication | [Official Documentation](https://socket.io/docs/v4/) |

**Why Are We Using This Tech Stack?** The combination of technologies shown in the table above represents a modern, industry-standard development stack. By learning these tools together in the context of AI Agents, you'll gain practical experience that you can immediately apply to other projects (personal, capstone, professional, etc.).


## Specific Homework Instructions


### Step 1: YouTube

1. Visit the course channel: https://www.youtube.com/@ghassemi

2. Subscribe to receive new lecture notifications, or you can just visit the [course calendar](https://docs.google.com/spreadsheets/d/14nQ43wy09sFn21ckNjBMyGT65enpqSLj73ezvqpVr78/edit?gid=475728874#gid=475728874) for links to lectures as they are released this semester.

   

1. Install Docker by visiting [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) and following the instructions for your operating system.

2. After you've installed, verify by running the following commands in your terminal:
   ```bash
   docker --version
   docker-compose --version
   ```

Make sure the docker desktop client is open on your machine.

### Step 4: OpenAI API

#### 4.1 Get OpenAI API Key

1. Sign up at [platform.openai.com](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create new secret key (save it securely!)
4. If you need help, see: [OpenAI API Key Setup Guide](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)



### Step 5: Environment Configuration

#### 5.1 Create Environment File

1. Navigate to your personal course repository (that's the one that matches your netID)
2. Create a `.env` file in the root directory of your project (e.g. by running the command `touch .env`)
3. Copy and paste the following configuration, being sure to replace the `<INSERT YOUR KEY HERE>` on line 2 with the API key you generated in step 4:

```env
# OpenAI Configuration
OPENAI_API_KEY=<INSERT YOUR KEY HERE>
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_CONVERSATION_HISTORY=1

# Database Configuration
DATABASE_NAME=db
DATABASE_HOST=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=iamsosecure
DATABASE_PORT=5432

# PostgreSQL Configuration
POSTGRES_VERSION=13
POSTGRES_PORT=5432

# Flask Configuration
SECRET_KEY=AKWNF1231082fksejfOSEHFOISEHF24142124124124124iesfhsoijsopdjf
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_PORT=8080
FLASK_HOST=0.0.0.0
SEND_FILE_MAX_AGE_DEFAULT=0

# Container Names
POSTGRES_CONTAINER=homework-postgres
FLASK_CONTAINER=homework-flask-app
DB_INIT_CONTAINER=homework-db-init

# System Configuration
TIMEZONE=America/New_York

# Development Settings
ENVIRONMENT=development

# Encryption Configuration
ENCRYPTION_ONEWAY_SALT = 'averysaltysailortookalongwalkoffashortbridge'
ENCRYPTION_ONEWAY_N = 32
ENCRYPTION_ONEWAY_R = 9
ENCRYPTION_ONEWAY_P = 1
ENCRYPTION_REVERSIBLE_KEY = '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='
```



### Step 6: Web App Deployment

#### 6.1 Deploy your web application locally

1. Navigate to the `homework 0` directory of your Personal Course Repository.

2. Use `docker-compose` to host the web application locally by executing the following command from a terminal:

   ```bash
   docker-compose up --build
   ```

   Open a new terminal window and run the following command to make sure the container was successfully created:

   ```bash
   docker ps
   ```
   
   You should see two containers: one for `homework-0-flask-app` and another for `postgres:13`
   
   

**FYI**: In this (or future) assignments, you may need to rebuild your application if you modify external dependencies (e.g., requirements.txt), environment variables (.env), or encounter persistent errors. Sometimes it's helpful to wipe existing images before rebuilding to ensure a clean state. To remove all docker-related images and containers, use:

```bash
docker rm -f -v $(docker ps -aq); docker rmi -f $(docker images -q); docker volume rm $(docker volume ls -q); docker network rm $(docker network ls -q)
```



#### 6.2 Access the local web application through the browser

You can view the deployed web application at the following address on your browser: [0.0.0.0:8080](http://0.0.0.0:8080). The web application I've provided includes several key features that you should test:

1. **Homepage**: Navigate to the homepage and verify it loads correctly
2. **Resume Page**: Navigate to the AI Agents tab, and click through to the AI resume.
3. **AI Chat**: Click the chat button on the right side and ask a question about the resume content
4. **Navigation**: Test moving between different pages to ensure navigation works