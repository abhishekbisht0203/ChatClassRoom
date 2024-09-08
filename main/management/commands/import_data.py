# myapp/management/commands/import_data.py

import json
from django.core.management.base import BaseCommand
from main.models import Subject, Topic, SubTopic

class Command(BaseCommand):
    help = 'Import subjects, topics, and subtopics from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as file:
            data = json.load(file)

        for subject_data in data['subjects']:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={'description': subject_data['description']}
            )
            for topic_data in subject_data['topics']:
                topic, created = Topic.objects.get_or_create(
                    subject=subject,
                    name=topic_data['name'],
                    defaults={'description': topic_data['description']}
                )
                for subtopic_data in topic_data['subtopics']:
                    SubTopic.objects.get_or_create(
                        topic=topic,
                        name=subtopic_data['name'],
                        defaults={'description': subtopic_data['description']}
                    )

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
