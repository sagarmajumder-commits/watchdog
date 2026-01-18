"""API health monitoring daemon."""
import time
import logging
import yaml
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/watchdog.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class EndpointMonitor:
    """Monitor for a single API endpoint."""
    
    def __init__(self, config: Dict):
        self.name = config['name']
        self.url = config['url']
        self.timeout = config.get('timeout', 10)
        self.interval = config.get('interval', 60)
        self.last_status = None
        
    def check(self) -> Dict:
        """
        Check endpoint health.
        
        Returns:
            Dict with status, response_time, and error if any
        """
        try:
            start = time.time()
            response = requests.get(self.url, timeout=self.timeout)
            elapsed = time.time() - start
            
            status = 'UP' if response.status_code == 200 else 'DOWN'
            
            result = {
                'name': self.name,
                'status': status,
                'status_code': response.status_code,
                'response_time': round(elapsed, 3),
                'timestamp': datetime.now().isoformat()
            }
            
            if status != self.last_status:
                logger.warning(f"{self.name} status changed: {self.last_status} -> {status}")
            
            self.last_status = status
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"{self.name}: Timeout after {self.timeout}s")
            return {'name': self.name, 'status': 'TIMEOUT', 'error': 'Request timeout'}
        except requests.exceptions.RequestException as e:
            logger.error(f"{self.name}: {str(e)}")
            return {'name': self.name, 'status': 'ERROR', 'error': str(e)}


def load_config(path: str = 'config.yaml') -> Dict:
    """Load configuration from YAML file."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main monitoring loop."""
    config = load_config()
    monitors = [EndpointMonitor(ep) for ep in config['endpoints']]
    
    logger.info(f"Watchdog started - monitoring {len(monitors)} endpoints")
    
    try:
        while True:
            for monitor in monitors:
                result = monitor.check()
                logger.info(
                    f"{result['name']}: {result['status']} "
                    f"({result.get('response_time', 'N/A')}s)"
                )
            
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Watchdog stopped")


if __name__ == '__main__':
    main()
