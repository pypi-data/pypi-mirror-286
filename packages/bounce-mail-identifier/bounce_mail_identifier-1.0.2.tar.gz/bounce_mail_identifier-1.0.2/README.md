
# Bounce Mail Identifier

A Python package to identify and handle bounced emails. This package allows you to fetch bounce emails from an IMAP server, extract sender and failed recipient information, and save the data to an Excel file.

## Features

- Fetches bounce emails from an IMAP server.
- Extracts sender address and failed recipient email addresses.
- Saves bounce information to an Excel file.
- Easy to integrate and use.

## Supported Email Providers

- Gmail
- Microsoft Outlook
- Yahoo Mail
- Any other IMAP-compatible email provider


## Installation

To install this package, use pip:

```sh
pip install bounce-mail-identifier
```

## Usage

### Command Line

After installing, you can use the package from the command line.

```sh
fetch_bounces
```

### As a Module

You can also use it as a module in your Python code.

```python
from bounce_mail_identifier.bounce_mail_handler import fetch_bounce_emails, save_bounces_to_excel

# Provide your email credentials and server details
username = 'your-email@example.com'
app_password = 'your-app-password'
imap_server = 'imap.example.com'

# Fetch bounce emails
bounces = fetch_bounce_emails(username, app_password, imap_server)

# Save the bounces to an Excel file
save_bounces_to_excel(bounces, 'bounces.xlsx')
```

## Dependencies

- pandas
- openpyxl

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Around With Us - [mscrabe@gmail.com](mailto:mscrabe@gmail.com)

## Acknowledgments

- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [imaplib](https://docs.python.org/3/library/imaplib.html)
- [email](https://docs.python.org/3/library/email.html)

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.
