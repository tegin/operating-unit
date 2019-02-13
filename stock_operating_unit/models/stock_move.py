from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    operating_unit_id = fields.Many2one(
        related='location_id.operating_unit_id',
        string='Source Location Operating Unit',
        readonly=True,
    )
    operating_unit_dest_id = fields.Many2one(
        related='location_dest_id.operating_unit_id',
        string='Dest. Location Operating Unit',
        readonly=True,
    )

    @api.multi
    @api.constrains('operating_unit_id', 'picking_id',
                    'location_id', 'operating_unit_dest_id',
                    'location_dest_id')
    def _check_stock_move_operating_unit(self):
        for stock_move in self:
            if not stock_move.operating_unit_id:
                return True
            operating_unit = stock_move.operating_unit_id
            operating_unit_dest = stock_move.operating_unit_dest_id
            if (stock_move.location_id and
                stock_move.location_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit != stock_move.picking_id.operating_unit_id
                ) and (
                stock_move.location_dest_id and
                stock_move.location_dest_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit_dest != stock_move.picking_id.operating_unit_id
            ):
                raise UserError(
                    _('Configuration error\nThe Stock moves must '
                      'be related to a location (source or destination) '
                      'that belongs to the requesting Operating Unit.')
                )
