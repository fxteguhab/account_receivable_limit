from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta

class sale_order(osv.osv):
	_inherit = 'sale.order'
	
	# COLUMNS ---------------------------------------------------------------------------------------------------------------
	
	_columns = {
		'is_receivable_overlimit': fields.boolean('Is Receivable Enabled'),
	}
	
	# DEFAULTS --------------------------------------------------------------------------------------------------------------
	
	_defaults = {
		'is_receivable_overlimit': False,
	}

	# ACTIONS ---------------------------------------------------------------------------------------------------------------

	def action_button_confirm(self, cr, uid, ids, context=None):
		partner_obj = self.pool.get('res.partner')
		for order in self.browse(cr, uid, ids, context):
			if partner_obj.is_credit_overlimit(cr, uid, order.partner_id.id, order.amount_total, context):
				if order.partner_id.is_overlimit_enabled:
					self.write(cr, uid, [order.id], {
						'is_receivable_overlimit': True,
						})
				else:
					raise osv.except_osv(_('Warning!'), _('Credit is / will be over-limit.'))
		return super(sale_order, self).action_button_confirm(cr, uid, ids, context)
	
	def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
		# Jika diminta supaya list dibatasi hanya untuk n date berapa hari yang lalu
		# untuk mengaktifkan fitur ini, tambahkan context limit_date di menu
		if context is not None and context.get('limit_date', False) :
			limit_n_date = self.pool.get('ir.config_parameter').get_param(cr, uid, 'sale.order', 0)
			if limit_n_date != 0:
				today = (datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
				n_date = int(limit_n_date)
			# kurangkan dengan timezone
				#n_pass_date = ((today - timedelta(hours=24*n_date)) - timedelta(hours = 7)).strftime('%Y-%m-%d %H:%M:%S')
				n_pass_date = (today - n_date).strftime('%Y-%m-%d %H:%M:%S')
				args.append(['date_order', '>=', n_pass_date])
		return super(sale_order,self).search(cr, uid, args, offset, limit, order, context, count)