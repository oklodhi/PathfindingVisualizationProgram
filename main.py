from Website import create_app
from Website import templates

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)

