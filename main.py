# importação de pacote
from estudo import create_app

# chamando creat_app do init
app = create_app()

# ligando o servidor flaskn
if __name__ == '__main__':
    app.run(debug=True)
    