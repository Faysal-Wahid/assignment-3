# NETWORK DESIGN DOCUMENTATION
## HIT274 Simulation Project - Multi-Campus University Network

---

## PROJECT OVERVIEW

**Scenario:** Multi-Campus University Network Design
- **Organization:** TechVarsity University
- **Structure:** 3 Campus Locations (Student 1, 2, and 3)
- **IPv4 Allocation:** 110.130.32.0/19
- **IPv6 Allocation:** 2001:ABCD:F00::/48

### Network Scenario Description

TechVarsity University operates across three campuses:
1. **Main Campus (Student 1)** - Administrative and Engineering Departments
2. **Medical Campus (Student 2)** - Medical School and Research Labs
3. **Business Campus (Student 3)** - Business School and IT Services

All campuses need to:
- Connect to each other for resource sharing
- Access the central WWW server (Internet simulation)
- Support both IPv4 and IPv6 communication
- Provide wireless connectivity for students and staff
- Ensure redundancy and security

---

## STUDENT 1: MAIN CAMPUS NETWORK DESIGN

### Network Requirements
- **Departments:** Administration, Engineering, Library, Student Services
- **Minimum:** 4 Routers, 6 Switches, 10 End Devices
- **Special:** DNS Server, Web Server, Wireless Network
- **Redundancy:** Dual paths to core, redundant switches

### IP Addressing Scheme (VLSM)

#### IPv4 Subnets (from 110.130.32.0/19)

| Network Name | Network Address | Subnet Mask | CIDR | Hosts | Usage |
|--------------|----------------|-------------|------|-------|-------|
| Administration VLAN | 110.130.32.0 | 255.255.255.128 | /25 | 126 | Admin PCs, Printers |
| Engineering VLAN | 110.130.32.128 | 255.255.255.128 | /25 | 126 | Engineering Lab |
| Library VLAN | 110.130.33.0 | 255.255.255.192 | /26 | 62 | Library Systems |
| Student Services VLAN | 110.130.33.64 | 255.255.255.192 | /26 | 62 | Student PCs |
| Server Farm | 110.130.33.128 | 255.255.255.240 | /28 | 14 | DNS, Web, File Servers |
| Wireless Network | 110.130.33.144 | 255.255.255.240 | /28 | 14 | Wireless Devices |
| Router Link 1 | 110.130.33.160 | 255.255.255.252 | /30 | 2 | R1-R2 |
| Router Link 2 | 110.130.33.164 | 255.255.255.252 | /30 | 2 | R1-R3 |
| Router Link 3 | 110.130.33.168 | 255.255.255.252 | /30 | 2 | R2-R3 |
| Router Link 4 | 110.130.33.172 | 255.255.255.252 | /30 | 2 | R2-R4 |
| Router Link 5 | 110.130.33.176 | 255.255.255.252 | /30 | 2 | R3-R4 |
| To WWW Server | 110.130.33.180 | 255.255.255.252 | /30 | 2 | R1-WWW |
| To Student 2 | 110.130.33.184 | 255.255.255.252 | /30 | 2 | R4-S2 |
| To Student 3 | 110.130.33.188 | 255.255.255.252 | /30 | 2 | R4-S3 |

#### IPv6 Subnets (from 2001:ABCD:F00::/48)

| Network Name | IPv6 Prefix | Usage |
|--------------|-------------|-------|
| Administration VLAN | 2001:ABCD:F00:1::/64 | Admin Network |
| Engineering VLAN | 2001:ABCD:F00:2::/64 | Engineering Lab |
| Library VLAN | 2001:ABCD:F00:3::/64 | Library Systems |
| Student Services VLAN | 2001:ABCD:F00:4::/64 | Student Network |
| Server Farm | 2001:ABCD:F00:5::/64 | Servers |
| Wireless Network | 2001:ABCD:F00:6::/64 | Wireless |
| Router Links | 2001:ABCD:F00:FF::/64 | Inter-router links |

### Network Topology

```
                    [WWW Server]
                          |
                      [Router 1] (Border Router)
                       /      \
                      /        \
                [Router 2]----[Router 3] (Core Routers)
                     \          /
                      \        /
                      [Router 4] (Distribution Router)
                           |
                    To Other Campuses
                           
Router 2 connects to:
- Switch 1 (Administration VLAN 10)
- Switch 2 (Engineering VLAN 20)

Router 3 connects to:
- Switch 3 (Library VLAN 30)
- Switch 4 (Student Services VLAN 40)
- Switch 5 (Server Farm VLAN 50)
- Switch 6 (Wireless Controller + Access Point)
```

### Device List

#### Routers (4)
1. **R1-Main-Border** - Border router connecting to WWW
2. **R2-Main-Core1** - Core router 1
3. **R3-Main-Core2** - Core router 2
4. **R4-Main-Dist** - Distribution router

#### Switches (6)
1. **SW1-Admin** - Administration Department
2. **SW2-Engineering** - Engineering Department
3. **SW3-Library** - Library
4. **SW4-Students** - Student Services
5. **SW5-Servers** - Server Farm
6. **SW6-Wireless** - Wireless Controller

#### End Devices (15+)
- **Administration:** 3 PCs, 1 Printer
- **Engineering:** 3 PCs, 1 Printer
- **Library:** 2 PCs, 1 Printer
- **Student Services:** 3 PCs
- **Servers:** DNS Server, Web Server, File Server
- **Wireless:** 3 Laptops/Tablets

---

## STUDENT 2: MEDICAL CAMPUS NETWORK DESIGN

### Network Requirements
- **Departments:** Medical School, Research Labs, Hospital Wing, Admin
- **Minimum:** 4 Routers, 6 Switches, 10 End Devices
- **Special:** Medical Records Server, DNS Server, Wireless Network

### IP Addressing Scheme (VLSM)

#### IPv4 Subnets (from 110.130.32.0/19)

| Network Name | Network Address | Subnet Mask | CIDR | Hosts | Usage |
|--------------|----------------|-------------|------|-------|-------|
| Medical School VLAN | 110.130.34.0 | 255.255.255.128 | /25 | 126 | Medical PCs |
| Research Lab VLAN | 110.130.34.128 | 255.255.255.128 | /25 | 126 | Research Equipment |
| Hospital Wing VLAN | 110.130.35.0 | 255.255.255.192 | /26 | 62 | Hospital Systems |
| Medical Admin VLAN | 110.130.35.64 | 255.255.255.192 | /26 | 62 | Admin PCs |
| Medical Servers | 110.130.35.128 | 255.255.255.240 | /28 | 14 | Medical Servers |
| Wireless Network | 110.130.35.144 | 255.255.255.240 | /28 | 14 | Wireless Devices |
| Router Links | 110.130.35.160-191 | Various /30 | /30 | 2 each | Inter-router |

#### IPv6 Subnets

| Network Name | IPv6 Prefix | Usage |
|--------------|-------------|-------|
| Medical School | 2001:ABCD:F00:10::/64 | Medical Network |
| Research Lab | 2001:ABCD:F00:11::/64 | Research |
| Hospital Wing | 2001:ABCD:F00:12::/64 | Hospital |
| Medical Admin | 2001:ABCD:F00:13::/64 | Admin |
| Medical Servers | 2001:ABCD:F00:14::/64 | Servers |
| Wireless | 2001:ABCD:F00:15::/64 | Wireless |

---

## STUDENT 3: BUSINESS CAMPUS NETWORK DESIGN

### Network Requirements
- **Departments:** Business School, IT Services, Finance, Marketing
- **Minimum:** 4 Routers, 6 Switches, 10 End Devices
- **Special:** Application Server, DNS Server, Wireless Network

### IP Addressing Scheme (VLSM)

#### IPv4 Subnets (from 110.130.32.0/19)

| Network Name | Network Address | Subnet Mask | CIDR | Hosts | Usage |
|--------------|----------------|-------------|------|-------|-------|
| Business School VLAN | 110.130.36.0 | 255.255.255.128 | /25 | 126 | Business PCs |
| IT Services VLAN | 110.130.36.128 | 255.255.255.128 | /25 | 126 | IT Department |
| Finance VLAN | 110.130.37.0 | 255.255.255.192 | /26 | 62 | Finance Systems |
| Marketing VLAN | 110.130.37.64 | 255.255.255.192 | /26 | 62 | Marketing |
| Business Servers | 110.130.37.128 | 255.255.255.240 | /28 | 14 | Servers |
| Wireless Network | 110.130.37.144 | 255.255.255.240 | /28 | 14 | Wireless Devices |
| Router Links | 110.130.37.160-191 | Various /30 | /30 | 2 each | Inter-router |

#### IPv6 Subnets

| Network Name | IPv6 Prefix | Usage |
|--------------|-------------|-------|
| Business School | 2001:ABCD:F00:20::/64 | Business Network |
| IT Services | 2001:ABCD:F00:21::/64 | IT Department |
| Finance | 2001:ABCD:F00:22::/64 | Finance |
| Marketing | 2001:ABCD:F00:23::/64 | Marketing |
| Business Servers | 2001:ABCD:F00:24::/64 | Servers |
| Wireless | 2001:ABCD:F00:25::/64 | Wireless |

---

## INTER-CAMPUS CONNECTIVITY

### Connection Architecture

```
                    [WWW Server]
                          |
                    [Student 1 - R1]
                          |
                    [Student 1 - R4]
                       /      \
                      /        \
            [Student 2 - R1]  [Student 3 - R1]
```

### Routing Protocol: OSPF

- **Area 0 (Backbone):** All border and distribution routers
- **Area 1:** Student 1 internal networks
- **Area 2:** Student 2 internal networks
- **Area 3:** Student 3 internal networks

### Default Route

All border routers will have a default static route pointing to WWW server:
```
ip route 0.0.0.0 0.0.0.0 [WWW_Server_IP]
ipv6 route ::/0 [WWW_Server_IPv6]
```

---

## SECURITY IMPLEMENTATION

### Router Security
1. **Enable secret password** for privileged mode
2. **Console password** with login
3. **VTY lines** secured with SSH (no Telnet)
4. **Banner messages** for legal notices
5. **ACLs** to restrict management access

### Switch Security
1. **Port security** on access ports
2. **DHCP snooping** enabled
3. **Disable unused ports**
4. **Enable PortFast and BPDU Guard**
5. **Management VLAN** separate from user VLANs

### Wireless Security
1. **WPA2-PSK** encryption
2. **Strong passphrase** (minimum 12 characters)
3. **SSID broadcast** disabled (optional)
4. **MAC filtering** enabled

---

## REDUNDANCY FEATURES

1. **Multiple paths** between core routers
2. **HSRP/VRRP** for gateway redundancy (if supported)
3. **Spanning Tree Protocol** (RSTP) on switches
4. **Dual connections** from access to distribution layer
5. **Multiple links** to WWW server

---

## VLAN CONFIGURATION

### Student 1 VLANs
- VLAN 10: Administration
- VLAN 20: Engineering
- VLAN 30: Library
- VLAN 40: Student Services
- VLAN 50: Servers
- VLAN 60: Wireless
- VLAN 99: Management

### Student 2 VLANs
- VLAN 110: Medical School
- VLAN 120: Research Lab
- VLAN 130: Hospital Wing
- VLAN 140: Medical Admin
- VLAN 150: Medical Servers
- VLAN 160: Wireless
- VLAN 199: Management

### Student 3 VLANs
- VLAN 210: Business School
- VLAN 220: IT Services
- VLAN 230: Finance
- VLAN 240: Marketing
- VLAN 250: Business Servers
- VLAN 260: Wireless
- VLAN 299: Management

---

## DNS CONFIGURATION

Each campus will have its own DNS server with:
- Forward lookup zones for local domain
- Reverse lookup zones
- Forwarders pointing to WWW server DNS

**Domains:**
- Student 1: main.techvarsity.edu
- Student 2: medical.techvarsity.edu
- Student 3: business.techvarsity.edu

---

## TESTING CHECKLIST

### Connectivity Tests
- [ ] Ping between devices in same VLAN
- [ ] Ping between devices in different VLANs (same campus)
- [ ] Ping between campuses (Student 1 ↔ Student 2)
- [ ] Ping between campuses (Student 1 ↔ Student 3)
- [ ] Ping between campuses (Student 2 ↔ Student 3)
- [ ] Ping to WWW server from all campuses
- [ ] IPv6 connectivity tests (all above)

### Service Tests
- [ ] DNS resolution working
- [ ] Web server accessible
- [ ] Wireless devices can connect
- [ ] Wireless devices can access wired network

### Redundancy Tests
- [ ] Disable one link, verify alternate path works
- [ ] Spanning Tree convergence
- [ ] OSPF route convergence

### Security Tests
- [ ] Cannot telnet to routers (SSH only)
- [ ] Port security triggers on violation
- [ ] Wireless requires authentication

---

This documentation provides the complete design framework. The next document will contain detailed configuration commands for implementation.
