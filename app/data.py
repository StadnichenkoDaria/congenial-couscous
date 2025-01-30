from .models import User, Support

users_db = {
    1: User(
        id=1,
        email="george.bluth@reqres.in",
        first_name="George",
        last_name="Bluth",
        avatar="https://reqres.in/img/faces/1-image.jpg"
    ),
    2: User(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg"
    ),
    3: User(
        id=3,
        email="emma.wong@reqres.in",
        first_name="Emma",
        last_name="Wong",
        avatar="https://reqres.in/img/faces/3-image.jpg"
    ),
    4: User(
        id=4,
        email="eve.holt@reqres.in",
        first_name="Eve",
        last_name="Holt",
        avatar="https://reqres.in/img/faces/4-image.jpg"
    ),
    5: User(
        id=5,
        email="harles.morris@reqres.in",
        first_name="Charles",
        last_name="Morris",
        avatar="https://reqres.in/img/faces/5-image.jpg"
    ),
    6: User(
        id=6,
        email="tracey.ramos@reqres.in",
        first_name="Tracey",
        last_name="Ramos",
        avatar="https://reqres.in/img/faces/6-image.jpg"
    )
}

example_support = Support(
    url="https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
    text="Tired of writing endless social media content? Let Content Caddy generate it for you."
)
