__autor__ = 'nickbortolotti'
__licencia__ = 'Apache 2.0'

import os
import sys
import simplejson
import jinja2
import webapp2

from apiclient.discovery import build
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

#Decorador para el cliente de BigQuery - ** Recuerde utilizar su client_secrets.json **
decorator = OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
                                             scope='https://www.googleapis.com/auth/plus.me')

#Construccion del servicio de BigQuery
servicio = build('plus', 'v1')

#Variables del proyecto
Proyecto = 'socialagilelearning'

#Entorno Jinja para trabajar plantillas y el HTML
Entorno_Jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Panel(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        http = decorator.http()
        try:
            usuario = servicio.people().get(userId='me').execute(http=http)
            nombre = usuario['displayName']

            #Definicion de los datos para insertar en HTML. Jinja2
            plantilla_values = {
                 'nombre_usuario': nombre,
            }

            #Inferencia de la plantilla con el HTML correspondiente
            template = Entorno_Jinja.get_template('index.html')
            self.response.write(template.render(plantilla_values))

        except:
            e = str(sys.exc_info()[0]).replace('&', '&amp;'
            ).replace('"', '&quot;'
            ).replace("'", '&#39;'
            ).replace(">", '&gt;'
            ).replace("<", '&lt;')
            self.response.out.write("<p>Error: %s</p>" % e)


application = webapp2.WSGIApplication([
                                         ('/', Panel),
                                         (decorator.callback_path, decorator.callback_handler()),
                                     ], debug=True)