import os
from urllib.parse import urlparse

# Module level cache
_TRUSTED_DOMAINS_CACHE = set()

def load_trusted_domains():
    global _TRUSTED_DOMAINS_CACHE
    if _TRUSTED_DOMAINS_CACHE:
        return _TRUSTED_DOMAINS_CACHE
        
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'trusted_domains.txt')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip().lower()
                if domain:
                    _TRUSTED_DOMAINS_CACHE.add(domain)
    except FileNotFoundError:
        print(f"Warning: {data_file} not found.")
        
    return _TRUSTED_DOMAINS_CACHE

def is_trusted_domain(url):
    try:
        # Ensure it has a scheme for urlparse to work correctly
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
            
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Strip port if present
        if ':' in domain:
            domain = domain.split(':')[0]
            
        # Strip 'www.' if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        trusted = load_trusted_domains()
        
        # Check exact match
        if domain in trusted:
            return True
            
        # Check subdomains (e.g. docs.google.com -> google.com in trusted)
        parts = domain.split('.')
        for i in range(len(parts) - 1):
            parent_domain = '.'.join(parts[i:])
            if parent_domain in trusted:
                return True
                
        return False
    except Exception:
        return False
