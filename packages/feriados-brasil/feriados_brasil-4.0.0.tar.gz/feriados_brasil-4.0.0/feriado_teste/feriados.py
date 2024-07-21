from datetime import date, timedelta

class FeriadosBrasil:
    """
    Classe que contém cidades de Minas Gerais
    """
    data = None
    meses_pt_br = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }
    #todo -> Usar o indice a partir do 0 ou do 1?
    dias_semana_pt_br = {
        0: "Domingo",
        1: "Segunda-Feira",
        2: "Terça-Feira",
        3: "Quarta-Feira",
        4: "Quinta-Feira",
        5: "Sexta-Feira",
        6: "Sábado"
    }

    @classmethod
    def calcular_pascoa(cls):
        "Retorna a data da Páscoa para um dado ano usando o algoritmo de computus"

        ano = cls.data.year

        a = ano % 19
        b = ano // 100
        c = ano % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mes = (h + l - 7 * m + 114) // 31
        dia = ((h + l - 7 * m + 114) % 31) + 1

        data_pascoa = date(ano, mes, dia)
        return data_pascoa

    @classmethod
    def __init__(cls, data: date):
        cls.data = data

        # calc_data = date(data.year, FeriadosBrasil.calcular_pascoa()[1], FeriadosBrasil.calcular_pascoa()[0])

        cls.feriados_nacionais = {
            (FeriadosBrasil.calcular_pascoa().day, FeriadosBrasil.calcular_pascoa().month): "Páscoa",
            (1, 1): "Confraternização Universal",
            FeriadosBrasil.calcular_pascoa() - timedelta(47): "Carnaval", #vai cair na segunda
            FeriadosBrasil.calcular_pascoa() - timedelta(46): "Carnaval", # vai cair na terça (descobrir porque tem 2 carnavais)
            FeriadosBrasil.calcular_pascoa() - timedelta(46): "Quarta-feira de Cinzas (Ponto facultativo até meio-dia)",
            FeriadosBrasil.calcular_pascoa() - timedelta(2): "Sexta-feira Santa",
            (21, 4): "Tiradentes",
            (1, 5): "Dia do Trabalho",
            FeriadosBrasil.calcular_pascoa() - timedelta(60): "Corpus Christi",
            (7, 9): "Independência do Brasil",
            (2, 11): "Finados",
            (15, 11): "Proclamação da República",
            (24, 12): "Véspera de Natal (Ponto facultativo a partir do meio-dia)",
            (25, 12): "Natal",
            (31, 12): "Véspera de Ano Novo (Ponto facultativo a partir do meio-dia)",
            (12, 10): "Nossa Senhora Aparecida",
        }

    @classmethod
    def get_feriados_nacionais(cls):
        return list(cls.feriados_nacionais.values())

    class __MG:
        feriados = None

        @classmethod
        def init(cls):
            cls.data = FeriadosBrasil.data

        @classmethod
        def get_data(cls):
            return cls.data

        @classmethod
        def get_data_feriado(cls):
            return (cls.data.day, cls.data.month)

        @classmethod
        def get_feriado(cls):
            return cls.feriados.get((cls.data.day, cls.data.month), None)

        @classmethod
        def get_feriados(cls):
            return list(cls.feriados.values())

        @classmethod
        def set_feriado_personalizado(cls, dia, mes, nome):
            cls.feriados[(dia, mes)] = nome
            return cls.feriados

        @classmethod
        def is_feriado(cls) -> bool:
            # Vai retornar um booleano dizendo se a data de hoje é feriado ou nao
            # vai permitir especificar uma data, caso nao seja epecificada, vai considearar a que foi colocada no initialize, caso nao seja especificada no initalizee vai considerar a de hoje (fazer essa mesma logica pro restante dos metodos)
            # return cls.feriados.get((cls.data.day, cls.data.month), "Não é um feriado")
            return True if cls.feriados.get((cls.data.day, cls.data.month)) != None else False
            ...

        @classmethod
        def get_feriados_regionais(cls):
            return list(cls.feriados_regionais.values())

        def get_feriados_nacionais():
            return list(FeriadosBrasil.feriados_nacionais.values())

        # todo decidir qual dos 2
        def del_feriado():
            ...

        def considerar_facultativo():
            ...

    class GovernadorValadares(__MG):

        @classmethod
        def init(cls):
            super().init()
            cls.feriados_regionais = {
                (30, 1): "Aniversário de Governador Valadares",
                (13, 6): "Dia de Santo Antônio"
            }

            cls.feriados = FeriadosBrasil.feriados_nacionais | cls.feriados_regionais
