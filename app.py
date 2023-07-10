"""The app module."""

from dataclasses import dataclass

from flask import Flask, render_template, url_for  # pylint: disable=unused-import

app = Flask(__name__)


@dataclass
class Shloka:
    """A Shloka."""

    pada1: str
    pada2: str
    pada3: str
    pada4: str
    idx: int | str

    def __post_init__(self):
        if isinstance(self.idx, int):
            self.idx = str(self.idx)

    def text(self) -> str:
        return f"{self.pada1}<br>{self.pada2}।<br>{self.pada3}\n<br>{self.pada4}॥{self.idx}॥"


shloka = Shloka(
    "अपि कुशलममर्त्याः स्वागतं सांप्रतं वः",
    "शमितदनुजदम्भा किं नु दम्भोलिकेलिः",
    "अपि धिषणमनीषानिर्मिता नीतिमार्गा-",
    "स्त्रिदशनगरयोगक्षेमकृत्ये क्षमन्ते",
    "१७",
)


@app.route("/")
@app.route("/home")
def home():
    return render_template("bhashya.html", shloka=shloka.text())


@app.route("/bhashya")
def bhasya():
    return render_template("bhashya.html", shloka=shloka.text())


if __name__ == "__main__":
    app.run(debug=True)
