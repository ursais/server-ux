# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Recompute stored reviewers so implied group members are included.

    ``active_test`` is disabled so archived users already stored on the
    relation are visible and get removed. Assigning ``reviewer_ids`` does
    not send review notifications.
    """
    env = api.Environment(cr, SUPERUSER_ID, {"active_test": False})
    reviews = env["tier.review"].search(
        [
            "|",
            ("reviewer_group_id", "!=", False),
            ("reviewer_field_id.relation", "=", "res.groups"),
        ]
    )
    if not reviews:
        return
    _logger.info(
        "Recomputing reviewers for %s tier reviews to include implied group members",
        len(reviews),
    )
    env.add_to_compute(reviews._fields["reviewer_ids"], reviews)
    reviews.flush_recordset(["reviewer_ids"])
