from mongoengine import (
    StringField, Document, DictField
    )


class Frequency(Document):
    label = StringField(max_length=200, required=True)
    value = DictField(required=True, places=0, default=0, min=0)


def create_standard_frequencies():
    Frequency(label='weekly', value={'weeks': 1}).save()
    Frequency(label='monthly', value={'months': 1}).save()
    Frequency(label='annually', value={'years': 1}).save()


def get_list():
    labels = []
    for frequency in Frequency.objects:
        labels.append(frequency.label)
    return labels


def get_by_label(label):
    return Frequency.objects(label=label).first()
