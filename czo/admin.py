from django.contrib import admin
from .models import *

# registering So we can access all data from Admin account,
admin.site.register(Node),
admin.site.register(Gateway),
admin.site.register(GatewayStats),
admin.site.register(NodeStats),
