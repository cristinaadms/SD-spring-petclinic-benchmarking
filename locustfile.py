from locust import HttpUser, task, between
import random

class PetClinicUser(HttpUser):
    wait_time = between(1, 3)

    @task(4)  # 40%
    def get_owners(self):
        self.client.get("http://localhost:8081/owners")

    @task(3)  # 30%
    def get_owner_by_id(self):
        owner_id = random.randint(1, 10)
        self.client.get(f"http://localhost:8081/owners/{owner_id}")

    @task(2)  # 20%
    def get_vets(self):
        self.client.get("http://localhost:8083/vets")

    @task(1)  # 10%
    def create_owner(self):
        owner = {
            "firstName": "Teste",
            "lastName": f"User{random.randint(1,10000)}",
            "address": "Rua 123",
            "city": "Teresina",
            "telephone": "999999999"
        }
        self.client.post("http://localhost:8081/owners", json=owner)
