import bluetooth
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print(nearby_devices)