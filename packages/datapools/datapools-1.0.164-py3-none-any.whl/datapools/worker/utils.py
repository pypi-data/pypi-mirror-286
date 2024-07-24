from urllib.parse import urlunparse, urlparse

from ..common.queues import QueueMessageType


def get_worker_storage_invalidation_routing_key(worker_id):
    return f"worker_{worker_id}"


def canonicalize_url(url):
    # Normalize the URL to a standard form
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path if p.path != "/" else "", p.params, p.query, ""))
