import logging

try:
    import queue
except ImportError:
    import Queue as queue

log = logging.getLogger('scitags')


def run(flow_queue, term_event, flow_map, ip_config):
    while not term_event.is_set():
        try:
            flow_id = flow_queue.get(block=True, timeout=0.5)
        except queue.Empty:
            continue

        log.debug(flow_id)

