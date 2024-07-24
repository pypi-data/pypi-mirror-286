<p align="center">
  Wraps the default Django SMTP Email Backend with trace instrumentation to the OpenTelemetry.
</p>

<p align="center">
<a href="https://pypi.org/project/django-otel-smtp-backend/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/django-otel-smtp-backend"/></a>
<a href="https://github.com/inventare/django-otel-smtp-backend/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/inventare/django-otel-smtp-backend"/></a>
</p>

## Description

This small package provides a wrapper for the default `django.core.mail.backends.smtp.EmailBackend` adapter to provide better tracing instrumentation for OpenTelemetry.

## Dependencies

- django >= 4.2
- opentelemetry-api

## Usage

### Installation

Install, from PyPI, using your package manager:

```sh
pip install django-otel-smtp-backend
```

### Configuration

Change the `EMAIL_BACKEND` field on `settings.py` file:

```python
EMAIL_BACKEND = "django_otel_smtp_backend.backend.EmailBackend"
EMAIL_HOST = ...
EMAIL_USE_TLS = ...
EMAIL_PORT = ...
EMAIL_USE_SSL = ...
EMAIL_HOST_USER = ...
EMAIL_HOST_PASSWORD = ...
```

The configuration of `OpenTelemetry` is not a subject of this readme.

## OpenTelemetry

The traces captured from the `EmailBackend` is structured as shown below (the times was taken from a real example):

```
  - send_messages (2.89s)
  | - open (1.55s)
  | - send_message_item (1.17s)
  | - close (168.43ms)
```

The `send_messages()` method from the `BaseEmailBackend` receives various e-mails and, in SMTP backend, send one by one using a for-iterator ([reference](https://github.com/django/django/blob/main/django/core/mail/backends/smtp.py#L120)). The `send_messages` span is opened when the `send_messages()` method is called, the `open` span is opened when the connection is opened and `close` span is opened when the connection is closed. The `send_message_item` span is opened when each e-mail is sent using the SMTP connection.

### Span Attributes

#### send_messages

| attribute         | description                                                |
| ----------------- | ---------------------------------------------------------- |
| raised            | indicate if the send_messages() method raises a exception. |
| stack             | stack trace of the raised exception (when raised=True).    |

#### open

| attribute               | description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| connection_already_open | indicate if the connection is already opened when open() is called. |
| connection_opened       | indicate if the connection is opened.                               |
| fail_silently           | indicate if the used value of fail_silently property.               |
| raised                  | indicate if the open() method raises a exception.                   |
| stack                   | stack trace of the raised exception (when raised=True).             |

#### send_message_item

| attribute               | description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| from_email              | the origin email.                                                   |
| recipients              | the destination email's.                                            |
| sent                    | indicate if the email is sent.                                      |
| raised                  | indicate if the method raises a exception.                          |
| stack                   | stack trace of the raised exception (when raised=True).             |

#### close

| attribute               | description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| has_connection          | indicate if the connection is opened when call close().             |
| raised                  | indicate if the open() method raises a exception.                   |
| stack                   | stack trace of the raised exception (when raised=True).             |


