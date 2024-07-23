from django.core.management.base import BaseCommand
from artd_customer.models import CustomerGroup
from artd_partner.models import Partner

CUSTOMER_GROUPS = [
    {
        "group_code": "new",
        "group_name": "New customers",
        "description": "New customers",
    },
    {
        "group_code": "wholesale",
        "group_name": "Wholesale customers",
        "description": "Wholesale customers",
    },
    {
        "group_code": "vip",
        "group_name": "VIP customers",
        "description": "VIP customers",
    },
]


class Command(BaseCommand):
    help = "Create the base customer groups."

    def add_arguments(self, parser):
        parser.add_argument(
            "--partner_slug",
            type=str,
            help="Slug of the partner",
            default=None,
        )

    def handle(self, *args, **options):
        partner_slug = options["partner_slug"]
        for group in CUSTOMER_GROUPS:
            if (
                CustomerGroup.objects.filter(group_code=group["group_code"]).count()
                == 0
            ):
                customer_group = CustomerGroup.objects.create(
                    group_code=group["group_code"],
                    group_name=group["group_name"],
                    group_description=group["description"],
                )
                self.stdout.write(
                    self.style.WARNING(f'Customer group {group["group_code"]} created')
                )
            else:
                customer_group = CustomerGroup.objects.filter(
                    group_code=group["group_code"]
                ).update(
                    group_name=group["group_name"],
                    group_description=group["description"],
                )
                self.stdout.write(
                    self.style.ERROR(f'Customer group {group["group_code"]} updated')
                )
            if partner_slug:
                partner = Partner.objects.filter(partner_slug=partner_slug).last()
                customer_group.partner = partner
                customer_group.save()
