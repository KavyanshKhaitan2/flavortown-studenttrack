from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.messages import error, success, info
from django.shortcuts import redirect
from .models import ScheduleSlot


# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = {}
        schedule_grid: dict[str, list] = {}
        for schedule in self.request.user.scheduleslot_set.all():
            schedule_grid.setdefault(schedule.day, [])
            schedule_grid[schedule.day].append(schedule)
            schedule_grid[schedule.day].sort(key=lambda x: x.period)
        context["schedule_grid"] = schedule_grid
        grid_items = list(schedule_grid.items())
        if len(grid_items) == 0:
            context["schedule_width"] = 0
        else:
            context["schedule_width"] = len(grid_items[0][1])
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, "dashboard/index.html", context=context)


class EditRoutineView(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = {}
        schedule_grid: dict[str, list] = {day: [] for day in ScheduleSlot.DAY_CHOICES}
        for schedule in ScheduleSlot.objects.filter(user=self.request.user):
            schedule_grid[schedule.day].append(schedule)
            schedule_grid[schedule.day].sort(key=lambda x: x.period)
        context["schedule_grid"] = schedule_grid
        grid_items = list(schedule_grid.items())
        if len(grid_items) == 0:
            context["schedule_width"] = 0
        else:
            context["schedule_width"] = len(grid_items[0][1])
        return context

    def get(self, request):
        return render(request, "routine/edit.html", context=self.get_context_data())

    def deleteAction(self, request):
        days_to_delete = []
        for key in request.POST.keys():
            if key.startswith("checkbox-"):
                day = key.removeprefix("checkbox-")
                if day in ScheduleSlot.DAY_CHOICES:
                    days_to_delete.append(day)
        if len(days_to_delete) == 0:
            info(request, "Couldnt find any selected day.")
            return
        for slot in ScheduleSlot.objects.filter(user=request.user):
            if slot.day in days_to_delete:
                slot.delete()
        success(request, "Deleted the selected days.")

    def undeleteAction(self, request):
        context = self.get_context_data()
        days_to_undelete = []
        for key in request.POST.keys():
            if key.startswith("checkbox-"):
                day = key.removeprefix("checkbox-")
                if day in ScheduleSlot.DAY_CHOICES:
                    days_to_undelete.append(day)
        if len(days_to_undelete) == 0:
            info(request, "Couldnt find any selected day.")
            return
        for day in days_to_undelete:
            for i in range(1, context['schedule_width']+1):
                ScheduleSlot.objects.get_or_create(
                    user=self.request.user,
                    day=day,
                    period=i,
                )
        success(request, "Undeleted the selected days.")

    def updateAction(self, request):
        context = self.get_context_data()
        schedule_width = request.POST["schedule_width"]
        schedule_width = int(schedule_width)
        if schedule_width < 0:
            error(request, "Schedule width cannot be negative!")
            return redirect(self.request.path_info)
        if schedule_width > context["schedule_width"]:
            for i in range(1, schedule_width + 1):
                for day in ScheduleSlot.DAY_CHOICES:
                    ScheduleSlot.objects.get_or_create(
                        user=self.request.user,
                        day=day,
                        period=i,
                    )
            success(request, "Successfully increased schedule_width!")
        if schedule_width < context["schedule_width"]:
            for slot in ScheduleSlot.objects.filter(user=self.request.user):
                if slot.period > schedule_width:
                    slot.delete()
            success(request, "Successfully decreased schedule_width!")
        slot_pks = []
        for key in dict(request.POST).keys():
            if key.startswith("slot-value-PK-"):
                slot_pks.append(int(key.removeprefix("slot-value-PK-")))
        updated = False
        for pk in slot_pks:
            slot = ScheduleSlot.objects.get(pk=pk)
            if slot.user != request.user:
                error(
                    request,
                    f"You do not own the schedule slot that you wished to edit! (Error key: {pk})",
                )
                break
            form_subject: str = request.POST[f"slot-value-PK-{pk}"].strip()
            if slot.subject == form_subject:
                continue
            slot.subject = form_subject
            slot.save()
            updated = True
        if updated:
            success(request, "Updated routine successfully.")

    def post(self, request):
        action = request.POST["action"]
        if action == "update":
            self.updateAction(request)
        if action == "delete":
            self.deleteAction(request)
        if action == "undelete":
            self.undeleteAction(request)
        return redirect(self.request.path_info)
