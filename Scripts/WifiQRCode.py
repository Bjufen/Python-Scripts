import subprocess
import re
import wifi_qrcode_generator.generator

Id = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8').split('\n')

pattern = r"Profile\s+:\s+(.+)"

profile_name = None
for line in Id:
    match = re.search(pattern, line)
    if match:
        profile_name = match.group(1).strip()
        break


id_results = '"' + profile_name + '"'  # Add double quotes around the profile name


password = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', 'ARRIS-4A72-5G', 'key=clear']).decode('utf-8').split('\n')

pattern = r"Key Content\s+:\s+(.+)"

key_content = None
for line in password:
    match = re.search(pattern, line)
    if match:
        key_content = match.group(1).strip()
        break

print("User name:", id_results)
print("Password:", key_content)

# Generate QR code
qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
    ssid=id_results,
    hidden=False,
    authentication_type='WPA',  # Adjust authentication type as needed
    password=key_content
)


qr_code.print_ascii()
