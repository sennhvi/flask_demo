# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    mydict = {"a":123, "b":456, "c":789, "key":"value"}
    mylist = list("abcdefg")
    myintvar = 5
    mystr = '<h1>safe过滤器测试</h1>'

    class MyClass:
        def __init__(self, integer):
            self.integer = integer

        def somemethod(self):
            return self.integer

    myobj = MyClass(name)
    return render_template("user.html", name=name, mydict=mydict, mylist=mylist, myintvar=myintvar, myobj=myobj, mystr=mystr)

@app.route("/tempo/")
def tempo():
    return render_template("template_demo.html")

@app.route("/bootstrap_tempo/<name>")
def bootstrap_tempo(name):
    return render_template("bootstrap_demo.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)