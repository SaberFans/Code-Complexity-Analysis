import requests
import json
from pygit2 import Repository
from pygit2 import discover_repository
from radon.visitors import ComplexityVisitor
import os
import shutil

# pull the repo
from git import Repo
current_working_directory = os.environ['repopath']
repo_url = os.getenv('repourl', 'https://github.com/faif/python-patterns.git')

if os.path.exists(current_working_directory):
	shutil.rmtree(current_working_directory)

Repo.clone_from(repo_url, current_working_directory)

repo = Repository(discover_repository(current_working_directory))

while(1):
	import time
	response = requests.get('http://manager:5000/steal')
	responobj = json.loads(response.text)
	if not responobj:
		print('no more commit to analyze, worker exits now!')
		break;
	else:
		'''
		extract the response payload like:
			{
				"cid": "commitid",
				"entries": [
					{
					"id", "entryid",
					"name": "entryname",
					""
					},
					{
						"id", "entryid2",
						"name": "entryname2",
						"type": "blob"
					}
				]
			}
		'''
		commitComplex = {}
		complexities = []
		commitComplex['cid'] = responobj['cid']
		commitComplex['complexities'] = complexities
		cComplex = 0
		for entry in responobj['entries']:
			sourceComplex = {}
			blob = repo[entry['id']]
			filename = entry['name']
			sourceComplex['name'] = filename
			sourceComplex['complex'] = []

			code = str(blob.data,'utf-8')
			try:
				v = ComplexityVisitor.from_code(code)
				complexsum = 0
				for func in v.functions:
					funcComplex = {}
					funcComplex['name'] = func.name
					funcComplex['lineno'] = func.lineno
					funcComplex['complexity'] = func.complexity
					complexsum = complexsum + func.complexity
					# append func complex
					sourceComplex['complex'].append(funcComplex)
				# accumulate the file complexity
				sourceComplex['complexval'] = complexsum
				# accumulate the commit complexity
				cComplex = cComplex + complexsum
				complexities.append(sourceComplex)
			except Exception:
				pass 
		commitComplex['cComplex']  = cComplex

		# submit following format of playload to manager server
		'''
		request data payload like:
			{
				"cid":"commit"
				"complexities":
				[
					{
						"name": "blobname",
						"complex": [],      # complexity deatil for each functions
						"complexval" : 1    # sum of complex of one source file
					}
				
				],
				"cComplex"
			}
		'''
		import sys
		cmitComplexPayload = json.dumps(commitComplex)
		requests.post('http://manager:5000/submit', data = cmitComplexPayload)

