from flask import Flask
from flask import request
from flask import jsonify
import os
from pygit2 import Repository
from pygit2 import discover_repository
from pygit2 import Tree
import json
import time
import sys
import shutil

commits = []

code_complexities= []
repo = None

app = Flask(__name__)

start_steal = None
end_steal = None
def setuprepo():
	# pull the repo
	from git import Repo
	current_working_directory = os.environ['repopath']
	repo_url = os.getenv('repourl', 'https://github.com/faif/python-patterns.git')
	if os.path.exists(current_working_directory):
		shutil.rmtree(current_working_directory)
	
	Repo.clone_from(repo_url, current_working_directory)

	# create different repo here
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
	global start_steal
	if not start_steal:
		# start count
		start_steal = time.time()
	entries = []
	if commits:
		# pop one commit off the list, hand it to worker
		commit = commits.pop()
		print('left commits to process'+str(len(commits)), file=sys.stdout)
		entrysearch(entries, commit, False)
		commitEntry = {}
		commitEntry['cid'] = str(commit.id)
		commitEntry['entries'] = entries
		return jsonify(commitEntry)
	else:
		# end of counting
		# stop the count once there's no more to steal
		global end_steal
		if not end_steal:
			end_steal = time.time()
		return jsonify({})


@app.route('/')
def getTime():
	if start_steal and end_steal:
		return str(end_steal-start_steal)
	else:
		return 'Not Finished'

@app.route('/num')
def getCommitNum():
	return str(len(commits))

if __name__ == "__main__":
	setuprepo()
	app.run(host="0.0.0.0", threaded=True, debug=True)