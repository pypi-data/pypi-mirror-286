from blib import Date
from collections.abc import Sequence


CODE_REDIRECT: str = "urn:ietf:wg:oauth:2.0:oob"


class ApiDate(Date):
	"""
		``Date`` class for API objects
	"""

	FORMAT: str = "%Y-%m-%dT%H:%M:%S.%zZ"
	ALT_FORMATS: Sequence[str] = (
		"%Y-%m-%dT%H:%M:%SZ",
		"%Y-%m-%d"
	)
