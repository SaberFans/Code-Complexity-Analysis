### Prerequisites
 * Docker Toolset
 * Python Dev 3.6+
 
### How to Run:
`docker-compose up`

### Explaination:
As the worker and manager module make use of pygit2 library,
so the installation process is defined in the Dockerfile

### Process of Complexity calculation:

1. Work-stealing pattern is used

2. Managers hosting commits info

3. Worker steal commits and work on it

4. Worker push back result to Manager node

### Result

The result is documented in RESULT and graphs are generated as Figure_1 and Figure_2

From the graph, you can see when more workers are involved in computing, it will be more efficient.
But as each worker will clone the entire repo from github, more containers more time it will consume for 
pulling down the docker.

Ideally, the repo should be downloaded beforehand for each of the work to work on without cloning, 
but to ease the build process, more feasible approach is chosen.



