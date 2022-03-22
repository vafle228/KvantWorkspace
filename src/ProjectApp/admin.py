from django.contrib import admin

from .models import (ActiveKvantProject, ClosedKvantProject, KvantProject,
                     KvantProjectMembershipRequest, KvantProjectTask,
                     MemberHiringKvantProject)

admin.site.register(KvantProject)
admin.site.register(KvantProjectTask)
admin.site.register(ClosedKvantProject)
admin.site.register(ActiveKvantProject)
admin.site.register(MemberHiringKvantProject)
admin.site.register(KvantProjectMembershipRequest)

