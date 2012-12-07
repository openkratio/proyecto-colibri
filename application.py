#!/usr/bin/env python
## -*- coding: utf-8 -*-
import os
from mako import exceptions
from mako.lookup import TemplateLookup
import tornado.ioloop
import tornado.web
from tornado import httpclient
from db import Database

root = os.path.dirname(__file__)
template_root = os.path.join(root, 'templates')
blacklist_templates = ('layouts',)
template_lookup = TemplateLookup(input_encoding='utf-8',
                                 output_encoding='utf-8',
                                 encoding_errors='replace',
                                 directories=[template_root])

def render_template(filename):
    if os.path.isdir(os.path.join(template_root, filename)):
        filename = os.path.join(filename, 'index.html')
    else:
        filename = '%s.html' % filename
    if any(filename.lstrip('/').startswith(p) for p in blacklist_templates):
        raise httpclient.HTTPError(404)
    try:
        return template_lookup.get_template(filename).render()
    except exceptions.TopLevelLookupException:
        raise httpclient.HTTPError(404)

class DefaultHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception, **kwargs):
        if hasattr(exception, 'code'):
            self.set_status(exception.code)
            if exception.code == 500:
                return exceptions.html_error_template().render()
            return render_template(str(exception.code))
        return exceptions.html_error_template().render()

    def return_json(self, data_dict):
        self.set_header('Content-Type', 'application/json')
        json_ = tornado.escape.json_encode(data_dict)
        self.write(json_)
        self.finish()

class MainHandler(DefaultHandler):
    def get(self, filename):
         self.write(render_template(filename))

class JsonHandler(DefaultHandler):
    def get(self, collection):
        data_instance = Database()
        connection = data_instance.connect_mongo()
        my_dict = data_instance.get_collection(connection, collection)
        data_instance.disconnect_mongo(connection)
        self.return_json(my_dict)

application = tornado.web.Application([
    (r'^/json/(?P<collection>[a-z]+)/$', JsonHandler),
    (r'^/index.html$', MainHandler),
], debug=True, static_path=os.path.join(root, 'static'))

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
