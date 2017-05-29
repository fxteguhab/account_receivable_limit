from openerp.osv import fields, osv
from openerp.tools.translate import _

from datetime import datetime, date, timedelta
from openerp import SUPERUSER_ID

class sale_order_config_settings(osv.osv_memory):
	_name = 'sale.order.config.settings'
	_inherit = 'res.config.settings'
	
	_columns = {
		'limit_sale_order_date': fields.date("Limit Sale Order Date",
			help="This setting is for limit to show Sale Order list. Just show Sale Order with date greater than this setting date."),
	}
	
	def create(self, cr, uid, values, context=None):
		id = super(sale_order_config_settings, self).create(cr, uid, values, context)
		# Hack: to avoid some nasty bug, related fields are not written upon record creation.
		# Hence we write on those fields here.
		vals = {}
		for fname, field in self._columns.iteritems():
			if isinstance(field, fields.related) and fname in values:
				vals[fname] = values[fname]
		self.write(cr, uid, [id], vals, context)
		
		sale_order_obj = self.pool.get('sale.order')
		sale_order_ids = sale_order_obj.search(cr, uid, [])
		if values.get('limit_sale_order_date', False):
			sale_order_obj.write(cr, uid, sale_order_ids, {
				'limit_sale_order_date': values['limit_sale_order_date'],
			}, context=context)
		else:
			sale_order_obj.write(cr, uid, sale_order_ids, {
				'limit_sale_order_date': datetime.today().strftime('1970-01-01 00:00:00'),
			}, context=context)
		return id