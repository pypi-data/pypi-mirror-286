from typing import Dict, List, Optional, Type, Union

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer


class BaseMixin:
    model: Type[Model]
    context: Optional[Dict[str, any]] = None
    serializer_save: Optional[Dict[str, any]] = None
    select_related: Optional[List[str]] = None
    prefetch_related: Optional[List[str]] = None
    enable_cache: Optional[bool] = False
    cache_duration: Optional[int] = None
    order_by: Optional[List[str]] = None
    query_params: Optional[Dict] = None

    def __init__(self) -> None:
        if self.enable_cache and not self.cache_duration:
            raise ImproperlyConfigured(
                "if enable cache is set to True you must define the cache duration , example 60 * 60 "
            )

    @method_decorator(cache_page(cache_duration))
    @method_decorator(vary_on_cookie)
    def cached_get(
        self, request: Request, serializer, pk=None, *args, **kwargs
    ) -> Response:
        return self.get_response(
            serializer, self.get_queryset(pk) if pk else self.get_queryset()
        )

    @staticmethod
    def get_response(serializer_klass, queryset) -> Response:
        return Response({"status": "Success", "data": serializer_klass(queryset).data})


class DjeasyListCreateAPI(BaseMixin, ListCreateAPIView):
    create_serializer_class: Type[BaseSerializer]
    list_serializer_class: Type[BaseSerializer]

    def get_create_serializer(self, data: Dict[str, any]) -> BaseSerializer:
        return self.create_serializer_class(data=data)

    def get_queryset(self) -> Model:
        queryset = super().get_queryset()
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        if self.prefetch_related:
            queryset = queryset.prefetch_related(*self.prefetch_related)
        if self.query_params:
            reverse_base = {v: k for k, v in self.query_params.items()}
            queryset = queryset.filter(
                **{
                    reverse_base[param_key]: param_value[0]
                    for param_key, param_value in dict(
                        self.request.query_params
                    ).items()
                    if param_key in reverse_base
                }
            )

        return queryset.order_by(*self.order_by) if self.order_by else queryset

    def get_list_serializer(self, instance: Model) -> BaseSerializer:
        return (
            self.list_serializer_class(instance, context=self.context, many=True)
            if self.context
            else self.list_serializer_class(instance, many=True)
        )

    def list(self, request: Request, *args, **kwargs) -> Response:
        if self.enable_cache:
            return self.cached_get(request, self.get_list_serializer, *args, **kwargs)
        return self.get_response(self.get_list_serializer, self.get_queryset())

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_create_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            (
                serializer.save(**self.serializer_save)
                if self.serializer_save
                else serializer.save()
            )
            return Response({"status": "Success", "data": serializer.data})
        return Response({"status": "Failure", "data": serializer.errors})


class DjeasyRetrieveUpdateAPI(BaseMixin, RetrieveUpdateDestroyAPIView):
    retrieve_serializer_class: Type[BaseSerializer]
    update_serializer_class: Type[BaseSerializer]
    cache_duration: Optional[int] = None

    def get_retrieve_serializer(self, instance: Model) -> BaseSerializer:
        return (
            self.retrieve_serializer_class(instance, context=self.context)
            if self.context
            else self.retrieve_serializer_class(instance)
        )

    def get_update_serializer(
        self, instance: Model, data: Dict[str, any]
    ) -> BaseSerializer:
        return self.update_serializer_class(instance, data=data)

    def get_queryset(self, pk: Union[int, str]) -> Model:
        queryset = super().get_queryset()
        if self.select_related:
            queryset = self.model.objects.select_related(*self.select_related)
        if self.prefetch_related:
            queryset = self.model.objects.prefetch_related(*self.prefetch_related)
        else:
            queryset = self.model
        return get_object_or_404(queryset, pk=pk)

    def retrieve(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        if self.enable_cache:
            return self.cached_get(
                request, self.get_retrieve_serializer, pk, *args, **kwargs
            )
        return self.get_response(self.get_retrieve_serializer, self.get_queryset(pk))

    def update(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        instance = self.get_queryset(pk)
        serializer = self.get_update_serializer(instance, request.data)
        if serializer.is_valid():
            (
                serializer.save(**self.serializer_save)
                if self.serializer_save
                else serializer.save()
            )
            return Response({"status": "Success", "data": serializer.data})
        return Response({"status": "Failure", "data": serializer.errors})

    def delete(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        self.model.objects.filter(id=pk).delete()
        return Response({"status": "Success", "data": "Deleted Successfully"})
