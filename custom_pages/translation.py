from modeltranslation.translator import translator, TranslationOptions
from .models import ContainerPage, QAPage, AskedQuestion


class TranslatedContainerPage(TranslationOptions):
    fields = ()

translator.register(ContainerPage, TranslatedContainerPage)


class TranslatedAskedQuestion(TranslationOptions):
    fields = ("question", "answer")

translator.register(AskedQuestion, TranslatedAskedQuestion)


class TranslatedQAPage(TranslationOptions):
    fields = ("content",)

translator.register(QAPage, TranslatedQAPage)
