from flask import Flask
from github import Github
import sys, base64, json, yaml

app = Flask(__name__)

config = sys.argv[1]
cl = config.split("/")
g = Github()

@app.route("/")
def hello():
    return "Hello from dockerized flask app"
    
@app.route('/v1/<string:filename>')
def index(filename):
    split1 = filename.split(".")
    repo = g.get_user(cl[3]).get_repo(cl[4])
    branch = repo.get_branch("master")
    for tree in repo.get_git_tree(branch.commit.sha, False).tree:
        fname = repo.get_file_contents(tree.path).name
        split2 = fname.split(".")
        if split1[0] == split2[0] and split1[1] == "yml":
            return base64.b64decode(repo.get_file_contents(tree.path).content)
        elif split1[0] == split2[0] and split1[1] == "json":
            data = base64.b64decode(repo.get_file_contents(tree.path).content)
            return json.dumps(yaml.load(data), sort_keys=False, indent=2)
    return "No such file found"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')