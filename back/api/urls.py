from django.urls import path

from api.api_views import (
    MyLinks,
    MainPage,
    CheckLink,
    ChangeLink,
    DeactivateLink,
    AddHashtag,
    MyAccount,
    LinkInfo
)

urlpatterns = [
    path(
        "create_link/",
        MainPage.as_view(),
        name='create_link'
    ),
    path(
        "my_links/",
        MyLinks.as_view(),
        name='my_links'
    ),
    path(
        "check_link/",
        CheckLink.as_view(),
        name='check_link'
    ),
    path(
        "change_link/",
        ChangeLink.as_view(),
        name='change_link'
    ),
    path(
        "deactivate_link/",
        DeactivateLink.as_view(),
        name='deactivate_link'
    ),
    path(
        "my_links/more/add_hashtag/",
        AddHashtag.as_view(),
        name='add_hashtag'
    ),
    path(
        "my_account/",
        MyAccount.as_view(),
        name='my_account'
    ),
    path(
        "my_links/more/",
        LinkInfo.as_view(),
        name='link_info'
    ),
]
