# DORA Lead Time Calculator

A Python script that calculates one of the four key DORA metrics - lead time.
Calculations are done based on the time from first commit to `master` for all pull requests within the last six months.

## Requirements

```bash
sudo apt install python3 python3-pip
pip install -r requirements.txt
```

## Usage

Set environment variables or configure the `.env` file with the following variables

- `GH_TOKEN=<YOUR_GITHUB_TOKEN>`, GitHub access token to be used for login
- `TARGETS=projectA,projectB,projectC`, comma separated list of value containing the target project names

```bash
❯ python main.py
Project              Lead Time (days)
ProjectA                        11.71
ProjectB                         5.50
ProjectC                        13.79
```

> _**Note**: There is no error handling as this is just a simple automation script._
