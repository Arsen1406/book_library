from rentals.models import Rentals


def search_date_return_book(pk: int):
    list_rentals = Rentals.objects.filter(books__id__in=[pk])
    obj = None
    for rentals in list_rentals:
        if obj is None:
            obj = rentals
            continue
        if rentals.return_date < obj.return_date:
            obj = rentals
    return obj
