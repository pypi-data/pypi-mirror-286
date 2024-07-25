# SSSMS (Simple SMS Sending and Lookup Utility)

SSSMS is a Python-based command-line utility for sending SMS messages and looking up phone number information.

## Features

- Send SMS messages via email-to-SMS gateways
- Look up carrier information for phone numbers
- Proxy support for network requests
- Configurable caching for phone number lookups
- Secure storage of credentials

## Installation

You can install SSSMS using pip:

```
pip install sssms
```

## Usage

After installation, you can use SSSMS from the command line:

```
sssms [OPTIONS] COMMAND [ARGS]...
```

Available commands:

- `lookup`: Look up information for a phone number
- `send`: Send an SMS message
- `proxy`: Start or configure the proxy server

For more detailed information on each command, use:

```
sssms COMMAND --help
```

## Configuration

On first run, SSSMS will prompt you to create a configuration file. This file will store your email credentials, proxy settings, and other configurations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.