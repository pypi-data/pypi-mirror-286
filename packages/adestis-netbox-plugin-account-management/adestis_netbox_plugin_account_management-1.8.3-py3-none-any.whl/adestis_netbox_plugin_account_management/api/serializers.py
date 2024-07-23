from .nested_serializer import *
from rest_framework import serializers
from adestis_netbox_plugin_account_management.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from tenancy.api.nested_serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *
from virtualization.api.nested_serializers import *

__all__ = (
    'LoginCredentialsSerializer',
    'SystemSerializer'
)

class LoginCredentialsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:logincredentials-detail'
    )

    system = NestedSystemSerializer(many=False,
                                    read_only=False,
                                    required=False)

    contact = NestedContactSerializer(many=False,
                                      read_only=False,
                                      required=False)

    class Meta:
        model = LoginCredentials
        fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'system', 'contact', 'created', 'last_updated', 'custom_field_data', 'logon_name', 'valid_from', 'valid_to', 'login_credentials_status', 'comments')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'url', 'system', 'contact', 'created', 'last_updated', 'custom_field_data', 'logon_name', 'valid_from', 'valid_to', 'login_credentials_status', 'comments')

class SystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:system-detail'
    )
    
    virtual_machine = NestedVirtualMachineSerializer(many=False,
                                                     read_only=False,
                                                     required=False)
    
    device = DeviceSerializer(many=False,
                              read_only=False,
                              required=False) 
    
    cluster_group = NestedClusterGroupSerializer(many=False,
                                                 read_only=False,
                                                 required=False)  
    
    cluster = NestedClusterSerializer(many=False,
                                      read_only=False,
                                      required=False)  
    
    tenant = TenantSerializer(many=False,
                             read_only=False,
                             required=False)
        
    group = TenantGroupSerializer(many=False,
                                  read_only=False,
                                  required=False)

    class Meta:
        model = System
        fields = ('id', 'url', 'display', 'name', 'system_url', 'system_status', 'device', 'virtual_machine', 'group', 'tenant', 'cluster_group', 'cluster', 'comments', 'tags',
                  'custom_fields', 'created', 'last_updated')
        brief_fields = ('id', 'url', 'display', 'name', 'system_url', 'system_status', 'device', 'virtual_machine', 'group', 'tenant', 'cluster_group', 'cluster', 'comments', 'tags',
                  'custom_fields', 'created', 'last_updated')
