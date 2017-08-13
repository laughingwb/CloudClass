from tutor.models import Tutor


def is_tutor(user):
    tutor = Tutor.objects.filter(user=user).first()

    if tutor:
        return True
    else:
        return False