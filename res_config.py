from openerp.osv import fields, osv
from openerp.tools.translate import _

from datetime import datetime, date, timedelta
from openerp import SUPERUSER_ID

class sale_order_config_settings(osv.osv_memory):
	_name = 'sale.order.config.settings'
	_inherit = 'res.config.settings'
	
	_PARAMS = [
		("limit_sale_order_date", "sale.order"),
	]
	
	_columns = {
		'limit_sale_order_date': fields.date("Limit Sale Order Date",
			help="This setting is for limit to show Sale Order list. Just show Sale Order with date greater than this setting date."),
	}
	
	def get_default_params(self, cr, uid, fields, context=None):
		res = {}
		param = self.pool.get('ir.config_parameter').get_param(cr, uid, 'sale.order', None)
		if param is not None:
			res['limit_sale_order_date'] = param
		return res
	
	def create(self, cr, uid, values, context=None):
		id = super(sale_order_config_settings, self).create(cr, uid, values, context)
		# Hack: to avoid some nasty bug, related fields are not written upon record creation.
		# Hence we write on those fields here.
		vals = {}
		for fname, field in self._columns.iteritems():
			if isinstance(field, fields.related) and fname in values:
				vals[fname] = values[fname]
		self.write(cr, uid, [id], vals, context)
		return id
	
	def set_params(self, cr, uid, ids, context=None):
		config_param_obj = self.pool.get('ir.config_parameter')
		config = self.browse(cr, uid, ids[0], context)
		config_param_obj.set_param(cr, uid, 'sale.order', config.limit_sale_order_date)