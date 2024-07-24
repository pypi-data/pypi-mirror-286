from jjsystem.database import db
from jjsystem.common.subsystem import entity


class Regiao(entity.Entity, db.Model):

    attributes = ['codigo_ibge', 'sigla', 'nome']
    attributes += entity.Entity.attributes

    codigo_ibge = db.Column(db.Numeric(1, 0), nullable=False, unique=True)
    sigla = db.Column(db.CHAR(2), nullable=False, unique=True)
    nome = db.Column(db.String(20), nullable=False)

    def __init__(self, id, codigo_ibge, sigla, nome,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.codigo_ibge = codigo_ibge
        self.sigla = sigla
        self.nome = nome

    @classmethod
    def collection(cls):
        return 'regioes'
