from django.db import models
from core.models import BaseModel

class NetworkInterface(BaseModel):
    """Network Interface Card (NIC) statistics."""
    hostname = models.CharField(max_length=255, db_index=True)
    interface_name = models.CharField(max_length=50) # eth0, wlan0
    mac_address = models.CharField(max_length=17, blank=True)
    ipv4_address = models.GenericIPAddressField(null=True, blank=True)
    
    mtu = models.IntegerField(default=1500)
    speed_mbps = models.IntegerField(default=1000)
    
    status = models.CharField(max_length=20, default='up') # up, down

    class Meta:
        verbose_name = 'Network Interface'
        verbose_name_plural = 'Network Interfaces'
        unique_together = ['hostname', 'interface_name']

    def __str__(self):
        return f"{self.hostname}:{self.interface_name}"

class TrafficFlow(BaseModel):
    """Aggregated network traffic record (NetFlow/sFlow)."""
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    source_port = models.IntegerField()
    destination_port = models.IntegerField()
    protocol = models.CharField(max_length=10) # TCP, UDP, ICMP
    
    bytes_transferred = models.BigIntegerField(default=0)
    packets_transferred = models.IntegerField(default=0)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = 'Traffic Flow'
        verbose_name_plural = 'Traffic Flows'

    def __str__(self):
        return f"{self.source_ip}:{self.source_port} -> {self.destination_ip}:{self.destination_port}"

class FirewallRule(BaseModel):
    """Active Access Control List rule."""
    name = models.CharField(max_length=255)
    action = models.CharField(max_length=20, default='allow') # allow, deny
    
    source_cidr = models.CharField(max_length=50, default='0.0.0.0/0')
    destination_cidr = models.CharField(max_length=50, default='0.0.0.0/0')
    port_range = models.CharField(max_length=50, default='any')
    protocol = models.CharField(max_length=20, default='any')
    
    priority = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Firewall Rule'
        verbose_name_plural = 'Firewall Rules'

    def __str__(self):
        return f"{self.name} ({self.action})"

class VPNConnection(BaseModel):
    """Site-to-Site or Client VPN funnel."""
    connection_id = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, default='site-to-site')
    remote_gateway = models.GenericIPAddressField(null=True)
    
    tunnel_status = models.CharField(max_length=20, default='down')
    bandwidth_mbps = models.FloatField(default=0.0)
    
    connected_check_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'VPN Connection'
        verbose_name_plural = 'VPN Connections'

    def __str__(self):
        return f"{self.connection_id} ({self.tunnel_status})"
