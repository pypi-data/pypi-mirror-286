import random

class UserAgentGenerator:
    def __init__(self):
        self.user_agent = self.generate_user_agent()

    def generate_user_agent(self):
        dalvik_user_agents = [
            "Dalvik/{}.{} (Linux; U; Android {}; {} Build/{}{})",
            "Dalvik/{}.{} (Linux; Android {}; {} Build/{}{})",
        ]

        devices = [
            "SM-G920F", "Nexus 5", "Nexus 6P", "Pixel 2", "Pixel 4", "Galaxy S10", "Galaxy S20",
            "SM-G975F", "SM-G950F", "SM-G960F", "SM-G970F", "SM-G973F", "SM-G980F",
            "SM-N960F", "SM-N950F", "SM-N970F", "SM-N975F", "SM-N980F", "SM-N985F",
            "P30 Pro", "P20 Pro", "Mate 20 Pro", "Mate 30 Pro", "Mate 40 Pro",
            "Mi 9", "Mi 10", "Mi 11", "Redmi Note 8", "Redmi Note 9", "Redmi Note 10",
            "OnePlus 7", "OnePlus 7T", "OnePlus 8", "OnePlus 8T", "OnePlus 9", "OnePlus 9 Pro",
            "Xperia Z5", "Xperia XZ1", "Xperia XZ2", "Xperia XZ3", "Xperia 1", "Xperia 5",
            "HTC U11", "HTC U12+", "HTC 10", "HTC One M9", "HTC One M8",
            "LG G6", "LG G7 ThinQ", "LG V30", "LG V40 ThinQ", "LG V50 ThinQ",
            "Google Pixel", "Google Pixel XL", "Google Pixel 2 XL", "Google Pixel 3", "Google Pixel 3 XL",
            "Galaxy A50", "Galaxy A51", "Galaxy A70", "Galaxy A71", "Galaxy A80", "Galaxy A90",
        ]

        versions = [
            "7.0", "7.1.1", "8.0.0", "8.1.0", "9", "10", "11"
        ]

        brands = [
            "Google", "Samsung", "Huawei", "Sony", "HTC", "OnePlus", "Xiaomi", "LG"
        ]

        template = random.choice(dalvik_user_agents)
        android_version = random.choice(versions)
        device = random.choice(devices)
        brand = random.choice(brands)
        generate_version = random.randint(1, 99)
        user_agent = template.format(generate_version, generate_version, android_version, brand, device, generate_version)
        return user_agent

    def __str__(self):
        return self.user_agent
