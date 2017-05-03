create table switches (
    hostname    text primary key,
    location    text
);

create table dhcp (
    mac          text primary key,
    ip           text,
    vlan         text,
    interface    text,
    switch       text not null references switches(hostname)
);
