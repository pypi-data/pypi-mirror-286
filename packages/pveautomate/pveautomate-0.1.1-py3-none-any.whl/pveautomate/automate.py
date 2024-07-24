import requests
import time
import urllib3
import csv
from random import randint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProxmoxManager:
    def __init__(self, proxmox_url, proxmox_user, proxmox_password, node, verify_ssl=False):
        """
        Initialize the ProxmoxManager with the required parameters.

        Args:
            proxmox_url (str): The URL of the Proxmox VE server.
            proxmox_user (str): The username to authenticate with.
            proxmox_password (str): The password to authenticate with.
            node (str): The Proxmox VE node to manage.
            verify_ssl (bool): Whether to verify SSL certificates. Defaults to False.
        """
        self.proxmox_url = proxmox_url
        self.proxmox_user = proxmox_user
        self.proxmox_password = proxmox_password
        self.node = node
        self.verify_ssl = verify_ssl
        self.vm_data_headers = ["VMID", "IP", "OWNER", "HNAME"]
        self.vm_data = []
        self.raw_data = ""
        
    def write_vm_data(self):
        """
        Write VM data to a CSV file.

        This method is usually internal and is used to dump data on range VMs to a CSV file.
        """
        with open("data.csv", "w", newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=self.vm_data_headers)
            csv_writer.writeheader()
            csv_writer.writerows(self.vm_data)

    def read_vm_data(self):
        """
        Read VM data from a CSV file.

        This method is usually internal and is used to load data on range VMs from a CSV file.
        """
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            self.vm_data = [row for row in reader]
            self.raw_data = file.read()

    def authenticate(self):
        """
        Authenticate with the Proxmox VE host and obtain a ticket and CSRF token.

        This method is usually internal and is used to authorize with the PVE host.

        Returns:
            tuple: A tuple containing the ticket and CSRF token.
        """
        response = requests.post(
            f"{self.proxmox_url}/access/ticket",
            data={"username": self.proxmox_user, "password": self.proxmox_password},
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return data["ticket"], data["CSRFPreventionToken"]

    def get_next_vm_id(self, ticket):
        """
        Get the next available VMID for clone/create operations.

        Args:
            ticket (str): The authentication ticket.

        Returns:
            int: The next available VMID.
        """
        next_id_url = f"{self.proxmox_url}/cluster/nextid"
        headers = {"Cookie": f"PVEAuthCookie={ticket}"}
        response = requests.get(next_id_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        next_id = response.json()["data"]
        return next_id

    def clone_vm(self, ticket, csrf_token, template_id, new_name, new_id):
        """
        Clone a VM or template to a new VMID and assign a new name.

        Args:
            ticket (str): The authentication ticket.
            csrf_token (str): The CSRF prevention token.
            template_id (int): The ID of the template to clone.
            new_name (str): The new name for the cloned VM.
            new_id (int): The new VMID for the cloned VM.

        Returns:
            dict: The response data from the clone operation.
        """
        clone_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{template_id}/clone"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {"newid": new_id, "name": new_name, "node": self.node, "vmid": template_id}
        response = requests.post(
            clone_url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()["data"]

    def assign_admin_vm_permissions(self, ticket, csrf_token, vm_id, user):
        """
        Assign admin permissions to a user for a given VMID.

        Args:
            ticket (str): The authentication ticket.
            csrf_token (str): The CSRF prevention token.
            vm_id (int): The ID of the VM.
            user (str): The user to assign admin permissions to.
        """
        acl_url = f"{self.proxmox_url}/access/acl"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {"path": f"/vms/{vm_id}", "users": user, "roles": "Administrator"}
        response = requests.put(acl_url, headers=headers, data=payload, verify=self.verify_ssl)
        response.raise_for_status()

    def set_vm_desc(self, ticket, csrf_token, vm_id, desc):
        """
        Set the description (Notes) of a VMID.

        Args:
            ticket (str): The authentication ticket.
            csrf_token (str): The CSRF prevention token.
            vm_id (int): The ID of the VM.
            desc (str): The description to set for the VM.
        """
        conf_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vm_id}/config"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {
            "description": desc,
        }
        response = requests.put(conf_url, headers=headers, data=payload, verify=self.verify_ssl)
        response.raise_for_status()

    def destroy_vm(self, vmid):
        """
        Destroy a VM by its ID.

        Args:
            vmid (int): The ID of the VM to destroy.
        """
        ticket, csrf_token = self.authenticate()
        delete_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        response = requests.delete(delete_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        self.vm_data = [vm for vm in self.vm_data if str(vm["VMID"]) != str(vmid)]
        self.write_vm_data()
        print(f"VM {vmid} on node {self.node} has been destroyed.")

    def destroy_range(self):
        """
        Destroy all range VMs.

        This method is intended for internal use and may not be suitable for a library.
        """
        self.read_vm_data()
        for vm in self.vm_data:
            print("Destroying VMID " + str(vm["VMID"]))
            self.destroy_vm(vm["VMID"])

    def create_win_range(self, user=None):
        """
        Create three cloned VMs for a given username.

        This method is intended for internal use and may not be suitable for a library.

        Args:
            user (str): The username to assign to the cloned VMs. Defaults to None.
        """
        template_vm_ids = [112, 135, 144]
        if user is None:
            user = input("Owner user (format 'foo@pve' or 'foo@pam'): ")
        uf = user.split("@")[0]
        new_instance_names = [uf + "-win1", uf + "-win2", uf + "-win3"]

        ticket, csrf_token = self.authenticate()
        for template_id, new_name in zip(template_vm_ids, new_instance_names):
            new_id = self.get_next_vm_id(ticket)
            self.clone_vm(ticket, csrf_token, template_id, new_name, new_id)
            time.sleep(2)
            self.assign_admin_vm_permissions(ticket, csrf_token, new_id, user)

            ip_last_bits = randint(100, 140)
            found = True
            while found:
                if "." + str(ip_last_bits) not in self.raw_data:
                    found = False
                else:
                    ip_last_bits = randint(100, 140)

            data = {
                "VMID": str(new_id),
                "IP": "10.0.1." + str(ip_last_bits),
                "OWNER": user,
                "HNAME": new_name,
            }
            self.vm_data.append(data)

            self.set_vm_desc(ticket, csrf_token, new_id, "My IP should be set to: " + data["IP"])

            print(
                f"VMID - {new_id}, {new_name} cloned from template {template_id} and permissions assigned to {user}"
            )
            self.write_vm_data()


if __name__ == "__main__":
    print("Stop it")
