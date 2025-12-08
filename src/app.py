from app import create_app

app = create_app()
app.secret_key = "une_cle_super_secrete"

if __name__ == "__main__":
    app.run(debug=True)
