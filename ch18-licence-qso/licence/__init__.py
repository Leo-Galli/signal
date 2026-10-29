"""Chapter 18 licence path helpers: calendar, quiz, cheat card, station ID, clubs."""

from licence.calendar import REQUIRED_CALENDAR_FIELDS, validate_calendar
from licence.cheat_card import REQUIRED_CHEAT_CARD_FIELDS, validate_cheat_card
from licence.clubs import REQUIRED_CLUBS_FIELDS, validate_clubs
from licence.phonetics import ITU_PHONETIC, spell_callsign
from licence.quiz import score_quiz, validate_quiz_doc
from licence.station_id import REQUIRED_STATION_ID_FIELDS, validate_station_id

__all__ = [
    "ITU_PHONETIC",
    "REQUIRED_CALENDAR_FIELDS",
    "REQUIRED_CHEAT_CARD_FIELDS",
    "REQUIRED_CLUBS_FIELDS",
    "REQUIRED_STATION_ID_FIELDS",
    "score_quiz",
    "spell_callsign",
    "validate_calendar",
    "validate_cheat_card",
    "validate_clubs",
    "validate_quiz_doc",
    "validate_station_id",
]
