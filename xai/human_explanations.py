"""Human-readable string mappings for technical features."""

EXPLANATIONS = {
    "url_length": {
        "BASIC": "This website uses a very long address, which is sometimes seen in phishing attacks.",
        "ADVANCED": "The URL length exceeds normal baseline bounds, a common indicator of obfuscation.",
        "TECHNICAL": "url_length standard deviation exceeded +2.5σ."
    },
    "entropy": {
        "BASIC": "The website address contains unusual patterns.",
        "ADVANCED": "The domain contains random-looking characters often used to evade detection.",
        "TECHNICAL": "Shannon entropy of the domain string > 4.5."
    },
    "lookalike": {
        "BASIC": "This website appears to imitate a trusted brand.",
        "ADVANCED": "The domain name closely resembles a known legitimate organization, likely a typo-squatting attempt.",
        "TECHNICAL": "Levenshtein distance <= 2 against Alexa Top 100 brands."
    },
    "ascii_lookalike": {
        "BASIC": "This website appears to imitate a trusted brand using similar-looking characters.",
        "ADVANCED": "ASCII character substitutions detected that resemble a known brand.",
        "TECHNICAL": "ASCII homoglyph substitution detected."
    },
    "subdomains": {
        "BASIC": "The website address has a complex structure.",
        "ADVANCED": "The URL contains multiple subdomains, which is often used to hide the true destination.",
        "TECHNICAL": "Subdomain depth >= 3."
    },
    "has_ip_address": {
        "BASIC": "This website uses an IP address instead of a standard name.",
        "ADVANCED": "The URL navigates directly to an IP address rather than a registered domain name.",
        "TECHNICAL": "Regex match for IPv4/IPv6 in netloc."
    },
    "ip_address": {
        "BASIC": "This website uses an IP address instead of a standard name.",
        "ADVANCED": "The URL navigates directly to an IP address rather than a registered domain name.",
        "TECHNICAL": "Regex match for IPv4/IPv6 in netloc."
    },
    "punycode": {
        "BASIC": "The website uses special characters to trick you into thinking it's a different site.",
        "ADVANCED": "The domain uses internationalized characters (Punycode) to visually spoof a legitimate domain.",
        "TECHNICAL": "xn-- prefix detected indicating IDNA encoding."
    },
    "tld_score": {
        "BASIC": "The website uses a domain ending that is frequently used by scammers.",
        "ADVANCED": "The Top-Level Domain (TLD) has a poor reputation in global threat intelligence feeds.",
        "TECHNICAL": "TLD classified as HIGH or CRITICAL risk."
    },
    "tld_risk_level": {
        "BASIC": "The website uses a domain ending that is frequently used by scammers.",
        "ADVANCED": "The Top-Level Domain (TLD) has a poor reputation in global threat intelligence feeds.",
        "TECHNICAL": "TLD classified as HIGH or CRITICAL risk."
    },
    "brand_mismatch": {
        "BASIC": "The website claims to be a brand but the address doesn't match.",
        "ADVANCED": "A brand name is present in the path or subdomain, but the root domain does not belong to that brand.",
        "TECHNICAL": "Extracted brand name from corpus != root domain registrar."
    },
    "hyphen_count": {
        "BASIC": "The website address contains many hyphens, which is unusual for legitimate sites.",
        "ADVANCED": "Excessive hyphens in the URL are a common phishing obfuscation technique.",
        "TECHNICAL": "Hyphen count in domain > threshold."
    },
    "has_at_symbol": {
        "BASIC": "The website address contains a suspicious '@' character.",
        "ADVANCED": "The '@' symbol in a URL can be used to disguise the true destination.",
        "TECHNICAL": "URL contains '@' which may redirect to unexpected host."
    },
    "digit_ratio": {
        "BASIC": "The website address contains an unusual number of digits.",
        "ADVANCED": "High digit-to-letter ratio suggests a randomly generated or obfuscated domain.",
        "TECHNICAL": "Digit ratio exceeds normal distribution bounds."
    },
    "token_count": {
        "BASIC": "The website address is broken into many parts, suggesting complexity.",
        "ADVANCED": "High token count in the URL path indicates possible obfuscation.",
        "TECHNICAL": "URL tokenization count exceeds baseline threshold."
    },
    "dot_count": {
        "BASIC": "The website address has an unusual structure with many separators.",
        "ADVANCED": "Excessive dots in the URL may indicate subdomain abuse.",
        "TECHNICAL": "Dot count in URL exceeds threshold."
    },
    "high_entropy": {
        "BASIC": "The website address contains unusual patterns.",
        "ADVANCED": "The domain contains random-looking characters often used to evade detection.",
        "TECHNICAL": "Shannon entropy flag triggered."
    },
    "url_length_risk_points": {
        "BASIC": "This website uses a very long address, which is sometimes seen in phishing attacks.",
        "ADVANCED": "The URL length risk score exceeds normal bounds.",
        "TECHNICAL": "url_length_risk_points > threshold."
    },
    "unicode_homograph": {
        "BASIC": "The website uses special characters to trick you into thinking it's a different site.",
        "ADVANCED": "Unicode homograph attack detected — visually identical characters from different scripts.",
        "TECHNICAL": "Unicode confusable characters detected via ICU tables."
    },
    # Features that are NOT suspicious by themselves — provide neutral explanations
    "uses_https": {
        "BASIC": "Multiple phishing indicators were detected.",
        "ADVANCED": "HTTPS alone does not guarantee safety; other indicators contributed to this classification.",
        "TECHNICAL": "HTTPS presence noted; not a primary classification factor."
    }
}

def get_human_explanation(feature_name: str, level: str = "BASIC") -> str:
    """Return a human-friendly string for a given feature."""
    feature_dict = EXPLANATIONS.get(feature_name)
    if not feature_dict:
        # Intelligent fallback instead of exposing raw feature names
        clean_name = feature_name.replace('_', ' ')
        # Avoid confusing explanations for benign features
        benign_features = {'uses https', 'uses http', 'valid'}
        if clean_name.lower() in benign_features:
            return "Multiple phishing indicators were detected."
        return f"The website address has suspicious characteristics."
        
    return feature_dict.get(level, feature_dict["BASIC"])
