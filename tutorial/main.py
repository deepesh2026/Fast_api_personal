import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0",port=8000, reload=True)


    # .run means running a webserver. the term "app.app:app" means that we are running the app object from the app.py file which is inside the app folder. The host is set to "0.0.0.0" so that the server is accessible from any IP address, and the port is set to 8080. The reload=True flag enables auto-reloading when code changes are detected.