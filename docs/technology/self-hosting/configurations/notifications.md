# Email Notifications

Corridor provides an option to send email notifications to the user on their registered email id when
an event occurs on the platform (e.g. completion of simulation, approval request for an object).

The different events for which notifications are triggered on the Platform:

- Completion or failure of job run
- Workflow Status change of an object
- Review status changes or comments added during approval process
- Sharing of an object

!!! note

    The user cannot customize which notifications will be sent as email.

## Configuration

The email notifications can be configured in `api_config.py` file with the parameter: `NOTIFICATION_PROVIDERS`.
The value should be a dictionary with the key being `email`.
The value for `email` should be a dictionary again with the email configuration details.
The email configuration details include:

- `from`: The email id from which the notifications are to be sent
- `username`: Username corresponding to the email id
- `password`: The password for the email id
- `host`: The host of the SMTP server
- `port`: The port number to use
- `ssl`: Should ssl be used
- `html`: Should the email be parsed as an HTML file

### Example

```python
NOTIFICATION_PROVIDERS = {
    'email': {
        'from': 'user@example.com',
        'username': 'user',
        'password': 'password',
        'host': 'smtp.server.com',
        'port': 465,
        'ssl': True,
        'html': True,
    },
}
```
