from flask import Flask
from flask import render_template

app = Flask(__name__)

dummyData = [
    {
        "f_name": "Robert",
        "l_name": "Siberry",
        "title": "Dr",
        "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
    },
    {
        "f_name": "Pete",
        "l_name": "Repeat",
        "title": "Mr",
        "content": "Pete and Repeat are on a boat Pete fell out who was left?"
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', title='Homepage', posts=dummyData)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run()