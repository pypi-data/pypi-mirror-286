from blib import Date
from collections.abc import Sequence
from datetime import datetime
from typing import Self


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


	@classmethod
	def parse(cls: type[Self], date: datetime | str | int | float, try_iso: bool = True) -> Self:
		if isinstance(date, str):
			date = date.split(".", 1)[0]

		return super().parse(date)
