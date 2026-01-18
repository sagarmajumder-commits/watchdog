# watchdog

Lightweight API health monitoring with configurable alerts.

## Features

- Monitor multiple endpoints
- Configurable check intervals
- Response time tracking
- Slack notifications (optional)
- Detailed logging

## Setup

```bash
pip install -r requirements.txt
cp config.yaml.example config.yaml
# Edit config.yaml with your endpoints
python watchdog.py
```

## Configuration

```yaml
endpoints:
  - name: "Production API"
    url: "https://api.example.com/health"
    interval: 60
    timeout: 10
    
notifications:
  slack:
    enabled: false
    webhook_url: ""
```

## Requirements

- Python 3.8+

## License

MIT
