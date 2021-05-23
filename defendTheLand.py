import os, sys
import re
import subprocess


def readLogs(log_file = "/var/log/apache2/access.log"):
    '''
    This definition opens the file that contains the logs
    return: returns the list of lines. Each line represents a log messsage
    '''
    f = open(os.path.join(sys.path[0], log_file), "r")
    lines = f.readlines()
    return lines


def searchLogin(log_list):
    '''
    This def searches to  find for malicious activity in a list of log messages.
    return: It returns a list with the malicious IPs identified in the logs
    '''
    #login_pattern = re.compile()
    # Define the regexs pattern to match an IP address
    ip_pattern = (r"^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})")
    # Initialize an empy list to host the malicious IPs
    malicious_ip_list = []
    for log in log_list:
        # Checks whether there is any dodgy paths in the logs
        if ("/wp-login.php" in log) or ("/wp-admin" in log) or ("/xmlrpc.php" in log) or ("/admin" in log):
            # Uses regexs to get the IP address
            malicious_ip = re.search(ip_pattern, log)
            # Places the IP address into the list
            malicious_ip_list.append(malicious_ip[0])
            # It is going to store the log entry so I can paste it in my wall of shame
            try:
                f = open("/home/pi/security/mfuckers.txt", "a")
                f.write(log)
                f.close()
            except:
                pass
    print(malicious_ip_list)
    return malicious_ip_list


def getUFW():
    '''
    It executes the command #sudo ufw status in order to get the UFW rules
    resource: https://www.circuitbasics.com/run-linux-commands-with-python/
    It then returns the ufw as a string
    '''
    x = subprocess.run(['sudo','ufw','status','numbered'], capture_output=True)
    ufw = x.stdout.decode()
    return ufw


def filterMaliciousIPs(malicious_ips):
    '''
    Gets the list of malicious IPs and then filters the IPs to find which are already configured in the UFW
    returns a list of unique IP addresses that are not into the UFW
    '''
    # Deleting duplicates by creating a dictionary (keys are unique) and then convert the dictionary back to a list: https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    malicious_ips = list(dict.fromkeys(malicious_ips))
    # loops the IPs
    ufw_table = getUFW()
    for ip in malicious_ips:
        # Checks whether the IPs are already in UFW
        if ip in ufw_table:
            malicious_ips.remove(ip)
    return malicious_ips


def configureUFW(ufw_ip_list):
    '''
    This definition adds a list of IP addresses into the UFW table
    '''
    for ip in ufw_ip_list:
        try:
            x = subprocess.run(['sudo', 'ufw', 'insert', '1', 'deny', 'in', 'from', ip], capture_output=True)
            #print(f"sudo ufw insert 1 deny in from {ip}")
        except:
            pass


if __name__ == "__main__":
    f=readLogs()
    malicious_ips = searchLogin(f)
    filtered_malicious_ips = filterMaliciousIPs(malicious_ips)
    configureUFW(filtered_malicious_ips)
