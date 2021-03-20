import secrets
import string
from datetime import datetime, timedelta

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ShortenYourLink.models import Link, Transitions
from ShortenYourLinkDjangoRest.settings import app_dmn


def owner_check(func):
    def wrapper(self, request, *args, **kwargs):
        if 'short_link' in request.data:
            short_link_rand_sequence = \
                str(request.data['short_link']).replace(f'{app_dmn}', '')

            if not Link.objects.filter(
                    random_sequence=short_link_rand_sequence) \
                    .exists():
                return Response(
                    data={"message": 'There are no link like this'},
                    status=403
                )

            if not request.user.id == Link.objects \
                    .filter(random_sequence=short_link_rand_sequence) \
                    .first().link_owner_id:
                return Response(
                    data={"message": 'You are not owner of this link'},
                    status=403
                )

        return Response(func(self, request, *args, **kwargs).data, status=200)

    return wrapper


def short_link_info_creation(request):
    orig_link = request.data['orig_link']
    life_time_end = datetime.utcnow() + timedelta(
        days=int(request.data['life_time']))
    domain_name = orig_link[int(orig_link.find('/')) + 2:]
    domain_name = domain_name[:int(domain_name.find('/'))].replace('www.', '')
    link_owner = request.user.id

    random_sequence_exist = False
    if Link.objects.filter(orig_link=orig_link,
                           link_owner=link_owner).exists():
        random_sequence = Link.objects.filter(orig_link=orig_link) \
            .first().random_sequence
        random_sequence_exist = True
    else:
        random_sequence = ''.join(secrets.choice(
            string.ascii_lowercase + string.digits)
                                  for _ in range(8))

    return (
        {"orig_link": orig_link,
         "domain_name": domain_name,
         "random_sequence": random_sequence,
         "link_owner": link_owner,
         "life_time_end": life_time_end},
        random_sequence,
        random_sequence_exist
    )


def short_link_change(request, serializer):
    orig_link = request.data['short_link']
    new_idx = request.data['new_idx']

    if Link.objects.filter(random_sequence=new_idx).exists():
        return Response(
            data={"message": 'Identifier is already in use'},
            status=400
        )

    short_link = get_object_or_404(
        Link,
        random_sequence=str(orig_link).replace(f'{app_dmn}', '')
    )
    serializer = serialization(serializer=serializer,
                               data={"random_sequence": new_idx},
                               mode='update',
                               instance=short_link)

    return serializer.data


def my_account_info(request):
    user = request.user
    username, registration_date, last_login_date, is_admin, status = \
        user.username, \
        user.date_joined, \
        user.last_login, \
        user.is_staff, \
        user.is_active
    transitions = Transitions.objects.filter(owner_id=request.user.id).all()
    trans_all_time = transitions.count()
    trans_last_day, trans_last_week, trans_last_30_days, trans_last_year = \
        transitions_counting(transitions)
    result_domain_dict = make_domains_list(request)
    result = {
        "username": username,
        "registration_date": registration_date,
        "last_login_date": last_login_date,
        "status": status, "is_admin": is_admin,
        "trans_all_time": trans_all_time,
        "trans_last_day": trans_last_day,
        "trans_last_week": trans_last_week,
        "trans_last_30_days": trans_last_30_days,
        "trans_last_year": trans_last_year,
        "result_domain_dict": result_domain_dict
    }
    return result


def link_info(request):
    owner = request.user.username
    link = get_object_or_404(
        Link,
        random_sequence=str(request.data['short_link'])
        .replace(f'{app_dmn}', ''))
    transitions = Transitions.objects.filter(link_id=link.id).all()
    link_trans_all_time = transitions.count()
    link_trans_last_day, link_trans_last_week, link_trans_last_30_days, link_trans_last_year \
        = transitions_counting(transitions)
    result = {
        "orig_link": link.orig_link,
        "random_sequence": link.random_sequence,
        "owner": owner,
        "link_trans_all_time": link_trans_all_time,
        "link_trans_last_day": link_trans_last_day,
        "link_trans_last_week": link_trans_last_week,
        "link_trans_last_30_days": link_trans_last_30_days,
        "link_trans_last_year": link_trans_last_year
    }

    return result


def make_domains_list(request):
    domains = []

    for domain in Link.objects.filter(link_owner=request.user.id).all():
        domains.append(domain.domain_name)

    domains_count = []

    for domain in domains:
        domains_count.append(Link.objects.filter(domain_name=domain).count())

    result_domain_list = dict(zip(domains, domains_count))

    return result_domain_list


def transitions_counting(transitions):
    link_trans_last_day = 0
    link_trans_last_week = 0
    link_trans_last_30_days = 0
    link_trans_last_year = 0

    days_count = [1, 7, 30, 365]

    for trans in transitions:
        if datetime.now() - trans.trans_time < timedelta(days=days_count[0]):
            link_trans_last_day += 1
        if datetime.now() - trans.trans_time < timedelta(days=days_count[1]):
            link_trans_last_week += 1
        if datetime.now() - trans.trans_time < timedelta(days=days_count[2]):
            link_trans_last_30_days += 1
        if datetime.now() - trans.trans_time < timedelta(days=days_count[3]):
            link_trans_last_year += 1

    return link_trans_last_day, link_trans_last_week, link_trans_last_30_days, link_trans_last_year


def serialization(**kwargs):
    serializer = kwargs.get('serializer')

    if kwargs.get('mode') == 'create' or 'get':
        serialized_data = serializer(data=kwargs.get('data'))

    if kwargs.get('mode') == 'update':
        serialized_data = serializer(
            instance=kwargs.get('instance'),
            data=kwargs.get('data')
        )

    if serialized_data.is_valid():
        serialized_data.save()

    return serialized_data
