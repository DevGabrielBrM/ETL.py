from abstract_etl import AbstractETL
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import *

class ETL:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def extract(self):
        with open(self.source, 'r') as file:
            return json.load(file)

    def transform(self):
        data = self.extract()
        transformed_data = []

        for entry in data:
            tipo = entry['tipo']
            atributos = entry['atributos']

            if tipo == 'UNIDADE_PRODUCAO':
                for attr in atributos:
                    unidade_producao = UNIDADE_PRODUCAO(
                        numero=attr['numero'],
                        peca_hora_nominal=attr['peca_hora_nominal']
                    )
                    transformed_data.append(unidade_producao)
            else:
                transformed_data.append((tipo, atributos))

        return transformed_data

    def load(self):
        transformed_data = self.transform()

        engine = create_engine(self.target)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        unidade_producao_entries = []
        other_entries = []

        for item in transformed_data:
            if isinstance(item, UNIDADE_PRODUCAO):
                unidade_producao_entries.append(item)
            else:
                other_entries.append(item)

    
        session.add_all(unidade_producao_entries)
        session.commit()

        
        for item in other_entries:
            tipo, atributos = item
            if tipo == 'REGISTRO_FALHA':
                for attr in atributos:
                    registro_falha = REGISTRO_FALHA(
                        id=attr['id'],
                        severidade=bool(attr['severidade']),
                        inicio=attr['inicio'],
                        fim=attr['fim'],
                        numero_unidade_producao=attr['numero_unidade_producao']
                    )
                    session.add(registro_falha)
            elif tipo == 'PECA':
                for attr in atributos:
                    peca = PECA(
                        numero=attr['numero'],
                        status=attr['status'],
                        inicio_fabricacao=attr['inicio_fabricacao'],
                        fim_fabricacao=attr['fim_fabricacao'],
                        numero_unidade_producao=attr['numero_unidade_producao']
                    )
                    session.add(peca)
            elif tipo == 'SOPRADORA':
                for attr in atributos:
                    sopradora = SOPRADORA(
                        numero=attr['numero'],
                        vazao_sopro=attr['vazao_sopro'],
                        pressao_sopro=attr['pressao_sopro']
                    )
                    session.add(sopradora)
            elif tipo == 'FRESADORA':
                for attr in atributos:
                    fresadora = FRESADORA(
                        numero=attr['numero'],
                        velocidade_rotacao=attr['velocidade_rotacao'],
                        profundidade_corte=attr['profundidade_corte']
                    )
                    session.add(fresadora)
            elif tipo == 'TORNO_CNC':
                for attr in atributos:
                    torno_cnc = TORNO_CNC(
                        numero=attr['numero'],
                        velocidade_rotacao=attr['velocidade_rotacao'],
                        tolerancia=attr['tolerancia']
                    )
                    session.add(torno_cnc)
            elif tipo == 'IMPRESSORA_3D':
                for attr in atributos:
                    impressora_3d = IMPRESSORA_3D(
                        numero=attr['numero'],
                        espessura_camada=attr['espessura_camada'],
                        tipo_material=attr['tipo_material']
                    )
                    session.add(impressora_3d)

        session.commit()
