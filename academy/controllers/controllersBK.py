from odoo import http


class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['academy.teachers']
        return http.request.render('academy.index', {
            'teachers': Teachers.search([])
        })

    @http.route('/academy/academy/<name>/', auth='public' , website=True)
    def human(self, **kw):
        if kw['name']=='human':
            Humans = http.request.env['res.partner']
            return http.request.render('academy.human', {
                'humans': Humans.search([])
            })
        else:
            try:
                acquirer_id =int(kw['name'].replace('h=','',1))
            except:
                Humans = http.request.env['res.partner'].search([('id','=',0)])
                return http.request.render('academy.human', {
                'humans': Humans
                })
            hum_id=int(kw['name'].replace('h=','',1))
            Humans = http.request.env['res.partner'].search([('id','=',hum_id)])
            return http.request.render('academy.human', {
                'humans': Humans
            })

    @http.route('/academy/<model("academy.teachers"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('academy.biography', {
            'person': teacher
        })

    # @http.route('/academy/human/<int:id>/', auth='public', website=True)
    # def human(self,**kw):
    #     Humans = http.request.env['res.partner'].search([('id','=',kw['id'])])
    #     return http.request.render('academy.human', {
    #         'humans': Humans
    #     })

    # @http.route('/academy/human/<name>/', auth='public', website=True)
    # def human(self, **kw):
    #     Humans = http.request.env['res.partner'].search([('name', '=', kw['name'])])
    #     return http.request.render('academy.human', {
    #         'humans': Humans
    #     })
#     @http.route('/academy/academy/objects/', auth='public')