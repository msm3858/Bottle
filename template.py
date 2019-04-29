from bottle import SimpleTemplate
from bottle import template
# First attempt.
tpl = SimpleTemplate("Hello{{name}}!")
tpl.render(name="World")
# Second attempt.
template("Hello {{name}}!", name='World')
# Third attempt.
my_dict={'number':123, 'street': 'Fake St.', 'city': 'Fakeville'}
template('I live at {{number}} {{street}}, {{city}}', *my_dict)



