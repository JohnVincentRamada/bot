from django.core.management.base import BaseCommand
from customadmin.models import Description
import json

class Command(BaseCommand):
    help = 'Upsert data from JSONL file to Description model'

    def handle(self, *args, **kwargs):
        jsonl_file_path = 'customadmin/data.jsonl'

        with open(jsonl_file_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                Description.objects.create(
                    title=data["Title"],
                    category=data["Category"],
                    answer=data["Answer"]
                )