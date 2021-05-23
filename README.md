# DefendTheLand

## GeorgiosZ Project: https://github.com/ZervakisGeorgios/DefendTheLand

## Description:
```
This script performs the following actions:
 • It will try to open the apache2 access.log file by default and read the logs
 • It will then pass the logs to another method to filter the logs. It tries to find logs that tried to access the admin panel or perform xmlrpc.php attack. It will store each malicious log into the mfuckers.txt file under /home/pi/security directory.
 • It will then delete duplicates and will drop IP addresses that are already into the UFW table
 • FInally, it will place the malicious IP addresses into the UFW table
 
**Next weekend, I will release a newer version of thiss cript. The final goal is to configure a cron job in the linux server and have the script running continuously. In order not to block the legit administrators out, the script will ask the user to input a list of IPs that should be ignored.**
```
## Input Variables:
```
By default the script will not ask to input variables. Most likely, you will need to modify the variables from inside the script to define where to store the malicious log entries and/or to point it to a different log file.
```
## Usage:
```
•	Download this repository and place it into the directory of your choice.
•	Modify line 36 to point the script to store the malicious logs in an appropriate file.
•	If necessary, pass the full path of the log file by calling the readLogs method in line 85
```
## Output:
```
The script will output the list with all malicious IP addressses. Feel free to comment it out
'''
