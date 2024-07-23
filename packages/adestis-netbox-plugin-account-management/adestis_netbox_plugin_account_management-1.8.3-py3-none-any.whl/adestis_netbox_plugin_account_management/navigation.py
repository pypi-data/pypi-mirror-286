from netbox.plugins import PluginMenuItem, PluginMenuButton
from netbox.choices import ButtonColorChoices

menu_items = [
        PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:system_list',
        link_text='Systems',
        permissions=["adestis_netbox_plugin_account_management.system_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_plugin_account_management:system_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_plugin_account_management.system_add"]),
        )
    ),
    PluginMenuItem(
        link='plugins:adestis_netbox_plugin_account_management:logincredentials_list',
        link_text='Login Credentials',
        permissions=["adestis_netbox_plugin_account_management.logincredentials_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_plugin_account_management:logincredentials_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_plugin_account_management.logincredentials_add"]),
        )
    )
]