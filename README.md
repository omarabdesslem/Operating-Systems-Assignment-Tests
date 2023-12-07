## Operating Systems Assignments Testing

### Project Description
This repository is intended to be used in the context of the computer applications course Project (15): Helping students better understand the expectations of a lab assignment.

### Usage
Python tests for Operating Systems labs:
The automated tests for the hash (TP2) and client-server (TP5) practical assignments will verify if the created programs function according to the specified requirements, by testing various functionalities.

### Usage Explanation
Hash:

```
./path_to/test.py /path_to/program -optional_arguments
```

Client-Server example:

```
./test.py ./TP-Correct/server 50000 [1,-1,0,2] 3
./test.py ./TP-Correct/client 50000 [1,-1,0,2] 3 -c
```

### Project Status
Completed
