from .courses import courses

def total_duration():

    return sum(curso.duration for curso in courses)
