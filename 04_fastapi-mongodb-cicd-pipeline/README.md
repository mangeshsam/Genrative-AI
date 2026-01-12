##  Live Deployment

This FastAPI application is successfully deployed on **Render**.

 **Live API URL:**  
https://genrative-ai.onrender.com/docs

---

##  API Endpoints

| Method | Endpoint | Description |
|------|--------|-------------|
| GET | `/` | Health check – verify API is running |
| GET | `/Extract_data/getdata` | Fetch data from MongoDB Atlas |

---

##  Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MongoDB Atlas
- **Async Driver:** Motor
- **Deployment:** Render
- **Version Control:** GitHub

---

##  Deployment Details

- The application is deployed using Render's web service.
- Environment variables are securely managed via Render.
- On each code update, Render automatically rebuilds and redeploys the application.
