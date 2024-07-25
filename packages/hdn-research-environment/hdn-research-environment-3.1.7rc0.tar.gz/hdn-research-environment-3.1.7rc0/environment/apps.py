from django.apps import AppConfig
from console.navbar import CONSOLE_NAV_MENU, NavLink, NavSubmenu
from django.utils.translation import gettext_lazy as _


class EnvironmentConfig(AppConfig):
    name = "environment"

    def ready(self):
        import environment.signals
        self.add_nav_items()


    def add_nav_items(self):
        new_nav_items = [
            NavSubmenu(_('Power Users'), 'cloud_groups', 'book', [
                NavLink(_('User Panel'), 'cloud_groups'),
                NavLink(_('Group Management'), 'cloud_groups_management'),
                NavLink(_('Group Creation'), 'create_cloud_group'),
            ]),
            NavSubmenu(_('Monitor'), 'datasets_monitoring', 'chart-line', [
                NavLink(_('Dataset Total Usage Time'), 'get_datasets_monitoring_data'),
            ]),
        ]

        CONSOLE_NAV_MENU.items.extend(new_nav_items)