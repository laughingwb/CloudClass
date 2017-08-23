from tutor.models import Teacher


def is_tutor(user):
    tutor = Teacher.objects.filter(user=user).first()

    if tutor:
        return True
    else:
        return False