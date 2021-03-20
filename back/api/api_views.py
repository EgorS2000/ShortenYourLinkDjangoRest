from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from ShortenYourLink.models import Link
from ShortenYourLinkDjangoRest.settings import app_dmn
from api.utils import (
     owner_check,
     short_link_info_creation,
     my_account_info,
     link_info,
     serialization
)
from api.serializers import (
    LinkAddSerializer,
    MyLinksViewSerializer,
    LinkCheckSerializer,
    LinkChangeSerializer,
    AddHashtagSerializer,
    LinksSerializer,
    AccountSerializer
)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id="Create new short link.",
        operation_description="Create new short link."
    )
)
class MainPage(CreateAPIView):
    serializer_class = LinkAddSerializer
    permissions = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if int(request.data['life_time']) <= 0:
            return Response(
                data='Link life time is less than zero',
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data['orig_link'].strip():
            return Response(
                data='Link is empty',
                status=status.HTTP_400_BAD_REQUEST
            )

        data, random_sequence, random_sequence_exist = \
            short_link_info_creation(request=self.request)
        if not random_sequence_exist:
            serialization(
                serializer=self.serializer_class,
                data=data,
                mode='create'
            )
        result = f'{app_dmn}{random_sequence}'

        return Response(data=result, status=status.HTTP_201_CREATED)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_id="List of user's links",
        operation_description="List of user's links"
    )
)
class MyLinks(ListAPIView):
    serializer_class = MyLinksViewSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        links = get_list_or_404(Link.objects.filter(
            link_owner=self.request.user.id
        ).order_by('creation_date').all())
        return links


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id="Return original link",
        operation_description="Return original link"
    )
)
class CheckLink(CreateAPIView):
    serializer_class = LinkCheckSerializer
    permissions = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.data['short_link'].strip():
            return Response(
                data='Short link is empty',
                status=status.HTTP_400_BAD_REQUEST
            )
        short_link_rand_sequence = str(request.data['short_link']) \
            .replace(f'{app_dmn}', '')
        orig_link = get_object_or_404(
            Link,
            random_sequence=short_link_rand_sequence
        ).orig_link
        return Response(orig_link, status=status.HTTP_200_OK)


@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_id="Change unique sequence of link",
        operation_description="Change unique sequence of link"
    )
)
class ChangeLink(UpdateAPIView):
    serializer_class = LinkChangeSerializer
    permissions = [IsAuthenticated]

    @owner_check
    def partial_update(self, request, *args, **kwargs):
        short_link, new_idx = \
            request.data['short_link'], request.data['new_idx']
        short_link_rand_sequence = str(short_link).replace(f'{app_dmn}', '')

        if not short_link.strip():
            return Response(
                data='Short link is empty',
                status=status.HTTP_400_BAD_REQUEST
            )
        if not new_idx.strip():
            return Response(
                data='New identifier is empty',
                status=status.HTTP_400_BAD_REQUEST
            )
        if Link.objects.filter(random_sequence=new_idx).exists():
            return Response(
                data='Identifier is already in use',
                status=status.HTTP_400_BAD_REQUEST
            )

        short_link = get_object_or_404(
            Link,
            random_sequence=short_link_rand_sequence
        )
        rand_seq = {"random_sequence": new_idx}

        serializer = serialization(
            serializer=self.serializer_class,
            data=rand_seq,
            mode='update',
            instance=short_link
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_id="Link deactivation",
        operation_description="List of user's links"
    )
)
class DeactivateLink(DestroyAPIView):
    permissions = [IsAuthenticated]

    @owner_check
    def destroy(self, request, *args, **kwargs):
        short_link_rand_sequence = request.data['short_link'] \
            .replace(f'{app_dmn}', '')
        short_link = get_object_or_404(
            Link,
            random_sequence=short_link_rand_sequence
        )
        short_link.delete()

        return Response(
            data={"message": 'Link deleted successfully'},
            status=status.HTTP_200_OK
        )


@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_id="Add hashtag to short link",
        operation_description="Add hashtag to short link"
    )
)
class AddHashtag(UpdateAPIView):
    serializer_class = AddHashtagSerializer
    permissions = [IsAuthenticated]

    @owner_check
    def partial_update(self, request, *args, **kwargs):
        if not request.data['link_tag'].strip():
            return Response(
                data="Link tag is empty",
                status=status.HTTP_400_BAD_REQUEST
            )
        link = get_object_or_404(
            Link,
            random_sequence=request.data['short_link'].replace(f'{app_dmn}', '')
        )
        data = {"link_tag": request.data['link_tag']}
        serialization(
            serializer=self.serializer_class,
            data=data,
            mode='update',
            instance=link
        )

        return Response(
            data={"message": 'Hashtag successfully added'},
            status=status.HTTP_200_OK
        )


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_id="User's account info",
        operation_description="User's account info"
    )
)
class MyAccount(ListAPIView):
    serializer_class = AccountSerializer
    permissions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = serialization(
            serializer=self.serializer_class,
            data=my_account_info(request),
            mode='get'
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id="Statistic of link",
        operation_description="Statistic of link"
    )
)
class LinkInfo(CreateAPIView):
    serializer_class = LinksSerializer
    permissions = [IsAuthenticated]

    @owner_check
    def post(self, request, *args, **kwargs):
        result = link_info(request)
        serializer = serialization(
            serializer=self.serializer_class,
            data=result,
            mode='post'
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
