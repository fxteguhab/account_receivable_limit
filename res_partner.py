from openerp.osv import osv, fields


class res_partner(osv.osv):
	_inherit = 'res.partner'
	
	_columns = {
		'is_overlimit_enabled': fields.boolean('Is Overlimit Enabled')
	}
	
	_defaults = {
		'is_overlimit_enabled': False
	}


class res_partner_receivable_limit_log(osv.osv):
	_name = 'res.partner.receivable.limit.log'
	
	_columns = {
		'partner_id': fields.many2one('res.partner', 'Customer', required=True, ondelete='cascade'),
		'change_date': fields.datetime('Change Date', required=True),
		'old_limit': fields.float('Old Limit', required=True),
		'new_limit': fields.float('New Limit', required=True),
		'change_by': fields.many2one('res.users', 'Change by')
	}
	
	_defaults = {
		'change_by': lambda self, cr, uid, context: uid
	}
	
	def name_get(self, cr, uid, ids, context=None):
		result = []
		for log in self.browse(cr, uid, ids, context):
			name = log.change_date + ' / ' + log.partner_id.name
			result.append((log.id, name))
		return result