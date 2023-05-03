from django.contrib import admin

from .models import IceCreamTub, Flavor


class IceCreamTubAdmin(admin.ModelAdmin):
    list_display = ("flavor", "scoops_available", "is_empty", "filling_rate")
    actions = ["refill_tubs"]

    def refill_tubs(self, request, queryset):
        for tub in queryset:
            tub.refill()
        self.message_user(request, "Selected tubs have been refilled.")

    refill_tubs.short_description = "Refill selected tubs"


admin.site.register(IceCreamTub, IceCreamTubAdmin)
admin.site.register(Flavor)
