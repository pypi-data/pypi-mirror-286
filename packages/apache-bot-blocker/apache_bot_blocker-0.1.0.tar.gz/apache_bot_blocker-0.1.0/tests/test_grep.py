import subprocess

# File containing the logs
log_file = 'digipart-custom.log-20240407.gz'

# Grep command to find lines with IPs ending in odd digits
grep_command = f"grep -E '[0-9]+\\.[0-9]+\\.[0-9]+\\.[13579]\\b' {log_file}"

# Run the grep command
result = subprocess.run(grep_command, shell=True, capture_output=True, text=True)

# Print the output
print(result.stdout)
