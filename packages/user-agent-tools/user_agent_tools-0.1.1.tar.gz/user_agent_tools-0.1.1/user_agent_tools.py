import json
import random
import re


OS_PATTERNS = [
    (r"Android", "Android"),
    (r"iPhone|iPad|iPod", "iOS"),
    (r"Windows NT 10\.0", "Windows 10"),
    (r"Windows NT 6\.3", "Windows 8.1"),
    (r"Windows NT 6\.2", "Windows 8"),
    (r"Windows NT 6\.1", "Windows 7"),
    (r"Windows NT 6\.0", "Windows Vista"),
    (r"Windows NT 5\.1", "Windows XP"),
    (r"Windows NT 5\.0", "Windows 2000"),
    (r"Mac OS X", "macOS"),
    (r"Linux", "Linux"),
]
BROWSER_PATTERNS = [
    (r"Chrome/(\S+)", "Chrome"),
    (r"Firefox/(\S+)", "Firefox"),
    (r"Safari/(\S+)", "Safari"),
    (r"Opera/(\S+)", "Opera"),
    (r"MSIE (\S+)", "Internet Explorer"),
    (r"Trident/.*rv:(\S+)", "Internet Explorer"),
    (r"Edge/(\S+)", "Microsoft Edge"),
]


class UA:
    def __init__(self):
        self.user_agents = []
        self.load_data()

    def load_data(self):
        with open("data.json", "r") as file:
            self.user_agents = json.load(file)

        # Sort by probability
        self.user_agents.sort(key=lambda ua: ua["prob"], reverse=True)

        # Normalize probabilities
        total_prob = sum(ua["prob"] for ua in self.user_agents)
        for ua in self.user_agents:
            ua["prob"] /= total_prob

    def top_user_agent(self):
        return self.user_agents[0]["ua"]

    def top_n_user_agents(self, n):
        return [ua["ua"] for ua in self.user_agents[:n]]

    def random(self, browser=None, system=None):
        filtered_uas = self.user_agents
        if browser:
            filtered_uas = [
                ua
                for ua in filtered_uas
                if browser.lower() in ua["system"].lower()
            ]
        if system:
            filtered_uas = [
                ua
                for ua in filtered_uas
                if system.lower() in ua["system"].lower()
            ]
        if not filtered_uas:
            raise ValueError("No user agents match the specified criteria")

        total_prob = sum(ua["prob"] for ua in filtered_uas)

        r = random.uniform(0, total_prob)

        cumulative_prob = 0
        for ua in filtered_uas:
            cumulative_prob += ua["prob"]
            if r <= cumulative_prob:
                return ua["ua"]

        return filtered_uas[-1]["ua"]

    def interpret(self, user_agent):
        result = {
            "system": "Unknown",
            "os": "Unknown",
            "browser": "Unknown",
            "browser_version": "Unknown",
            "platform": "Unknown",
        }

        for pattern, os_name in OS_PATTERNS:
            if re.search(pattern, user_agent):
                result["os"] = os_name
                if "Windows" in os_name:
                    result["platform"] = "windows"
                elif os_name == "macOS":
                    result["platform"] = "macos"
                elif os_name == "Android":
                    result["platform"] = "android"
                elif os_name == "iOS":
                    result["platform"] = "ios"
                elif os_name == "Linux":
                    result["platform"] = "linux"
                break

        if "Kindle" in user_agent:
            result["platform"] = "kindle"

        for pattern, browser_name in BROWSER_PATTERNS:
            match = re.search(pattern, user_agent)
            if match:
                result["browser"] = browser_name
                result["browser_version"] = match.group(1)
                break

        return result
