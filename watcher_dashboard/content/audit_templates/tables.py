# -*- encoding: utf-8 -*-
# Copyright (c) 2016 b<>com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
import horizon.exceptions
import horizon.messages
import horizon.tables

from watcher_dashboard.api import watcher


AUDIT_TEMPLATE_GOAL_DISPLAY_CHOICES = (
    ("BASIC_CONSOLIDATION", pgettext_lazy(
        "Goal of an Audit",
        "Consolidate Servers")),
    ("MINIMIZE_ENERGY_CONSUMPTION", pgettext_lazy(
        "Goal of an Audit",
        "Minimize Energy")),
    ("BALANCE_LOAD", pgettext_lazy(
        "Goal of an Audit",
        "Load Balancing")),
    ("MINIMIZE_LICENSING_COST", pgettext_lazy(
        "Goal of an Audit",
        "Minimize Licensing Cost")),
    ("PREPARED_PLAN_OPERATION", pgettext_lazy(
        "Goal of an Audit",
        "Prepared Plan Operation")),
)


class CreateAuditTemplates(horizon.tables.LinkAction):
    name = "create"
    verbose_name = _("Create Template")
    url = "horizon:admin:audit_templates:create"
    classes = ("ajax-modal", "btn-launch")


class AuditTemplatesFilterAction(horizon.tables.FilterAction):
    filter_type = "server"
    filter_choices = (
        ('name', _("Template Name ="), True),
    )


class LaunchAudit(horizon.tables.BatchAction):
    name = "launch_audit"
    verbose_name = _("Launch Audit")
    data_type_singular = _("Launch Audit")
    data_type_plural = _("Launch Audits")
    success_url = "horizon:admin:audits:index"
    # icon = "cloud-upload"
    # policy_rules = (("compute", "compute:create"),)

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            "Launch Audit",
            "Launch Audits",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            "Launched Audit",
            "Launched Audits",
            count
        )

    def action(self, request, obj_id):
        params = {'audit_template_uuid': obj_id}
        params['type'] = 'ONE_SHOT'
        params['deadline'] = None
        watcher.Audit.create(request, **params)


class DeleteAuditTemplates(horizon.tables.DeleteAction):
    verbose_name = _("Delete Templates")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            "Delete Template",
            "Delete Templates",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            "Deleted Template",
            "Deleted Templates",
            count
        )

    def delete(self, request, obj_id):
        watcher.AuditTemplate.delete(request, obj_id)


class AuditTemplatesTable(horizon.tables.DataTable):
    name = horizon.tables.Column(
        'name',
        verbose_name=_("Name"),
        link="horizon:admin:audit_templates:detail")
    goal = horizon.tables.Column(
        'goal',
        verbose_name=_('Goal'),
        status=True,
        status_choices=AUDIT_TEMPLATE_GOAL_DISPLAY_CHOICES
    )

    def get_object_id(self, datum):
        return datum.uuid

    class Meta(object):
        name = "audit_templates"
        verbose_name = _("Available")
        table_actions = (
            CreateAuditTemplates,
            DeleteAuditTemplates,
            AuditTemplatesFilterAction,
            # LaunchAuditTemplates,
        )
        row_actions = (
            LaunchAudit,
            # CreateAuditTemplates,
            # DeleteAuditTemplates,
        )