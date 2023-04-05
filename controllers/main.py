import odoo
import json
import logging
_logger = logging.getLogger(__name__)

class SchoolAPI(odoo.http.Controller):
    @odoo.http.route('/foo', auth='public')
    def foo_handler(self):
        return "Welcome to 'foo' API!"

    @odoo.http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })

    @odoo.http.route(['/school/<db_15>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def pet_handler(self, db_15, id, **kw):
        model_name = "school.information"
        try:
            registry = odoo.modules.registry.Registry(db_15)
            with odoo.api.Environment.manage(), registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                response = {
                    "status": "ok",
                    "content": {
                        "sch_id": rec.sch_id,
                        "name": rec.name,
                        "type": rec.type,
                        "email": rec.email,
                        "address": rec.address,
                    }
                }
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)
