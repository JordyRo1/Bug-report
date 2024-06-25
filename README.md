# Bug report
 
## Configuration

 - Starknet-py: 0.21.0
 - Dojo: 0.7.0-alpha.2

 ## Steps to reproduce

 - Install the dependancies: 
  ```bash
  poetry install 
  ```
 - Run a katana instance. From there, retrieve the prefunded account configuration to replace it in the `test_contract.py` script.
  ```bash 
  katana 
  ``` 
 - On a new terminal, run this command: 
 ```bash
 python3 src/tests/test_contract.py
 ```

The invalid signature should occur from there. 