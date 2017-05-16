# noinspection PyStatementEffect
{
	'name': 'Account Receivable Limit',
	'version': '1.0',
	'author': 'Christyan Juniady and Associates',
	'maintainer': 'Christyan Juniady and Associates',
	'category': 'General',
	'sequence': 21,
	'website': 'http://www.chjs.biz',
	'summary': '',
	'description': """
		Stock Opname
	""",
	'images': [
	],
	'depends': ['base','board','web','stock'],
	'data': [
		'views/res_partner.xml',
		'views/account_receivable_limit.xml',
		'menu/account_receivable_limit.xml'
	],
	'demo': [
	],
	'test': [
	],
	'installable': True,
	'application': True,
	'auto_install': False,
	'qweb': [
		'static/src/xml/ipc_idss.xml'
	 ],
}