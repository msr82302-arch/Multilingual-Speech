class TTSProviderError(Exception):
    """
    Domain-level error raised when a TTS provider fails.
    Views and other callers can catch this without depending on
    the underlying provider SDK.
    """


class BaseTTS:
    """
    Base interface for TTS providers.
    """

    def synthesize(self, text: str, **kwargs) -> bytes:
        """
        Convert text to audio bytes.
        Implementations should raise TTSProviderError on provider failures.
        """
        raise NotImplementedError
