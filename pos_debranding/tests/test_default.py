
import eagle.tests


@eagle.tests.common.at_install(True)
@eagle.tests.common.post_install(True)
class TestUi(eagle.tests.HttpCase):

    def test_01_check_logo(self):
        env = self.env
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        env['ir.module.module'].search([('name', '=', 'pos_debranding')], limit=1).state = 'installed'
        self.phantom_js(
            '/web',

            "eagle.__DEBUG__.services['web_tour.tour']"
            ".run('pos_debranding_tour')",

            "eagle.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_debranding_tour.ready",

            login="admin",
            timeout=240,
        )
