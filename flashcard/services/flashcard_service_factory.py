from flashcard.services.iflashcardservice import IFlashcardService
from flashcard.services.phrase_flashcard_service import PhraseFlashcardService
from flashcard.services.verse_flashcard_service import VerseFlashcardService
from flashcard.services.word_flashcard_service import WordFlashcardService


class FlashcardServiceFactory:
    @staticmethod
    def get_service(service_name: str) -> IFlashcardService:
        for cls in IFlashcardService.__subclasses__():
            if cls.__name__.lower() == service_name.lower():
                return cls()
        raise ValueError(f"No such service: {service_name}")

    @staticmethod
    def list_services() -> list[str]:
        return [cls.service_type for cls in IFlashcardService.__subclasses__()]