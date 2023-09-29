from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)

class_active = "active"


class Database:
    @staticmethod
    def query(
        db: str, sql: str, args: tuple, many: bool = True
    ) -> list[tuple] or tuple:
        try:
            with sqlite3.connect(db) as connection:
                cursor = connection.cursor()
                cursor.execute(sql, args)
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
        except Exception as error:
            print(error)

    @staticmethod
    def select(
        db: str, table: str, columns: list[str], id: int = None
    ) -> list[tuple] or tuple:
        query = "SELECT {} FROM {}".format(", ".join(columns), table)
        if not id:
            return Database.query(db=db, sql=query, args=())
        return Database.query(
            sql=f"{query} WHERE id =?",
            args=(id,),
            many=False,
        )

    @staticmethod
    def insert(
        db: str, table: str, columns: list[str], values: list[any]
    ) -> list[tuple]:
        return Database.query(
            db=db,
            sql="INSERT INTO {} ({}) VALUES ({})".format(
                table, ", ".join(columns), ", ".join(["?" for _ in values])
            ),
            args=values,
        )


class Views:
    class Base:
        @staticmethod
        @app.route("/")
        def home():
            return render_template("home.html", page="home")

        @staticmethod
        @app.route("/vacancy")
        def vacancy():
            vacancies = Database.select(
                db="database/vacancies.db",
                table="vacancies",
                columns=[
                    "company",
                    "address",
                    "position",
                    "salary",
                    "experience",
                    "date",
                    "img",
                ],
            )
            return render_template("vacancy.html", page="vacancy", vacancies=vacancies)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)  # http://127.0.0.1:8000/
