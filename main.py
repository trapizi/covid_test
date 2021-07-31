from website import create_app
import data


app = create_app()

if __name__ == "__main__":
    #data.request_data()
    app.run(debug=True)