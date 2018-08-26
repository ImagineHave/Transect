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


def get_as_list_of_tuples():
    return [(f.value, f.label) for f in Frequency.objects.order_by('label')]


def get_by_label(label):
    return Frequency.objects(label=label).first()


def get_by_value(value):
    return Frequency.objects(value=value).first()
