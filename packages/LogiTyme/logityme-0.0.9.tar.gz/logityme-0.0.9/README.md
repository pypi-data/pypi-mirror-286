<h1 align="center">LogiTyme</h1>
<p align="center">A Python handler for <a href="https://github.com/lmas3009/LogiTyme"><i>logityme</i></a>.</p>

[//]: # ([![python compatibility]&#40;https://github.com/lmas3009/LogiTyme/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions/badge.svg&#41;]&#40;https://github.com/lmas3009/LogiTyme/actions/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions.yml&#41;)
[![python version](https://img.shields.io/badge/Works_With_Python-3.8,%203.9,%203.10,%203.11-orange)](https://github.com/lmas3009/LogiTyme/actions/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions.yml)

---

LogiTyme is a Python package used to track the time spent on each function, custom functions, and the entire Python Program

- Python package repo link: https://pypi.org/project/LogiTyme/


# *Installation Process*:
1. Install LogiTyme via pip:
To install the LogiTyme package, use the following pip command
    ```bash
    pip install LogiTyme
    ```
3. Verifify the Installation:
After installation, you can verify it by importing LogiTyme in a python script
    ```bash
    import LogiTyme
    print(LogiTyme.__version__)
    ```


# *Usage*

Simple example on how to use LogiTyme in Cloud Provider:

Checkout the expected output: https://github.com/lmas3009/LogiTyme/blob/main/example/testing-cloud.md

```bash
from LogiTyme import LogiTymeCloud
logityme = LogiTymeCloud(maxTime=5)
logityme.StartReport()

@logityme.smart_threshold_check(maxTimeLimit=3)
def slow_function(n):
  result = 0
  for i in range(n):
    for j in range(n):
      result += i*j
      print(result)

  return result

for i in range(10):
  for j in range(10):
    print(i*j)

def slow_function2(n):
  result = 0
  for i in range(n):
    for j in range(n):
      result += i*j
      print(result)

  return result

slow_function(20)
slow_function2(20)

logityme.GenerateReport()
```

Simple example on how to use LogiTyme in local:
```bash
from LogiTyme import LogiTyme

logityme = LogiTyme(maxTime=5)

logityme.StartReport()

@logityme.smart_threshold_check(maxTimeLimit=3)
def slow_function(n):
  result = 0
  for i in range(n):
    for j in range(n):
      result += i*j
      print(result)

  return result

@logityme.smart_threshold_check(maxTimeLimit=2)
def slow_function2(n):
  result = 0
  for i in range(n):
    for j in range(n):
      result += i*j
      print(result)

  return result

slow_function(20)
slow_function2(20)

logityme.LogiFuncStart(name="for-loop", maxLimit=3)
re = 0
for i in range(500):
  for j in range(500):
    re += i * j
    print(re)
logityme.LogiFuncEnd()

logityme.GenerateReport()
```

**_Resulted Output while running in local:_**
```text

Performance Analysis

1. Introduction:
	This report presents the findings of a performance analysis conducted on the Python program 'test.py'. The purpose of the analysis is to provide insights into the time consumed by the program and offer recommendations for optimizing its performance.

2. Methodolgy:
	The program was profiled using the cProfile module to collect data on execution time. The collected data was analyzed to identify the functions consuming the most time.

3. Results:
	- Started the program at: 2024-07-17 17:38:14.340244
	- Ended the program at: 2024-07-17 17:38:19.493889
	- Total Execution Time: 5.152 seconds
	- As you defined the threshold limit as 5 mins, Since this script took Less then your threshold limit, you are good to go...
	- memory consumed: 0.0234MB

4. Functions Results:
+----------------+---------------+-----------------------------+
| Function Name  | Time Consumed | Maximum Threshold Limit Set |
+----------------+---------------+-----------------------------+
| slow_function  | 0.004 secs    | 180 secs                    |
| slow_function2 | 0.004 secs    | 120 secs                    |
| for-loop       | 4.549 secs    | 180 secs                    |
+----------------+---------------+-----------------------------+

5. inBuilt-functions Time-Consumed Report:
+----------------------------------+---------------+
| Function Name                    | Time Consumed |
+----------------------------------+---------------+
| <built-in method builtins.print> | 4.556 secs    |
+----------------------------------+---------------+

6. Environment Suggestions:
	- Short tasks (less than 5 minutes):
		-- GCP (Cloud Functions, Compute Engine, GKE, Cloud Run) or AWS (Lambda, EC2, ECS, Step Function, Glue): 
			 Both are well-suited for tasks that complete quickly.
		-- Azure Functions (Consumption Plan, VM, AKS, Container Instances):
			 Good choice for short tasks

7. Code Optimization:
+----------------+---------------+-----------------------------+
| Function Name  | Time Consumed | Maximum Threshold Limit Set |
+----------------+---------------+-----------------------------+
| slow_function  | 0.004 secs    | 180 secs                    |
| slow_function2 | 0.004 secs    | 120 secs                    |
| for-loop       | 4.549 secs    | 180 secs                    |
+----------------+---------------+-----------------------------+
Since this function "slow_function" took 0.004 secs is less then 180 seconds (i.e < 3 mins). The function is quite optimized.
Since this function "slow_function2" took 0.004 secs is less then 120 seconds (i.e < 2 mins). The function is quite optimized. 
Since this function "for-loop" took 4.549 secs is less then 180 seconds (i.e < 3 mins). The function is quite optimized.

8. Conclusion:
	The analysis revealed areas for potential optimization in the Python program 'test.py'. By implementing the recommendations outlined in this report, the program's performance can be improved, leading to better overall efficency.
```


# _Release Version_

- **```0.0.9```**
  - Introducing **LogiTymeCloud**
    - This is to track time spent by a program while running in any cloud provider. For example check out: https://github.com/lmas3009/LogiTyme/blob/main/example/testing-cloud.py
    - In LogiTymeCloud you can't calculate time spent by, any loops, api-calls, etc..
  - Decommission
    - We removed **_env_** from **LogiTyme(env="local",maxTime=5)**, now it will be **LogiTyme(maxTime=5)** or **LogiTymeCloud(maxTime=10)**
  - Resolved Minor Bugs while Generating Report.
    


- **```0.0.7 / 0.0.8```**
  - Introducing maxTime on LogiTyme
    - **LogiTyme(env="local",maxTime=5)** _used to set the time limt for entire python program. This is for set the threshold limit._
  - Introducing decorators
    - **@logityme.smart_threshold_check(maxTimeLimit=2)** _used to set the time limt for a function. If the limit crossed, It will suggest you for a optimization._
  - Introducing maxLimit on LogiFuncStart
    - **logityme.LogiFuncStart(name="for-loop", maxLimit=3)** _used to keep track of the threshold limit, if it cross the limit, It will suggest you for a optimization._
  

- **```0.0.2 / 0.0.3 / 0.0.4 / 0.0.5 / 0.0.6```**
  - Launching LogiTyme
    - Functions Included:
      - **StartReport:** _used to start the process of logging the time for you python program._
      - **GenerateReport:**  _used to end the logging process and generate a report based on each function used in the code.
        Now this will start process the logged data and generate a report based on the time spent in each function used in your code.
        The generated report will provide insights into the performance if different functions_
        - env  To run the code in local machine or in cloud machine
        - env = "local" / "cloud" 
      - **LogiFuncStart & LogiFuncEnd:** _used to log time for custom code._


# *Creator Information*:
- Created By: Aravind Kumar Vemula
- Twitter: https://x.com/AravindKumarV09
- Github: https://github.com/lmas3009

