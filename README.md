# tristar-poller
Polling of Morningstar Tristar MPPT solar controllers via modbus tcp

* Curently only polls the dip switch settings

### Script steps
1. Reads input .csv for device name and IP
2. Polls modbus holding registers via TCP
3. Converts response into human readable values
4. Saves to output .csv

### Input .csv

By default IP addresses and device names are read from "export.csv"
Name in column 3 and IP address in column 5

### Output .csv

Will output into a .csv


That's it for now

