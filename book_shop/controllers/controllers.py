from odoo import http

class book_shop(http.Controller):
    @http.route('/writer/<model("book_shop.writer"):writer>/', auth='public', website=True)
    def teacher(self, writer):
        return http.request.render('book_shop.writer', {
            'writer': writer
        })

    @http.route('/writers', auth='public', website=True)
    def writers(self, **kw):
        try:
            if int(kw['id'])>=0:
                writer = http.request.env['book_shop.writer'].search([('id', '=', kw['id'])])
        except ValueError:
            if kw['id'] == 'all':
                writer = http.request.env['book_shop.writer'].search([])
            else:
                writer = http.request.env['book_shop.writer']
        return http.request.render('book_shop.writer', {
                'writers': writer
            })

    @http.route('/submit',  type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def index(self, **kw):
        data=kw
        model=kw['model']
        del data['model']
        table=http.request.env[model]
        response=table.create(data)
        data['ID']=response.id
        return http.request.render('book_shop.submit', {
            'msg': data,
        })