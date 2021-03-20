from rest_framework import serializers

from ShortenYourLink.models import Link


class LinkAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'orig_link',
            'domain_name',
            'random_sequence',
            'link_owner',
            'life_time_end'
        ]


class MyLinksViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class LinkCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['orig_link']


class LinkChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['random_sequence']


class AddHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['link_tag']


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text="Username",
    )
    registration_date = serializers.DateTimeField(
        help_text="Account registration date",
    )
    last_login_date = serializers.DateTimeField(
        help_text="Last login date",
    )
    status = serializers.BooleanField(
        help_text="Active/Not active",
    )
    is_admin = serializers.BooleanField(
        help_text="Admin/Not admin",
    )
    trans_all_time = serializers.IntegerField(
        help_text="The number of clicks on links for all time",
    )
    trans_last_day = serializers.IntegerField(
        help_text="The number of clicks on links for last day",
    )
    trans_last_week = serializers.IntegerField(
        help_text="The number of clicks on links for last week",
    )
    trans_last_30_days = serializers.IntegerField(
        help_text="The number of clicks on links for last 30 days",
    )
    trans_last_year = serializers.IntegerField(
        help_text="The number of clicks on links for last year",
    )
    result_domain_dict = serializers.ListField(
        help_text="List of domains of all original links",
    )


class LinksSerializer(serializers.Serializer):
    link = serializers.URLField(
        help_text="Original link",
    )
    random_sequence = serializers.IntegerField(
        help_text="link identifier",
    )
    owner = serializers.IntegerField(
        help_text="Owner of link",
    )
    link_trans_all_time = serializers.IntegerField(
        help_text="The number of clicks on link for all time",
    )
    link_trans_last_day = serializers.IntegerField(
        help_text="The number of clicks on link for last day",
    )
    link_trans_last_week = serializers.IntegerField(
        help_text="The number of clicks on link for last week",
    )
    link_trans_last_30_days = serializers.IntegerField(
        help_text="The number of clicks on link for last 30 days",
    )
    link_trans_last_year = serializers.IntegerField(
        help_text="The number of clicks on link for last year",
    )
