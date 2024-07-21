import factory
from django.apps import apps
from django.conf import settings
from faker import Faker

from core.factories import CustomDjangoModelFactory
from product.factories.image import ProductImageFactory
from product.factories.review import ProductReviewFactory
from product.models.product import Product

fake = Faker()

available_languages = [lang["code"] for lang in settings.PARLER_LANGUAGES[settings.SITE_ID]]


class ProductTranslationFactory(factory.django.DjangoModelFactory):
    language_code = factory.Iterator(available_languages)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    master = factory.SubFactory("product.factories.product.ProductFactory")

    class Meta:
        model = apps.get_model("product", "ProductTranslation")
        django_get_or_create = ("language_code", "master")


class ProductFactory(CustomDjangoModelFactory):
    unique_model_fields = [
        ("slug", lambda: fake.slug()),
    ]

    product_code = factory.Faker("uuid4")
    category = factory.SubFactory("product.factories.category.ProductCategoryFactory")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    active = factory.Faker("boolean")
    stock = factory.Faker("random_int", min=0, max=100)
    discount_percent = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True, max_value=100)
    vat = factory.SubFactory("vat.factories.VatFactory")
    view_count = factory.Faker("random_int", min=0, max=1000)
    weight = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)

    class Meta:
        model = Product
        django_get_or_create = ("slug",)
        skip_postgeneration_save = True
        exclude = ("unique_model_fields", "num_images")

    num_images = factory.LazyAttribute(lambda o: 2)
    num_reviews = factory.LazyAttribute(lambda o: 2)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        num_images = kwargs.pop("num_images", 2)
        num_reviews = kwargs.pop("num_reviews", 2)
        instance = super()._create(model_class, *args, **kwargs)

        if "create" in kwargs and kwargs["create"]:
            if num_images > 0:
                images = ProductImageFactory.create_batch(num_images)
                instance.images.add(*images)
            if num_reviews > 0:
                reviews = ProductReviewFactory.create_batch(num_images)
                instance.reviews.add(*reviews)

        return instance

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        if not create:
            return

        translations = extracted or [
            ProductTranslationFactory(language_code=lang, master=self) for lang in available_languages
        ]

        for translation in translations:
            translation.master = self
            translation.save()
