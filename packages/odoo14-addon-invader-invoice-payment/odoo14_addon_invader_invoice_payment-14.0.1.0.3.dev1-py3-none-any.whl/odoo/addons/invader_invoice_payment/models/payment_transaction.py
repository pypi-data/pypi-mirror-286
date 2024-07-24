# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    invoice_ids = fields.Many2many(
        comodel_name="account.move",
        relation="account_invoice_transaction_rel",
        column1="transaction_id",
        column2="invoice_id",
        string="Invoices",
        copy=False,
        readonly=True,
    )
    invoice_ids_nbr = fields.Integer(
        compute="_compute_invoice_ids_nbr", string="# of invoices"
    )

    @api.depends("invoice_ids")
    def _compute_invoice_ids_nbr(self):
        """
        Compute function for the field invoice_ids_nbr.
        Count the number of invoices.
        :return:
        """
        for record in self:
            record.invoice_ids_nbr = len(record.invoice_ids)

    def action_view_account_invoice(self):
        action = {
            "name": _("Invoice(s)"),
            "type": "ir.actions.act_window",
            "res_model": self.invoice_ids._name,
            "target": "current",
        }
        invoices = self.invoice_ids
        if len(invoices) == 1:
            action.update({"res_id": invoices.id, "view_mode": "form"})
        else:
            action.update(
                {
                    "domain": [("id", "in", invoices.ids)],
                    "view_mode": "tree,form",
                }
            )
        return action

    def _get_invoice_not_payable_states(self):
        """
        Get invoice states where it's not possible to pay.
        :return: list of str
        """
        return ["paid", "cancel"]

    def _get_invader_payables(self):
        """
        Inherit to return invoices to pay
        :return: recordset
        """
        self.ensure_one()
        if self.invoice_ids:
            states = self._get_invoice_not_payable_states()
            return self.invoice_ids.filtered(lambda i: i.state not in states)
        return super()._get_invader_payables()
