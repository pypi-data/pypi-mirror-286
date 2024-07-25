from odoo import api, fields, models

class EditorialCompany(models.Model):
    """Extend res.company for editorial management"""

    _inherit = "res.company"
    _check_company_auto = True

    module_editorial_ddaa = fields.Boolean("Gestión de DDAA", default=False)

    @api.model
    def _default_product_category_ddaa(self):
        try:
            return self.env.ref("gestion_editorial.product_category_ddaa").id
        except ValueError:
            return False

    @api.model
    def _default_product_categories_genera_ddaa(self):
        try:
            return [self.env.ref("gestion_editorial.product_category_genera_ddaa").id]
        except ValueError:
            return False

    def is_category_genera_ddaa_or_child(self, cat_id):
        if cat_id.parent_path:
            parents_and_self_ids = [int(x) for x in cat_id.parent_path.split("/")[:-1]]
            for cat_ddaa_id in self.product_categories_genera_ddaa_ids:
                if cat_ddaa_id.id in parents_and_self_ids:
                    return True
        return False

    @api.model
    def _default_stock_picking_type_deposito_compra(self):
        try:
            return self.env.ref("gestion_editorial.stock_picking_type_compra_deposito").id
        except ValueError:
            return False

    @api.model
    def _default_account_journal_compra_deposito(self):
        try:
            return self.env.ref("gestion_editorial.account_journal_compra_deposito").id
        except ValueError:
            return False

    product_category_ddaa_id = fields.Many2one(
        "product.category",
        string="Categoría de producto para DDAA",
        default=_default_product_category_ddaa,
        help="Categoría de producto que representa los derechos de autoría.",
    )

    product_categories_genera_ddaa_ids = fields.Many2many(
        "product.category",
        string="Categorías que generan DDAA",
        default=_default_product_categories_genera_ddaa,
        help="Categorías de producto madre que generan derechos de autoría.",
    )

    stock_picking_type_compra_deposito_id = fields.Many2one(
        "stock.picking.type",
        string="Tipo de operación de depósito compra",
        default=_default_stock_picking_type_deposito_compra,
        help="Tipo de operación usada para las compras a depósito.",
    )

    account_journal_deposito_compra_id = fields.Many2one(
        "account.journal",
        string="Diario para liquidaciones de compra a depósito",
        default=_default_account_journal_compra_deposito,
    )
