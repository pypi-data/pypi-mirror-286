import requests
import time
import getpass
import urllib3
import csv
from random import randint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProxmoxManager:
    def __init__(self, proxmox_url, proxmox_user, proxmox_password, node, verify_ssl=False):
        self.proxmox_url = proxmox_url
        self.proxmox_user = proxmox_user
        self.proxmox_password = proxmox_password
        self.node = node
        self.verify_ssl = verify_ssl
        self.vm_data_headers = ["VMID", "IP", "OWNER", "HNAME"]
        self.vm_data = []
        self.raw_data = ""
        
    def write_vm_data(self):
        with open("data.csv", "w", newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=self.vm_data_headers)
            csv_writer.writeheader()
            csv_writer.writerows(self.vm_data)

    def read_vm_data(self):
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            self.vm_data = [row for row in reader]
            self.raw_data = file.read()

    def authenticate(self):
        response = requests.post(
            f"{self.proxmox_url}/access/ticket",
            data={"username": self.proxmox_user, "password": self.proxmox_password},
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return data["ticket"], data["CSRFPreventionToken"]

    def get_next_vm_id(self, ticket):
        next_id_url = f"{self.proxmox_url}/cluster/nextid"
        headers = {"Cookie": f"PVEAuthCookie={ticket}"}
        response = requests.get(next_id_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        next_id = response.json()["data"]
        return next_id

    def clone_vm(self, ticket, csrf_token, template_id, new_name, new_id):
        clone_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{template_id}/clone"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {"newid": new_id, "name": new_name, "node": self.node, "vmid": template_id}
        response = requests.post(
            clone_url, headers=headers, data=payload, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()["data"]

    def assign_permissions(self, ticket, csrf_token, vm_id, user):
        acl_url = f"{self.proxmox_url}/access/acl"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {"path": f"/vms/{vm_id}", "users": user, "roles": "Administrator"}
        response = requests.put(acl_url, headers=headers, data=payload, verify=self.verify_ssl)
        response.raise_for_status()

    def set_vm_desc(self, ticket, csrf_token, vm_id, desc):
        conf_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vm_id}/config"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        payload = {
            "description": desc,
        }
        response = requests.put(conf_url, headers=headers, data=payload, verify=self.verify_ssl)
        response.raise_for_status()

    def destroy_vm(self, vmid):
        ticket, csrf_token = self.authenticate()
        delete_url = f"{self.proxmox_url}/nodes/{self.node}/qemu/{vmid}"
        headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
        response = requests.delete(delete_url, headers=headers, verify=self.verify_ssl)
        response.raise_for_status()
        self.vm_data = [vm for vm in self.vm_data if str(vm["VMID"]) != str(vmid)]
        self.write_vm_data()
        print(f"VM {vmid} on node {self.node} has been destroyed.")

    def destroy_range(self):
        self.read_vm_data()
        for vm in self.vm_data:
            print("Destroying VMID " + str(vm["VMID"]))
            self.destroy_vm(vm["VMID"])

    def create_win_range(self, user=None):
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
            self.assign_permissions(ticket, csrf_token, new_id, user)

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
    proxmox_url = "https://10.0.1.12:8006/api2/json"
    proxmox_user = "root@pam"
    proxmox_password = getpass.getpass(f"Authenticate for {proxmox_user}: ")
    node = "pve4"

    manager = ProxmoxManager(proxmox_url, proxmox_user, proxmox_password, node)

    running = True

    while running:
        manager.read_vm_data()
        print(
            """1. Create Windows range VMs for user
2. Destroy single VM
3. Destroy multiple VMs
4. Destroy ALL range VMs
5. Create Windows range VMs for multiple users
Q. Quit"""
        )
        c = input("> ")
        if c == "1":
            manager.create_win_range()
        elif c == "5":
            users = input("Comma-seperated list of users to make VMs for: ")
            for user in users.split(","):
                if not '@' in user:
                    user = user + "@pve"
                manager.create_win_range(user)
        elif c == "2":
            manager.destroy_vm(int(input("VMID to destroy (NO CONFIRMATION): ")))
        elif c == "3":
            kaboom = input("Comma-seperated list to remove (NO CONFIRMATION): ")
            for id in kaboom.split(","):
                manager.destroy_vm(int(id))
        elif c == "4":
            manager.destroy_range()
        else:
            running = False
