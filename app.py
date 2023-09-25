import requests
import csv

# Set your Meraki API key and organization ID
api_key = 'YOUR API KEY GOES HERE'
organization_id = 'YOUR ORG ID GOES HERE'

# Define the API endpoint URLs
uplink_statuses_url = f'https://api.meraki.com/api/v1/organizations/{organization_id}/uplinks/statuses'
networks_url = f'https://api.meraki.com/api/v1/organizations/{organization_id}/networks'

# Define headers with the API key
headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json'
}

try:
    # Make the API request to get uplink statuses
    response_uplinks = requests.get(uplink_statuses_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response_uplinks.status_code == 200:
        # Parse the JSON response for uplink statuses
        uplink_statuses = response_uplinks.json()

        # Make the API request to get network data
        response_networks = requests.get(networks_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response_networks.status_code == 200:
            # Parse the JSON response for networks
            networks = response_networks.json()

            # Create a dictionary to store network name by ID
            network_names = {network['id']: network['name'] for network in networks}

            # Create a list to store the desired information
            uplink_info_list = []

            # Iterate through each device's uplinks
            for device_status in uplink_statuses:
                network_id = device_status['networkId']
                serial = device_status['serial']

                # Get the network name from the dictionary
                network_name = network_names.get(network_id, 'N/A')

                # Iterate through each uplink of the device
                for uplink in device_status.get('uplinks', []):
                    interface = uplink.get('interface', 'N/A')
                    status = uplink.get('status', 'N/A')

                    # Append the information to the list
                    uplink_info_list.append([network_name, serial, interface, status])

            # Specify the CSV file name
            csv_file = 'uplink_statuses.csv'

            # Write data to CSV file with headings
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                # Add headings to the CSV file
                writer.writerow(['Network Name', 'Serial Number', 'Interface', 'Status'])
                # Write the data
                writer.writerows(uplink_info_list)

            print(f'Data written to {csv_file} successfully!')
        else:
            print(f'Error: {response_networks.status_code} - {response_networks.text}')
    else:
        print(f'Error: {response_uplinks.status_code} - {response_uplinks.text}')

except Exception as e:
    print(f'An error occurred: {str(e)}')
