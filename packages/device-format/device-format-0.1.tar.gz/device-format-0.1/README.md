
# DEVICES FORMAT

  

This package is designed to generate regular expression formats based on device names. It simplifies the process of validating and parsing device identifiers by providing pre-defined regex patterns for various device types.

  

## Installation

  

You can install `devices-format` via pip. Use the following command:

  

```markdown

pip install devices-format

```

  

## Usage

  

Generate regular expression formats based on device names.

```markdown

from devices_format import Device

device = Device("OVF-AAAAAAATEY", "olt")
print(device.get_device_format())

```

  
  

## Supported Device Names

- OLT

- OTB

- CA1

- CA2

- FTSBS

- CPE