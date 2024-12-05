from abc import ABC, abstractmethod

class IFlashcardService(ABC):
    service_type = None

    @abstractmethod
    def get_request_types(self):
        pass

    @abstractmethod
    def get_id_options(self, user):
        pass

    @abstractmethod
    def get_juz_options(self, user):
        pass

    @abstractmethod
    def get_category_options(self, user):
        pass

    @abstractmethod
    def get_range_options(self, user):
        pass

    @abstractmethod
    def get_flashcards(self, flashcardset, amount, ):
        pass

    @abstractmethod
    def get_flashcards_by_category(self, flashcardset, amount, category):
        pass

    @abstractmethod
    def get_flashcards_by_juz(self, flashcardset, amount, juz_list):
        pass

    @abstractmethod
    def get_flashcards_by_ids(self, flashcardset, amount, id_list):
        pass

    @abstractmethod
    def get_flashcards_by_range(self, flashcardset, amount, start, end):
        pass
