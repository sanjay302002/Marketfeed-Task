import sys
import time
import signal
import logging

# Configure logging
logging.basicConfig(filename='log_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_log(log_file):
    try:
        logging.info("Starting log monitoring for file: %s", log_file)
        with open(log_file, 'r') as f:
            f.seek(0, 2)  # Move to the end of the file
            while True:
                line = f.readline()
                if line:
                    print(line.strip())  # Print the new log entry
                time.sleep(0.1)  # Sleep briefly to avoid high CPU usage
    except KeyboardInterrupt:
        logging.info("Log monitoring interrupted.")
        sys.exit(0)
    except Exception as e:
        logging.error("An error occurred during log monitoring: %s", str(e))
        sys.exit(1)

def analyze_log(log_file):
    try:
        logging.info("Starting log analysis for file: %s", log_file)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            keywords = ['error', 'HTTP']  # Keywords to search for
            keyword_counts = {keyword: 0 for keyword in keywords}
            for line in lines:
                for keyword in keywords:
                    if keyword in line.lower():
                        keyword_counts[keyword] += 1
            # Print summary report
            logging.info("Summary Report:")
            for keyword, count in keyword_counts.items():
                logging.info("Occurrences of '%s': %d", keyword, count)
    except Exception as e:
        logging.error("An error occurred during log analysis: %s", str(e))
        sys.exit(1)

def signal_handler(signal, frame):
    logging.info("Received signal %s, exiting.", signal)
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_monitor.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    # Register signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)

    monitor_log(log_file)
