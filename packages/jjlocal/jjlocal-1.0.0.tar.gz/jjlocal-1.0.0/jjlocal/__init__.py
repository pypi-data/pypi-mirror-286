import os
import jjsystem

from jjsystem.system import System
from flask_cors import CORS
from jjlocal.subsystem.common import endereco
from jjlocal.subsystem.sysadmin import ibge_sync
from jjlocal.subsystem.parametrizacao.localidade \
    import regiao, uf, mesorregiao, microrregiao, municipio, pais
from jjlocal.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('jjlocal',
                [endereco.subsystem, ibge_sync.subsystem, regiao.subsystem,
                 mesorregiao.subsystem, uf.subsystem, microrregiao.subsystem,
                 municipio.subsystem, pais.subsystem],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(jjsystem.SystemFlask):

    def __init__(self):
        super().__init__(system)

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        jjlocal_database_uri = os.getenv('JJLOCAL_DATABASE_URI', None)
        if jjlocal_database_uri is None:
            raise Exception('JJLOCAL_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for Postgres
            # export JJLOCAL_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/jjlocal
            self.config['SQLALCHEMY_DATABASE_URI'] = jjlocal_database_uri
