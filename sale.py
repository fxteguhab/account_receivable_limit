from openerp.osv import osv, fields
from openerp.tools.translate import _


class sale_order(osv.osv):
	_inherit = 'sale.order'
	
	_columns = {
		'is_receivable_overlimit': fields.boolean('Is Receivable Enabled')
	}
	
	_defaults = {
		'is_receivable_overlimit': False
	}

	def action_button_confirm(self, cr, uid, ids, context=None):
		partner_obj = self.pool.get('res.partner')
		for order in self.browse(cr, uid, ids, context):
			if partner_obj.is_credit_overlimit(cr, uid, order.partner_id.id, order.amount_total, context):
				raise osv.except_osv(_('Warning!'), _('Credit is / will be over-limit.'))
		
		return super(sale_order, self).action_button_confirm(cr, uid, ids, context)