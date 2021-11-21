from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Everytime we change the python files, it'll rerun the webserver.