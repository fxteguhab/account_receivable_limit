from datetime import datetime
from openerp.osv import osv, fields


class res_partner(osv.osv):
	_inherit = 'res.partner'
	
	# COLUMNS ---------------------------------------------------------------------------------------------------------------
	
	_columns = {
		'is_overlimit_enabled': fields.boolean('Is Overlimit Enabled')
	}
	
	# DEFAULTS --------------------------------------------------------------------------------------------------------------
	
	_defaults = {
		'is_overlimit_enabled': False
	}
	
	# OVERRIDES -------------------------------------------------------------------------------------------------------------
	
	def create(self, cr, uid, vals, context=None):
		receivable_limit_log_obj = self.pool.get('res.partner.receivable.limit.log')
		result_partner_id = super(res_partner, self).create(cr, uid, vals, context)
		if vals.get('customer', False):
			receivable_limit_log_obj.record_receivable_limit_changes(
				cr, uid, result_partner_id, 0, vals.get('credit_limit', 0)
			)
		return super(res_partner, self).create(cr, uid, vals, context)
	
	def write(self, cr, uid, ids, vals, context=None):
		new_credit = vals.get('credit_limit', False)
		if new_credit:
			receivable_limit_log_obj = self.pool.get('res.partner.receivable.limit.log')
			for partner in self.browse(cr, uid, ids, context):
				if vals.get('customer', partner.customer):
					receivable_limit_log_obj.record_receivable_limit_changes(
						cr, uid, partner.id, partner.credit_limit, new_credit
					)
		return super(res_partner, self).write(cr, uid, ids, vals, context)
	
	# METHODS ---------------------------------------------------------------------------------------------------------------
	
	def is_credit_overlimit(self, cr, uid, partner_id, credit_modifier=0, context=None):
		"""
		Checks for the given partner_id with is_overlimit_enabled is False whether current credit + credit modifier is larger
		than credit_limit
		:param partner_id: int: Id of res.partner.
		:param credit_modifier: float: modifies current credit to be calculated with credit_limit
		:return: True if if is_overlimit_enabled is False current credit + credit modifier is larger than credit_limit;
			otherwise returns False.
		"""
		partner = self.browse(cr, uid, [partner_id], context)[0]
		if (not (partner.credit_limit == 0.0 or partner.credit_limit is None or partner.is_overlimit_enabled)
				and partner.credit + credit_modifier > partner.credit_limit):
			return True
		return False

# ==========================================================================================================================


class res_partner_receivable_limit_log(osv.osv):
	_name = 'res.partner.receivable.limit.log'
	
	# COLUMNS ---------------------------------------------------------------------------------------------------------------
	
	_columns = {
		'partner_id': fields.many2one('res.partner', 'Customer', required=True, ondelete='cascade'),
		'change_date': fields.datetime('Change Date', required=True),
		'old_limit': fields.float('Old Limit', required=True),
		'new_limit': fields.float('New Limit', required=True),
		'change_by': fields.many2one('res.users', 'Change by')
	}
	
	# DEFAULTS --------------------------------------------------------------------------------------------------------------
	
	_defaults = {
		'change_by': lambda self, cr, uid, context: uid
	}
	
	# OVERRIDES -------------------------------------------------------------------------------------------------------------
	
	def name_get(self, cr, uid, ids, context=None):
		result = []
		for log in self.browse(cr, uid, ids, context):
			name = log.change_date + ' / ' + log.partner_id.name
			result.append((log.id, name))
		return result
	
	# METHODS ---------------------------------------------------------------------------------------------------------------
	
	def record_receivable_limit_changes(self, cr, uid, partner_id, old_limit, new_limit, context=None):
		"""
		Write new record for receivable limit changes.
		:param partner_id: int: Id of res.partner.
		:param old_limit: float: Old credit limit.
		:param new_limit: float: New credit limit.
		:return: Boolean: True if successful
		"""
		vals = {
			'partner_id': partner_id,
			'change_date': datetime.now(),
			'old_limit': old_limit,
			'new_limit': new_limit,
			'change_by': uid
		}
		self.create(cr, uid, vals, context)
		return True