from copy import copy
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from newsletters.models import Newsletter, Tag
from newsletters.permissions import CustomPermissions
from newsletters.serializers import NewsletterSerializer, TagSerializer, NewsletterCreateSerializer
from accounts.tasks import send_email_subscribe, send_email_unsubscribe, send_email, send_email_share, \
    send_notice_to_publish


class NewsletterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all().order_by('id')
    serializer_class = NewsletterSerializer
    permission_classes = (CustomPermissions,)

    def get_queryset(self):
        try:
            data = {}
            for i in self.request.query_params:
                data[i] = self.request.query_params[i]
            return self.queryset.filter(**data)
        except KeyError:
            return self.queryset

# Admin -------------------------------------
    def create(self, request, *args, **kwargs):
        data = copy(self.request.data)
        data['created_by'] = self.request.user.id
        serialized = NewsletterCreateSerializer(data=data)

        if not serialized.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serialized.errors
            )

        serialized.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized.data
        )

    @action(methods=['GET', 'POST'], detail=False)
    def tags(self, request):

        if request.method == 'GET':
            queryset = Tag.objects.all()
            serialized = TagSerializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method == 'POST':
            new_tag = request.data
            new_tag_serialized = TagSerializer(data=new_tag)
            new_tag_serialized.is_valid()
            new_tag_serialized.save()
            return Response(status=status.HTTP_201_CREATED, data=new_tag_serialized.data)

    @action(methods=['POST'], detail=True)
    def share(self, request, pk=None):
        newsletter = self.get_object()
        if request.user == newsletter.created_by and newsletter.published:
            admins = User.objects.filter(is_staff=True)
            emails = []
            for i in admins.all():
                if not i == request.user:
                    emails.append(str(i.email))
            print(emails)
            send_email_share.apply_async(args=[request.user.email, emails, newsletter.name])
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def publish(self, request, pk=None):
        newsletter = self.get_object()
        print(request.user)
        if request.user == newsletter.created_by and len(newsletter.votes.all()) >= newsletter.target:
            newsletter.published = True
            newsletter.published_at = datetime.now()
            newsletter.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Users -------------------------------------------------------------
    @action(methods=['GET'], detail=False)
    def subscribed(self, request):
        if request.user.is_authenticated:
            subscriptions = request.user.subscriptions.all()
            subscriptions_serialized = NewsletterSerializer(subscriptions, many=True)
            return Response(status=status.HTTP_200_OK, data=subscriptions_serialized.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "Authentication credentials were not "
                                                                             "provided."})

    @action(methods=['POST'], detail=True)
    def vote(self, request, pk=None):
        newsletter = self.get_object()
        newsletter.votes.add(request.user)
        print(len(newsletter.votes.all()))
        if len(newsletter.votes.all()) >= newsletter.target:
            send_notice_to_publish.apply_async(args=[newsletter.created_by.email, newsletter.name])
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, pk=None):
        newsletter = self.get_object()
        if not request.user == newsletter.created_by:
            if len(newsletter.votes.all()) >= newsletter.target:
                newsletter.subscribers.add(request.user)
                send_email_subscribe.apply_async(args=[request.user.email, newsletter.name])
                send_email_datetime = datetime.now() + timedelta(days=newsletter.frequency)
                send_email.apply_async(args=[request.user.email, newsletter.name], eta=send_email_datetime)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def unsubscribe(self, request, pk=None):
        newsletter = self.get_object()
        if request.user in newsletter.subscribers.all():
            print(request.user.email, newsletter.name)
            newsletter.subscribers.remove(request.user)
            send_email_unsubscribe.apply_async(args=[request.user.email, newsletter.name])
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
