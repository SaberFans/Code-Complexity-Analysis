from flask import Flask
from flask import request
from flask import jsonify
import os
from pygit2 import Repository
from pygit2 import discover_repository
from pygit2 import Tree
import json

commits = []
code_complexities= []
repo = None

app = Flask(__name__)

def setuprepo():
	# pull the repo
	from pygit2 import clone_repository
	repo_url = os.getenv('repourl','https://github.com/libgit2/pygit2.git')
	repo_path = os.getenv('repopath','/tmp/coplexity/repo')

	if not os.path.exists(repo_path):
		os.makedirs(repo_path)

	# for some reason this isn't working
	# repo = clone_repository('https://github.com/libgit2/pygit2.git', '/path/to/create/repository')
	current_working_directory = '/repo/test'
	global repo
	repo = Repository(discover_repository(current_working_directory))

	from pygit2 import GIT_SORT_REVERSE
	global commits
	for commit in repo.walk(repo.head.target, GIT_SORT_REVERSE):
		commits.append(commit)

# submit aggregate all the complexity details
@app.route('/submit', methods=['GET', 'POST']) 
def submit():
	complexity = json.loads(request.data)
	global code_complexities
	code_complexities.append(complexity)
	print('=========')
	print(complexity)
	print('=========')    
	return 'OK, 200'
# submit aggregate all the complexity details
@app.route('/show')
def show():
	return jsonify(code_complexities)

def entrysearch(entries, commit, isTree):
	if not isTree:
		tree = commit.tree
	else:
		tree = commit
	for entry in tree:
		if str(entry.type)  != "tree":
			# append only .py files
			if str(entry.name).endswith(".py"):
				entries.append({'id':str(entry.id), 'name':str(entry.name), 'type': str(entry.type)})
		else:
			entry = repo.get(entry.oid)
			entrysearch(entries, entry, True)

@app.route('/steal') 
def steal():
	entries = []
	if commits:
		# pop one commit off the list, hand it to worker
		commit = commits.pop()
		entrysearch(entries, commit, False)
		commitEntry = {}
		commitEntry['cid'] = str(commit.id)
		commitEntry['entries'] = entries
		return jsonify(commitEntry)
	else:
		return jsonify({})

@app.route('/')
def hello():
	return 'Hello World!\n'

if __name__ == "__main__":
	setuprepo()
	app.run(host="0.0.0.0", threaded=True, debug=True)