# User Agent Tools

This project provides a Python class `UA` for working with user agent strings. It offers functionality for generating random user agents, interpreting user agent strings, and extracting information about operating systems, browsers, and platforms.

## Features

- Generate random user agents with optional browser and system filters
- Interpret user agent strings to extract OS, browser, and platform information

## Installation

```bash
pip install user-agent-tools
```

## Usage

```python
from user_agent_tools import UA

# Initialize the UA class
ua_tools = UA()

# Generate a random user agent
random_ua = ua_tools.random()
print(f"Random User Agent: {random_ua}")

# Generate a random user agent for Chrome on Windows
chrome_windows_ua = ua_tools.random(browser="Chrome", system="Windows")
print(f"Random Chrome on Windows User Agent: {chrome_windows_ua}")

# Interpret a user agent string
ua_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
interpretation = ua_tools.interpret(ua_string)
print(f"Interpretation: {interpretation}")

# Most common user agent
most_common_ua = ua_tools.top_user_agent()
print(f"Most Common User Agent: {most_common_ua}")

# Top-n user agents
top_5_uas = ua_tools.top_n_user_agents(5)
print("Top 5 User Agents:")
for i, ua in enumerate(top_5_uas, 1):
    print(f"{i}. {ua}")
```

## License

This project is licensed under the Creative Commons Zero v1.0 Universal (CC0) license. 

## Acknowledgments

Thanks to willshouse.com, source of the [useragents by prevalence](https://techblog.willshouse.com/2012/01/03/most-common-user-agents/) listed in `data.json`.