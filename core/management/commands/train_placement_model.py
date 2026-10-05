from django.core.management.base import BaseCommand
from core.ml_models import train_and_save_model


class Command(BaseCommand):
    help = "Train and save the placement prediction model"

    def handle(self, *args, **kwargs):
        model, accuracy = train_and_save_model()

        self.stdout.write(
            self.style.SUCCESS(
                f"Placement model trained successfully. Accuracy: {accuracy * 100:.2f}%"
            )
        )