import ipaddress

# Special-purpose IPv4 ranges
SPECIAL_IPV4 = [
    # "This network", RFC791, Section 3.2
    "0.0.0.0/8",
    # "This host on this network", RFC1122, Section 3.2.1.3
    "0.0.0.0/32",
    # Private-Use, RFC1918
    "10.0.0.0/8",
    # Shared Address Space, RFC6598
    "100.64.0.0/10",
    # Loopback, RFC1122, Section 3.2.1.3
    "127.0.0.0/8",
    # Link Local, RFC3927
    "169.254.0.0/16",
    # Private-Use, RFC1918
    "172.16.0.0/12",
    # IETF Protocol Assignments, RFC6890, Section 2.1
    "192.0.0.0/24",
    # IPv4 Service Continuity Prefix, RFC7335
    "192.0.0.0/29",
    # IPv4 dummy address, RFC7600
    "192.0.0.8/32",
    # Port Control Protocol Anycast, RFC7723
    "192.0.0.9/32",
    # Traversal Using Relays around NAT Anycast, RFC8155
    "192.0.0.10/32",
    # NAT64/DNS64 Discovery, RFC8880, RFC7050, Section 2.2
    "192.0.0.170/32",
    "192.0.0.171/32",
    # Documentation (TEST-NET-1), RFC5737
    "192.0.2.0/24",
    # AS112-v4, RFC7535
    "192.31.196.0/24",
    # AMT, RFC7450
    "192.52.193.0/24",
    # Private-Use, RFC1918
    "192.168.0.0/16",
    # Direct Delegation AS112 Service, RFC7534
    "192.175.48.0/24",
    # Benchmarking, RFC2544
    "198.18.0.0/15",
    # Documentation (TEST-NET-2), RFC5737
    "198.51.100.0/24",
    # Documentation (TEST-NET-3), RFC5737
    "203.0.113.0/24",
    # Multicast (Not listed as special purpose in IANA registry)
    "224.0.0.0/4",
    # Reserved, RFC1112, Section 4
    "240.0.0.0/4",
    # Limited Broadcast, RFC8190, RFC919, Section 7
    "255.255.255.255/32"

    # Deprecated IPv4 ranges. The following prefixes might be included in
    # some filtering guides but were not included here since they are
    # deprecated and may be reallocated any time in the future.
    # Deprecated, previously 6to4 Relay Anycast, RFC7526
    # "192.88.99.0/24",
]

# Special-purpose IPv6 ranges
SPECIAL_IPV6 = [
    # IPv4-compatible, loopback, et al, RFC4291
    "::/8",
    # Loopback Address (included above), RFC4291
    # "::1/128",
    # Unspecified Address (included above), RFC4291
    # "::/128",
    # IPv4-mapped Address (included above), RFC4291
    # "::ffff:0:0/96",
    # IPv4-IPv6 Translat., RFC6052
    "64:ff9b::/96",
    # IPv4-IPv6 Translat., RFC8215
    "64:ff9b:1::/48",
    # Discard-Only Address Block, RFC6666
    "100::/64",
    # IETF Protocol Assignments, RFC2928
    "2001::/23",
    # TEREDO, RFC4380, RFC8190
    "2001::/32",
    # Port Control Protocol Anycast, RFC7723
    "2001:1::1/128",
    # Traversal Using Relays around NAT Anycast, RFC8155
    "2001:1::2/128",
    # Benchmarking, RFC5180, RFC Errata 1752
    "2001:2::/48",
    # AMT, RFC7450
    "2001:3::/32",
    # AS112-v6, RFC7535
    "2001:4:112::/48",
    # ORCHIDv2, RFC7343
    "2001:20::/28",
    # Drone Remote ID Protocol Entity Tags (DETs) Prefix, RFC9374
    "2001:30::/28",
    # Documentation, RFC3849
    "2001:db8::/32",
    # 6to4, RFC3056
    "2002::/16",
    # Direct Delegation AS112 Service, RFC7534
    "2620:4f:8000::/48",
    # Unique-Local, RFC4193, RFC8190
    "fc00::/7",
    # Link-Local Unicast, RFC4291
    "fe80::/10",
    # Multicast, RFC4291
    "ff00::/8",

    # Deprecated IPv6 ranges. The following prefixes might be included in
    # some filtering guides but were not included here since they are
    # deprecated and may be reallocated any time in the future.
    # Deprecated, previously ORCHID, RFC4843
    # "2001:10::/28",
    # Deprecated, previously 6bone, RFC5156, Section 2.9
    # "3ffe::/16",
    # Deprecated, previously site-local, rfc3879 Section 6
    # "fec0::/10",
]

# Sets of networks
SPECIAL_IPV4_NETWORKS = {ipaddress.ip_network(prefix) for prefix in SPECIAL_IPV4}
SPECIAL_IPV6_NETWORKS = {ipaddress.ip_network(prefix) for prefix in SPECIAL_IPV6}

def is_bogon_pfx(prefix):
    """
    This function is used to determine whether a given IP address (either IPv4
    or IPv6) is a part of a special purpose address block.

    The function compares the input address to known special purpose address
    ranges as listed by the Internet Assigned Numbers Authority (IANA) and the
    NLNOG BGP Filter Guide website but also makes some modifications to take
    some upcoming reallocation into account.

    Sources:
    - https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
    - https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
    - https://bgpfilterguide.nlnog.net/guides/bogon_prefixes/
    """
    network = ipaddress.ip_network(prefix)
    networks = SPECIAL_IPV4_NETWORKS if network.version == 4 else SPECIAL_IPV6_NETWORKS
    return any(network.subnet_of(special_net) for special_net in networks)


def is_bogon_asn(asn_raw):
    """
    Check if a given ASN is in any reserved range.

    Sources:
    - https://www.iana.org/assignments/iana-as-numbers-special-registry/iana-as-numbers-special-registry.xhtml
    - https://www.iana.org/assignments/as-numbers/as-numbers.xhtml
    - https://bgpfilterguide.nlnog.net/guides/bogon_asns/
    """
    asn = extract_asn(asn_raw)

    reserved_asns = {
        0,          # Reserved, RFC7607
        112,        # AS112 project, RFC7534
        23456,      # AS_TRANS, RFC6793
        65535,      # Last 16 bit ASN, RFC7300
        4294967295  # Last 32 bit ASN, RFC7300
    }

    if asn in reserved_asns:
        return True

    reserved_asn_ranges = {
        (64496, 64511),           # Documentation/Sample, RFC5398
        (64512, 65534),           # Private use, RFC6996
        (65536, 65551),           # Documentation/Sample, RFC5398
        (65552, 131071),          # IANA reserved, no RFC
        (4200000000, 4294967294)  # Private use, RFC6996
    }

    if any(start <= asn <= end for start, end in reserved_asn_ranges):
        return True
    return False


def extract_asn(asn_raw):
    # Extract the number from the ASN string
    if isinstance(asn_raw, int):
        return asn_raw

    return int(asn_raw.lower().replace("as", "").strip())


def is_out_of_encoding_range(asn_raw, max_asn_encoding=33521664):
    asn = extract_asn(asn_raw)

    if asn > max_asn_encoding:
        return True

    return False
