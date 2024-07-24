# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class CartService(Component):
    _inherit = "shopinvader.cart.service"

    def _prepare_cart(self, **cart_params):
        res = super()._prepare_cart(**cart_params)
        backend = self.shopinvader_backend
        if "workflow_process_id" not in cart_params and backend.workflow_process_id:
            res["workflow_process_id"] = backend.workflow_process_id.id
        return res
