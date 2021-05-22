control ingress {
    process_cache();
    process_value();
    
    apply (ipv4_route);
}

control egress {
    if (nc_hdr.op == NC_READ_REQUEST and nc_cache_md.cache_exist != 1) {
        heavy_hitter();
    }
    apply (ethernet_set_mac);
}
