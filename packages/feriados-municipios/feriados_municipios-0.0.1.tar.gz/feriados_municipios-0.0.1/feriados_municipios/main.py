from datetime import date, timedelta
import traceback


class FeriadosBrasil:

    """
        Contém todos os estados do Brasil com municípios e feriados municipais.

        @vars:
            data (datetime.date): Data especificada no construtor da classe FeriadosBrasil, é um objeto date, e que se não for especificado terá a data do dia atual como valor padrão.
            meses_ptBR (dict): Dicionário com todos os meses traduzidos para o português. Seus índices começam do 1 até o 12 de maneira bem intuitiva.
    """

    data = None

    meses_ptBR = {
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
        12: "Dezembro",
    }

    dias_semana_ptBR = {
        1: "Domingo",
        2: "Segunda-Feira",
        3: "Terça-Feira",
        4: "Quarta-Feira",
        5: "Quinta-Feira",
        6: "Sexta-Feira",
        7: "Sábado",
    }

    class DataNaoEspecificada(Exception):
        """
        Exceção levantada quando alguma data não for especificada nas funções.
        """
        def __init__(self):
            self.message = "Data não especificada na função, especifique um dia e um mês."
            self.stack = traceback.extract_stack()[:-1]
            super().__init__(self.message)

        def __str__(self):
            if self.stack:
                # Extrai a última chamada da pilha, que é onde o erro ocorreu
                error_line = self.stack[-1]

            return f"<Traceback>\n\n\tOcorreu uma exceção do tipo DataNaoEspecificada.Exception\n------> {self.message}\n\n\tArquivo: {error_line.filename}\n\tFunção: {error_line.name}\n\tLinha> {error_line.lineno}\n\n<Traceback>"

    class NomeDataNaoEspecificado(Exception):
        """
        Exceção levantada quando algum nome não for especificada nas funções.
        """
        def __init__(self):
            self.message = "Nome não especificado na função, especifique o nome do feriado."
            self.stack = traceback.extract_stack()[:-1]
            super().__init__(self.message)

        def __str__(self):
            if self.stack:
                error_line = self.stack[-1]
            return f"<Traceback>\n\n\tOcorreu uma exceção do tipo NomeDataNaoEspecificado.Exception\n------> {self.message}\n\n\tArquivo: {error_line.filename}\n\tFunção: {error_line.name}\n\tLinha> {error_line.lineno}\n\n<Traceback>"

    @classmethod
    def __calcular_pascoa(cls):
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
    def __init__(cls, data: date = date.today()):
        cls.data = data

        data_pascoa = FeriadosBrasil.__calcular_pascoa()

        cls.feriados_nacionais = {
            (
                data_pascoa.day,
                data_pascoa.month,
            ): ["Páscoa", False],
            (1, 1): ["Confraternização Universal", False],
            (
                (data_pascoa - timedelta(47)).day,
                (data_pascoa - timedelta(47)).month,
            ): ["Véspera de Carnaval", False],
            (
                (data_pascoa - timedelta(46)).day,
                (data_pascoa - timedelta(46)).month,
            ): ["Carnaval", False],
            (
                (data_pascoa - timedelta(46)).day,
                (data_pascoa - timedelta(46)).month,
            ): ["Quarta-feira de Cinzas", True],
            (
                (data_pascoa - timedelta(2)).day,
                (data_pascoa - timedelta(2)).month,
            ): ["Sexta-feira Santa", False],
            (21, 4): ["Tiradentes", False],
            (1, 5): ["Dia do Trabalho", False],
            (
                (data_pascoa + timedelta(60)).day,
                (data_pascoa + timedelta(60)).month,
            ): ["Corpus Christi", False],
            (7, 9): ["Independência do Brasil", False],
            (2, 11): ["Finados", False],
            (15, 11): ["Proclamação da República", False],
            (24, 12): ["Véspera de Natal", True],
            (25, 12): ["Natal", False],
            (31, 12): ["Véspera de Ano Novo", True],
            (12, 10): ["Nossa Senhora Aparecida", False],
        }

    @classmethod
    def get_feriados_nacionais(cls):
        """
            Retorna uma lista com todos os feriados nacionais do Brasil.
        """
        dict_feriados_nacionais = []
        for feriado_nome in list(cls.feriados_nacionais.values()):
            dict_feriados_nacionais.append(feriado_nome[0])
        return dict_feriados_nacionais


    class __MG:
        feriados = None

        @classmethod
        def init(cls):
            """
            Função responsável por inicializar todas as variáveis de Municípios, atribuindo a cada município seus respectivos feriados.
            """
            cls.data = FeriadosBrasil.data

        @classmethod
        def get_data(cls):
            """
                Retorna a um data da instância no formato datetime.date.
            """
            return cls.data

        @classmethod
        def get_data_feriado(cls):
            """
                Retorna o dia e o mês da data da instância.

                Return: (dia, mes)
            """
            return (cls.data.day, cls.data.month)

        @classmethod
        def get_feriado(cls):
            """
                Retorna o nome do feriado do dia da instância. Caso não seja um feriado, retornará None.
            """
            if cls.feriados.get((cls.data.day, cls.data.month), None) is not None:
                return cls.feriados.get((cls.data.day, cls.data.month), None)[0]
            return None

        @classmethod
        def get_feriados(cls):
            """
                Retorna todos os feriados da instância.

                Return:
                dict_feriados (list): Lista de feriados.
            """
            dict_feriados = []
            for feriado_nome in list(cls.feriados.values()):
                dict_feriados.append(feriado_nome[0])
            return dict_feriados

        @classmethod
        def new_feriado_personalizado(cls, dia: int = None, mes: int = None, nome: str = None, facultativo = False):
            """
                Cria um novo feriado.

                @param:
                    dia (int): dia do feriado a ser criado
                    mes (int): mes do feriado a ser criado
                    nome (str): nome do feriado a ser criado
                    facultativo (bool): se o feriado é facultativo ou não
            """
            if (dia is None) | (mes is None):
                raise FeriadosBrasil.DataNaoEspecificada()

            if nome is None:
                raise FeriadosBrasil.NomeDataNaoEspecificado()

            try:
                dia = int(dia)
                mes = int(mes)
                nome = str(nome)
                facultativo = bool(facultativo)
            except:
                print("-")
                print("\tInsira valores válidos nos parâmetros de dia e mês da função ´set_feriado_as_facultativo_by_date´.")
                print("-")
                raise TypeError

            def __verificar_data(dia, mes, ano):
                def e_bissexto(ano):
                    # Função para verificar se o ano é bissexto
                    return (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)

                def dias_no_mes(mes, ano):
                    dias_por_mes = {
                        1: 31, 2: 29 if e_bissexto(ano) else 28, 3: 31,
                        4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
                        9: 30, 10: 31, 11: 30, 12: 31
                    }
                    return dias_por_mes.get(mes, 0)

                if 1 <= mes <= 12:
                    dias_maximos = dias_no_mes(mes, ano)
                    if 1 <= dia <= dias_maximos:
                        return True
                    else:
                        return False
                else:
                    return False

            if not __verificar_data(dia, mes, cls.data.year):
                print("\n<Traceback>\n\n\t @param: `dia` ou `mes` inválidos, verifique se o dia não ultrapassa o limite do mês especificado no argumento,\n\t ou se o mês especificado não ultrapassa a quantidade que um ano possa ter.\n\n<Traceback>")
                raise ValueError

            cls.feriados[(dia, mes)] = [nome, facultativo]

        @classmethod
        def is_feriado(cls) -> bool:
            """
                Retorna True se o dia da instância for feriado, e False caso não seja feriado.
            """
            return (
                True
                if cls.feriados.get((cls.data.day, cls.data.month)) is not None
                else False
            )

        @classmethod
        def is_feriado_na_data(cls, dia: int = None, mes:int = None) -> bool:
            """
                Retorna True se o dia passado no parâmetro for feriado, e False caso não seja feriado.

                @param:
                    dia(int): dia a ser verificado como feriado
                    mes(int): mes a ser verificado como feriado
            """
            if (dia is None) | (mes is None):
                raise FeriadosBrasil.DataNaoEspecificada()

            try:
                dia = int(dia)
                mes = int(mes)
            except:
                print("-")
                print("\tInsira valores válidos nos parâmetros de dia e mês da função ´set_feriado_as_facultativo_by_date´.")
                print("-")
                raise TypeError

            return (
                True
                if cls.feriados.get((dia, mes)) is not None
                else False
            )

        @classmethod
        def is_feriado_by_name(cls, nome_feriado: str = None) -> bool:
            """
                Retorna True se o nome do feriado passado for feriado de fato, e False caso não seja feriado ou caso esse feriado não seja encontrado.
            """
            if (nome_feriado is None):
                raise FeriadosBrasil.NomeDataNaoEspecificado()

            for feriado_nome in list(cls.feriados.values()):
                if feriado_nome[0] == str(nome_feriado):
                    return True
            return False

        @classmethod
        def get_feriados_regionais(cls):
            """
                Retorna uma lista com os nomes de todos os feriados regionais da classe especificada.

                Exemplo: FeriadosBrasil.GovernadorValadares.get_feriados_regionais() -> Feriados Municipais de Governador Valadares
            """
            dict_feriados = []
            for feriado_nome in list(cls.feriados_regionais.values()):
                dict_feriados.append(feriado_nome[0])
            return dict_feriados

        def get_feriados_nacionais():
            """
                Retorna uma lista com os nomes de todos os feriados nacionais.

                Exemplo: FeriadosBrasil.GovernadorValadares.get_feriados_nacionais() -> Feriados do Brasil
                ou FeriadosBrasil.get_feriados_nacionais() -> Feriados do Brasil
            """
            dict_feriados_nacionais = []
            for feriado_nome in list(FeriadosBrasil.feriados_nacionais.values()):
                dict_feriados_nacionais.append(feriado_nome[0])
            return dict_feriados_nacionais

        @classmethod
        def del_feriado(cls, feriado_deletar: str = None):
            """
                Deleta um feriado da lista de feriados da classe especificada.

                Exemplo: FeriadosBrasil.Ipatinga.del_feriado("Natal")

                @param:
                    feriado_deletar(str): Nome do feriado a ser deletado.
            """
            if feriado_deletar is None:
                raise FeriadosBrasil.NomeDataNaoEspecificado()

            if isinstance(feriado_deletar, str):
                cls.feriados = {
                    k: v for k, v in cls.feriados.items() if v[0] != str(feriado_deletar)
                }

        @classmethod
        def del_feriado_by_date(cls, dia, mes):
            """
                Deleta um feriado da lista de feriados da classe especificada através do dia e do mês.
                Será considerado sempre o ano da data passada na instância.

                Exemplo: FeriadosBrasil.Ipatinga.del_feriado(dia=31, mes=3)

                @param:
                    dia (int): Dia do feriado a ser deletado
                    mes (int): Mes do feriado a ser deletado
            """
            if (dia is None) | (mes is None):
                raise FeriadosBrasil.DataNaoEspecificada()

            try:
                dia = int(dia)
                mes = int(mes)
            except:
                print("-")
                print("\tInsira valores válidos nos parâmetros de dia e mês da função ´set_feriado_as_facultativo_by_date´.")
                print("-")
                raise TypeError

            if cls.feriados.get((dia, mes)) is not None:
                cls.feriados.pop((dia, mes))

        @classmethod
        def get_feriados_facultativos(cls):
            """
                Retorna uma lista de todos os feriados facultativos da classe especificada.

                Exemplo: FeriadosBrasil.Ipatinga.get_feriados_facultativos() -> Lista com os feriados facultativos.
            """
            dict_facultativos = {
                k: v for k, v in cls.feriados.items() if v[1] == True
            }

            nomes_feriados_facultativos = []
            for k, v in dict_facultativos.items():
                nomes_feriados_facultativos.append(v[0])

            return nomes_feriados_facultativos

        @classmethod
        def set_feriado_as_facultativo(cls, nome_feriado: str = None):
            """
                Seta um feriado existente para facultativo.

                @param:
                    nome_feriado (str): Nome do feriado a ser setado como facultativo.
            """
            if nome_feriado is None:
                raise FeriadosBrasil.NomeDataNaoEspecificado()

            for chave, valor in cls.feriados.items():
                if valor[0] == str(nome_feriado):
                    valor[1] = True

        @classmethod
        def unset_feriado_as_facultativo(cls, nome_feriado = None):
            """
                Seta um feriado existente para não facultativo.

                @param:
                    nome_feriado (str): Nome do feriado a ser setado como não facultativo.
            """
            if nome_feriado is None:
                raise FeriadosBrasil.NomeDataNaoEspecificado()

            for chave, valor in cls.feriados.items():
                if valor[0] == str(nome_feriado):
                    valor[1] = False

        @classmethod
        def set_feriado_as_facultativo_by_date(cls, dia: int = None, mes: int = None):
            """
                Seta um feriado existente para facultativo através do dia e do mes do feriado.

                @param:
                    dia (int): Dia do feriado a ser setado como facultativo.
                    mes (int): Mes do feriado a ser setado como facultativo.
            """
            if (dia is None) | (mes is None):
                raise FeriadosBrasil.DataNaoEspecificada()

            try:
                dia = int(dia)
                mes = int(mes)
            except:
                print("-")
                print("\tInsira valores válidos nos parâmetros de dia e mês da função ´set_feriado_as_facultativo_by_date´.")
                print("-")
                raise TypeError

            for chave, valor in cls.feriados.items():
                if (dia == chave[0]) & (mes == chave[1]):
                    valor[1] = True

        @classmethod
        def unset_feriado_as_facultativo_by_date(cls, dia = None, mes = None):
            """
                Seta um feriado existente para não facultativo através do dia e do mes do feriado.

                @param:
                    dia (int): Dia do feriado a ser setado como não facultativo.
                    mes (int): Mes do feriado a ser setado como não facultativo.
            """
            if (dia is None) | (mes is None):
                raise FeriadosBrasil.DataNaoEspecificada()

            try:
                dia = int(dia)
                mes = int(mes)
            except:
                print("-")
                print("\tInsira valores válidos nos parâmetros de dia e mês da função ´set_feriado_as_facultativo_by_date´.")
                print("-")
                raise TypeError

            for chave, valor in cls.feriados.items():
                if (dia == chave[0]) & (mes == chave[1]):
                    valor[1] = False

        @classmethod
        def del_all_feriados(cls):
            """
                Remove todos os feriados da classe especificada.
            """
            cls.feriados = dict()

    class GovernadorValadares(__MG):

        @classmethod
        def init(cls):
            """
                Inicializa todos feriados regionais de Governador Valadares.
            """
            super().init()
            cls.feriados_regionais = {
                (30, 1): ["Aniversário de Governador Valadares", False],
                (13, 6): ["Dia de Santo Antônio", False],
            }

            cls.feriados = FeriadosBrasil.feriados_nacionais | cls.feriados_regionais

    class Ipatinga(__MG):

        @classmethod
        def init(cls):
            """
                Inicializa todos feriados regionais de Ipatinga.
            """
            super().init()
            cls.feriados_regionais = {
                (29, 4): ["Aniversário de Ipatinga", False],
                (13, 6): ["Dia de Santo Antônio", False],
            }

            cls.feriados = FeriadosBrasil.feriados_nacionais | cls.feriados_regionais

    class CoronelFabriciano(__MG):

        @classmethod
        def init(cls):
            """
                Inicializa todos feriados regionais de Coronel Fabriciano.
            """
            super().init()
            cls.feriados_regionais = {
                (20, 1): ["Aniversário de Coronel Fabriciano", False],
                (21, 11): ["Dia de Nossa Senhora da Imaculada Conceição", False],
            }

            cls.feriados = FeriadosBrasil.feriados_nacionais | cls.feriados_regionais

    class JuizDeFora(__MG):

        @classmethod
        def init(cls):
            """
                Inicializa todos feriados regionais de Juiz de Fora.
            """
            super().init()
            cls.feriados_regionais = {
                (31, 7): ["Dia de São João Nepomuceno", False],
                (23, 11): ["Aniversário de Juiz de Fora", False],
            }

            cls.feriados = FeriadosBrasil.feriados_nacionais | cls.feriados_regionais
