from traceback import TracebackException

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as EmailBackendBase
from django.core.mail.message import sanitize_address
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class EmailBackend(EmailBackendBase):
    """
    A wrapper that instruments the default
    `django.core.mail.backends.smtp.EmailBackend`
    with open-telemetry.
    """

    def _open(self) -> bool:
        span = trace.get_current_span()

        already_connected = bool(self.connection)

        span.set_attribute("fail_silently", self.fail_silently)
        span.set_attribute("connection_already_open", already_connected)
        span.set_attribute("raised", False)
        span.set_attribute("stack", "")

        try:
            opened = super().open()
            span.set_attribute("connection_opened", opened)
        except OSError as e:
            opened = False
            span.set_attribute("connection_opened", opened)

            if not self.fail_silently:
                stacktrace = "".join(TracebackException.from_exception(e).format())
                span.set_attribute("raised", True)
                span.set_attribute("stack", stacktrace)
                raise e

        return opened

    def _close(self):
        span = trace.get_current_span()

        has_connection = self.connection is not None

        span.set_attribute("has_connection", has_connection)
        span.set_attribute("raised", False)
        span.set_attribute("stack", "")

        try:
            super().close()
        except Exception as e:
            if not self.fail_silently:
                stacktrace = "".join(TracebackException.from_exception(e).format())
                span.set_attribute("raised", True)
                span.set_attribute("stack", stacktrace)
                raise e

    def _send_messages(self, email_messages):
        span = trace.get_current_span()

        span.set_attribute("raised", False)
        span.set_attribute("stack", "")

        sent_messages = 0
        try:
            sent_messages = super().send_messages(email_messages)
        except Exception as e:
            stacktrace = "".join(TracebackException.from_exception(e).format())
            span.set_attribute("raised", True)
            span.set_attribute("stack", stacktrace)
            raise e
        finally:
            span.set_attribute("sent_messages", sent_messages)

    def _send(self, email_message):
        with tracer.start_as_current_span("send_message_item"):
            span = trace.get_current_span()

            encoding = email_message.encoding or settings.DEFAULT_CHARSET
            from_email = sanitize_address(email_message.from_email, encoding)
            span.set_attribute("from_email", from_email)
            span.set_attribute("stack", "")
            span.set_attribute("raised", False)

            if not email_message.recipients():
                span.set_attribute("recipients", "")
                span.set_attribute("sent", False)
                return False

            recipients = [
                sanitize_address(addr, encoding) for addr in email_message.recipients()
            ]
            span.set_attribute("recipients", ",".join(recipients))
            try:
                is_sent = super()._send(email_message)
                span.set_attribute("sent", is_sent)
            except Exception as e:
                stacktrace = "".join(TracebackException.from_exception(e).format())
                span.set_attribute("sent", False)
                span.set_attribute("raised", True)
                span.set_attribute("stack", stacktrace)

    def open(self) -> bool:
        with tracer.start_as_current_span("open"):
            return self._open()

    def close(self):
        with tracer.start_as_current_span("close"):
            self._close()

    def send_messages(self, email_messages):
        with tracer.start_as_current_span("send_messages"):
            return self._send_messages(email_messages)
