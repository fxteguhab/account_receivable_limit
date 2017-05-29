from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, date, timedelta


class sale_order(osv.osv):
	_inherit = 'sale.order'
	
	# COLUMNS ---------------------------------------------------------------------------------------------------------------
	
	_columns = {
		'is_receivable_overlimit': fields.boolean('Is Receivable Enabled'),
	# field untuk membatasi sale order list yang muncul sesuai dengan date dari res config global
		'limit_sale_order_date' : fields.date("Limit Sale Order Date")
	}
	
	# DEFAULTS --------------------------------------------------------------------------------------------------------------
	
	_defaults = {
		'is_receivable_overlimit': False,
		'limit_sale_order_date' : lambda *a: datetime.today().strftime('1970-01-01 00:00:00'),
	}
	
	# ACTIONS ---------------------------------------------------------------------------------------------------------------

	def action_button_confirm(self, cr, uid, ids, context=None):
		partner_obj = self.pool.get('res.partner')
		for order in self.browse(cr, uid, ids, context):
			if partner_obj.is_credit_overlimit(cr, uid, order.partner_id.id, order.amount_total, context):
				raise osv.except_osv(_('Warning!'), _('Credit is / will be over-limit.'))
		return super(sale_order, self).action_button_confirm(cr, uid, ids, context)