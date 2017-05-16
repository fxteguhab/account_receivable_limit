from openerp.osv import osv, fields


class res_partner(osv.osv):
	_inherit = 'res.partner'
	
	_columns = {
		'is_overlimit_enabled': fields.boolean('Is Overlimit Enabled')
		# Kalau True maka meskipun limit piutang diset tapi tetap boleh overlimit.
		# 	Note: di view, posisi field ini adalah di bawah credit_limit
	}
	
	_defaults = {
		'is_overlimit_enabled': False
	}