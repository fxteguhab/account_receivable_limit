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
	'depends': ['base','board','web','stock', 'sale'],
	'data': [
		'views/res_partner_view.xml',
		'views/res_config_view.xml',
		'views/account_receivable_limit_view.xml',
		'menu/account_receivable_limit_menu.xml'
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