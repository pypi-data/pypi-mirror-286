import sqlite3 as sq
import hashlib as sh
from deprecated import deprecated
import os

class SQLITE:
    '''
    Faça a gestão dos seus bancos de dados com esta classe.
    
    Importe a classe e use um dos métodos abaixo:
    ```python
    # Importando a classe
    from manage-sql import SQLITE
    
    # Instacioando a classe
    db = SQLITE('nome_do_banco')
    
    # Usar cada um dos metodos:
    db.criarTabela()
    db.inserirDados()
    db.apagarDados()
    db.editarDados()
    db.adicionarColuna()
    db.apagarColuna()
    db.apagarTabela()
    db.verDados()
    db.encriptarValor()
    ```
    
    Funções descontinuadas
    ```python
    # Encriptar valores
    db.encryptPass() # Função antiga
    db.encriptarValor() # Nova função
    
    # Consultar dados
    db.verDadosPlus() # Função antiga
    db.verDados() # Função em uso
    ```
    '''

    def __init__(self, nomeBanco: str):
        """
        Inicializa a classe com o nome do banco de dados.
        
        :param nomeBanco: Nome do banco de dados a ser utilizado.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco)
        ```
        """
        
        self.nomeBanco = nomeBanco

    @property
    def numeroTabelas(self) -> int:
        return self._numeroTabelas
    
    @property
    def nomeTabelas(self) -> list:
        return self._nomeTabelas
    
    def conectarBanco(self):
        """
        Conecta ao banco de dados e cria a pasta 'database' se não existir.

        :return: Um objeto de conexão e cursor do banco de dados.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        database, cursor = db.conectarBanco()
        ```
        """
        try:
            path = rf'{os.getcwd()}\database'
            os.mkdir(path)
        except:
            pass
        
        database = sq.connect(f'database/{self.nomeBanco}.db')
        cursor = database.cursor()

        return database, cursor

    def criarTabela(self, nomeTabela: str, Colunas: list, ColunasTipo: list):
        """
        Cria uma tabela no banco de dados.

        :param nomeTabela: Nome da tabela a ser criada.
        :param Colunas: Lista com os nomes das colunas.
        :param ColunasTipo: Lista com os tipos das colunas.

        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.criarTabela(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            ColunasTipo=['TEXT', 'INTEGER']
        )
        ```
        """
        if type(Colunas) == list and type(ColunasTipo) == list:
            if len(Colunas) == len(ColunasTipo):
                database, cursor = self.conectarBanco()
                ListaColunas = []

                for i in range(len(Colunas)):
                    ListaColunas.append(f'{Colunas[i]} {ColunasTipo[i]}')

                ColunaSQL = ','.join(ListaColunas)

                cursor.execute(f'CREATE TABLE IF NOT EXISTS {nomeTabela} (id INTEGER PRIMARY KEY AUTOINCREMENT,{ColunaSQL})')

                database.commit()
                database.close()
            else:
                print('Impossível criar tabelas: quantidade de colunas e tipos não coincide.')
        else:
            print('Impossível criar tabelas: parâmetros devem ser listas.')

    def inserirDados(self, nomeTabela: str, Colunas: list, dados: list):
        """
        Insere dados em uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde os dados serão inseridos.
        :param Colunas: Lista com os nomes das colunas.
        :param dados: Lista com os valores a serem inseridos.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.inserirDados(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            dados=['valor1', 123]
        )
        ```
        """
        if type(Colunas) == list and type(dados) == list:
            if len(Colunas) == len(dados):
                database, cursor = self.conectarBanco()

                ColunaSQL = ', '.join(Colunas)

                params = ', '.join('?' for _ in dados)

                cursor.execute(f'INSERT INTO {nomeTabela} ({ColunaSQL}) VALUES ({params})', (dados))

                database.commit()
                database.close()
            else:
                print('Impossível inserir dados: quantidade de colunas e valores não coincide.')
        else:
            print('Impossível inserir dados: parâmetros devem ser listas.')

    def apagarDados(self, nomeTabela: str, conditions: str = ''):
        """
        Apaga registros de uma tabela no banco de dados SQLite.

        :param nomeTabela: Nome da tabela da qual os dados serão apagados.
        :param conditions: Condição SQL para selecionar os registros a serem apagados. Se vazio, todos os registros serão apagados.
        
        Exemplo de uso:
        
        ```python
        db = SQLITE('meu_banco')
        
        # Apaga registros com id = 1
        db.apagarDados("minha_tabela", "id = 1")
        
        # Apaga todos os registros da tabela
        db.apagarDados("minha_tabela")
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'DELETE FROM {nomeTabela}')
        
        else:
            cursor.execute(f'DELETE FROM {nomeTabela} WHERE {conditions}')
        
        database.commit()
        database.close()

    def editarDados(self, nomeTabela: str, Coluna: str, Valor: str, conditions: str = ''):
        """
        Edita registros em uma tabela no banco de dados SQLite.

        :param nomeTabela: Nome da tabela a ser editada.
        :param Coluna: Nome da coluna a ser editada.
        :param Valor: Novo valor a ser atribuído à coluna.
        :param conditions: Condição SQL para selecionar os registros a serem editados. Se vazio, todos os registros serão atualizados.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        
        # Edita registros com id = 1
        db.editarDados("minha_tabela", "nome_coluna", "novo_valor", "id = 1")
        
        # Edita todos os registros da tabela
        db.editarDados("minha_tabela", "nome_coluna", "novo_valor")
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = ?", (Valor,))
        
        else:
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = ? WHERE {conditions}", (Valor,))
        
        database.commit()
        database.close()

    def adicionarColuna(self, nomeTabela: str, Coluna: str, ColunaTipo: str):
        """
        Adiciona uma nova coluna a uma tabela no banco de dados SQLite.

        :param nomeTabela: Nome da tabela na qual a coluna será adicionada.
        :param Coluna: Nome da nova coluna.
        :param ColunaTipo: Tipo de dados da nova coluna (por exemplo, INTEGER, TEXT).
        
        Exemplo de uso:
        ```python
        db_manager = DatabaseManager()
        
        # Adiciona uma coluna do tipo TEXT
        db_manager.adicionarColuna("minha_tabela", "nova_coluna", "TEXT")```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} ADD COLUMN {Coluna} {ColunaTipo}')

        database.commit()
        database.close()
    
    def apagarColuna(self, nomeTabela: str, Coluna: str):
        """
        Apaga uma coluna de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde a coluna será apagada.
        :param Coluna: Nome da coluna a ser apagada.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.apagarColuna('minha_tabela', 'coluna2')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} DROP COLUMN {Coluna}')

        database.commit()
        database.close()

    def apagarTabela(self, nomeTabela: str):
        """
        Apaga uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser apagada.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.apagarTabela('minha_tabela')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'DROP TABLE IF EXISTS {nomeTabela}')

        database.commit()
        database.close()

    def verDados(self, nomeTabela: str, conditions: str = '', colunas: str = '*'):
        """
        Consulta dados de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser consultada.
        :param conditions: Condições para a consulta (opcional).
        :param colunas: Colunas a serem selecionadas (opcional).
        :return: Dados consultados.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        dados = db.verDados('minha_tabela')
        print(dados)
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela}')
        else:
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela} WHERE {conditions}')

        dados = cursor.fetchall()

        database.commit()
        database.close()

        return dados
    
    @deprecated(reason='Esta função vai ser descontinuada na versão 0.4.0. Considere usar função verDados()')
    def verDadosPlus(self, query: str, params: list):
        """
        Consulta dados com base em uma query SQL customizada.

        :param query: Query SQL a ser executada.
        :param params: Parâmetros para a query SQL.
        :return: Dados consultados.
        
        ```python
        db = SQLITE('meu_banco')
        query = "SELECT * FROM minha_tabela WHERE coluna1 = ? AND coluna2 = ?"
        params = ['valor1', 123]
        dados = db.verDadosPlus(query, params)
        print(dados)
        ```
        """
        database, cursor = self.conectarBanco()
        
        cursor.execute(query, params)
        dados = cursor.fetchall()
        
        database.commit()
        database.close()
        
        return dados

    @deprecated(reason='Esta função vai ser descontinuada na versão 0.4.0. Considere usar a função encriptarValor()')
    def encryptPass(self, value: str):
        """
        Gera um hash SHA-512 de um valor fornecido.

        :param value: Valor a ser criptografada.
        :return: Valor criptografado em SHA-512.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        value_hashed = db.encryptPass('minha_senha')
        print(value_hashed)
        ```
        """
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        value_hashed = hash.hexdigest()

        return value_hashed
    
    def encriptarValor(self, value: str):
        """
        Gera um hash SHA-512 de um valor fornecido.

        :param value: Valor a ser criptografada.
        :return: Valor criptografado em SHA-512.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        value_hashed = db.encryptValor('valor')
        print(value_hashed)
        ```
        """
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        value_hashed = hash.hexdigest()

        return value_hashed
    
    @property
    def _nomeTabelas(self):
        database, cursor = self.conectarBanco()
        rows = []
        
        tables = cursor.execute(
            'SELECT name FROM sqlite_master WHERE type = "table"'
        ).fetchall()
        
        database.close()
        
        for row in tables:
            if row[0] != 'sqlite_sequence':
                rows.append(row[0])
        
        return rows
    
    @property
    def _numeroTabelas(self):
        database, cursor = self.conectarBanco()
        
        number = cursor.execute(
            'SELECT COUNT(name) FROM sqlite_master WHERE type = "table"'
        ).fetchone()[0] - 1
        
        database.close()
        
        return number
    
    def totalLinhas(self, nomeTabela: str):
        database, cursor = self.conectarBanco()
        
        number: int = cursor.execute(
            f'SELECT COUNT("*") FROM {nomeTabela}'
        ).fetchone()[0]
        
        database.close()
        
        return number
    
    def ultimaLinha(self, nomeTabela: str):
        id = self.totalLinhas(nomeTabela)
        database, cursor = self.conectarBanco()
        
        if id != 0:
            lastrow: list = cursor.execute(
                f'SELECT * FROM {nomeTabela} WHERE id ="{id}"'
            ).fetchone()
            
            database.close()
            
            return lastrow
        
        else:
            database.close()
            
            return id
    
    def numeroColunas(self, nomeTabela: str):
        database, cursor = self.conectarBanco()
        
        number = cursor.execute(
            f'PRAGMA table_info({nomeTabela})'
        ).fetchall()
        
        database.close()
        
        return len(number)
    
    def nomeColunas(self, nomeTabela: str):
        database, cursor = self.conectarBanco()
        
        rows = cursor.execute(
            f'PRAGMA table_info({nomeTabela})'
        ).fetchall()
        
        database.close()
        
        return [row[1] for row in rows]


if __name__ == '__main__':

    """
    Nesta secção vamos ver exemplo de como implementar cada função desta biblioteca
    """
    
    # Criando a conexão com o banco de dados
    db = SQLITE('usuarios')
    
    # Criando as variáveis necessárias
    nomebela = 'usuarios'
    colunas = {
        'nome': 'TEXT',
        'usuario': 'TEXT',
        'senha': 'TEXT',
    }
    
    dados = {
        'nome': 'Alexandre Zunguze',
        'usuario': 'azunguze',
        'senha': 'Aa123'
    }
    
    # db.criarTabela()
    db.criarTabela(
        nomeTabela=nomebela,
        Colunas=[col for col in colunas],
        ColunasTipo=[col for col in colunas.values()]
    )
    
    # db.inserirDados()
    for _ in range(3):
        db.inserirDados(
            nomeTabela=nomebela,
            Colunas=[col for col in dados],
            dados=[dado for dado in dados.values()]
        )
    
    # db.apagarDados()
    db.apagarDados(
        nomeTabela=nomebela,
        conditions='id = 3'
    )
    
    # db.editarDados()
    db.editarDados(
        nomeTabela=nomebela,
        Coluna=list(colunas.keys())[2],
        Valor=db.encriptarValor('Aa123')
    )
    
    db.editarDados(
        nomeTabela=nomebela,
        Coluna=list(colunas.keys())[2],
        Valor=db.encriptarValor('Aa123'),
        conditions='id = 2'
    )
    
    # db.adicionarColuna()
    db.adicionarColuna(
        nomeTabela=nomebela,
        Coluna='email',
        ColunaTipo='TEXT'
    )
    
    # db.apagarColuna()
    db.apagarColuna(
        nomeTabela=nomebela,
        Coluna='email'
    )
    
    # db.verDados()
    dados_1 = db.verDados(
        nomeTabela=nomebela
    )
    
    dados_2 = db.verDados(
        nomeTabela=nomebela,
        conditions='id = 1'
    )
    
    dados_3 = db.verDadosPlus(
        query=f'SELECT * FROM {nomebela} WHERE id = ?',
        params=[1]
    ) # Descontinuado, será desativado na versão 0.4.0
    
    print(f'dados 1:{dados_1}\ndados 2: {dados_2}\ndados 3:{dados_3}')
    
    # db.encryptPass()
    print(
        db.encryptPass(
            value='Aa123'
        ) # Descontinuado, será apagado na verão 0.4.0
    )
    
    # db.numeroTabelas
    print(f'numero de tabelas: {db.numeroTabelas}')
    
    # db.nomeTabelas
    print(f'nome tabelas: {db.nomeTabelas}')
    
    # db.numeroLinhas()
    print(
        f'numero linhas: {db.totalLinhas(nomeTabela=nomebela)}'
    )
    
    # db.ultimaLinha()
    print(
        f'ultima linha: {db.ultimaLinha(nomeTabela=nomebela)}'
    )
    
    # db.numeroColunas()
    print(f'numero de colunas: {db.numeroColunas(nomeTabela=nomebela)}')
    
    # db.nomeColunas()
    print(f'nome de colunas: {db.nomeColunas(nomeTabela=nomebela)}')
    
    # Apagador todos dados
    db.apagarDados(
        nomeTabela=nomebela
    )
    
    # db.apagarTabela()
    db.apagarTabela(
        nomeTabela=nomebela
    )
    
    # apagar a database
    os.remove(rf'{os.getcwd()}\database\usuarios.db')