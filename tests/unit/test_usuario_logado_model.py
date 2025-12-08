"""
Testes para o modelo UsuarioLogado (model/usuario_logado_model.py)

Testa todos os métodos do dataclass UsuarioLogado incluindo
verificação de perfis, serialização e desserialização.
"""

import pytest
from unittest.mock import MagicMock

from model.usuario_logado_model import UsuarioLogado
from util.perfis import Perfil


class TestUsuarioLogadoInstanciacao:
    """Testes de criação de instâncias"""

    def test_criar_usuario_logado(self):
        """Deve criar instância com todos os campos"""
        usuario = UsuarioLogado(
            id=1,
            nome="João Silva",
            email="joao@teste.com",
            perfil=Perfil.AUTOR.value
        )

        assert usuario.id == 1
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@teste.com"
        assert usuario.perfil == "autor"

    def test_usuario_logado_imutavel(self):
        """UsuarioLogado deve ser imutável (frozen=True)"""
        usuario = UsuarioLogado(
            id=1,
            nome="João",
            email="joao@teste.com",
            perfil=Perfil.AUTOR.value
        )

        with pytest.raises(AttributeError):
            usuario.nome = "Novo Nome"


class TestIsAdmin:
    """Testes para o método is_admin()"""

    def test_admin_retorna_true(self):
        """Admin deve retornar True"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_admin() is True

    def test_autor_retorna_false(self):
        """autor não deve ser admin"""
        autor = UsuarioLogado(
            id=1,
            nome="autor",
            email="autor@teste.com",
            perfil=Perfil.AUTOR.value
        )

        assert autor.is_admin() is False

    def test_LEITOR_retorna_false(self):
        """LEITOR não deve ser admin"""
        LEITOR = UsuarioLogado(
            id=1,
            nome="LEITOR",
            email="LEITOR@teste.com",
            perfil=Perfil.LEITOR.value
        )

        assert LEITOR.is_admin() is False


class TestIsautor:
    """Testes para o método is_autor()"""

    def test_autor_retorna_true(self):
        """autor deve retornar True"""
        autor = UsuarioLogado(
            id=1,
            nome="autor",
            email="autor@teste.com",
            perfil=Perfil.AUTOR.value
        )

        assert autor.is_autor() is True

    def test_admin_retorna_false(self):
        """Admin não deve ser autor"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_autor() is False

    def test_LEITOR_retorna_false(self):
        """LEITOR não deve ser autor"""
        LEITOR = UsuarioLogado(
            id=1,
            nome="LEITOR",
            email="LEITOR@teste.com",
            perfil=Perfil.LEITOR.value
        )

        assert LEITOR.is_autor() is False


class TestIsLEITOR:
    """Testes para o método is_LEITOR()"""

    def test_LEITOR_retorna_true(self):
        """LEITOR deve retornar True"""
        LEITOR = UsuarioLogado(
            id=1,
            nome="LEITOR",
            email="LEITOR@teste.com",
            perfil=Perfil.LEITOR.value
        )

        assert LEITOR.is_LEITOR() is True

    def test_admin_retorna_false(self):
        """Admin não deve ser LEITOR"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_LEITOR() is False

    def test_autor_retorna_false(self):
        """autor não deve ser LEITOR"""
        autor = UsuarioLogado(
            id=1,
            nome="autor",
            email="autor@teste.com",
            perfil=Perfil.AUTOR.value
        )

        assert autor.is_LEITOR() is False


class TestTemPerfil:
    """Testes para o método tem_perfil()"""

    def test_tem_perfil_unico(self):
        """Deve retornar True quando tem o perfil"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.tem_perfil(Perfil.ADMIN.value) is True

    def test_nao_tem_perfil(self):
        """Deve retornar False quando não tem o perfil"""
        autor = UsuarioLogado(
            id=1,
            nome="autor",
            email="autor@teste.com",
            perfil=Perfil.AUTOR.value
        )

        assert autor.tem_perfil(Perfil.ADMIN.value) is False

    def test_tem_perfil_multiplos(self):
        """Deve retornar True quando tem um dos perfis"""
        LEITOR = UsuarioLogado(
            id=1,
            nome="LEITOR",
            email="LEITOR@teste.com",
            perfil=Perfil.LEITOR.value
        )

        # LEITOR está na lista
        assert LEITOR.tem_perfil(
            Perfil.ADMIN.value,
            Perfil.LEITOR.value
        ) is True

    def test_nao_tem_nenhum_perfil(self):
        """Deve retornar False quando não tem nenhum dos perfis"""
        autor = UsuarioLogado(
            id=1,
            nome="autor",
            email="autor@teste.com",
            perfil=Perfil.AUTOR.value
        )

        # autor não é admin nem LEITOR
        assert autor.tem_perfil(
            Perfil.ADMIN.value,
            Perfil.LEITOR.value
        ) is False


class TestToDict:
    """Testes para o método to_dict()"""

    def test_converte_para_dict(self):
        """Deve converter para dicionário"""
        usuario = UsuarioLogado(
            id=42,
            nome="Teste",
            email="teste@email.com",
            perfil="autor"
        )

        resultado = usuario.to_dict()

        assert resultado == {
            "id": 42,
            "nome": "Teste",
            "email": "teste@email.com",
            "perfil": "autor"
        }


class TestFromDict:
    """Testes para o método from_dict()"""

    def test_cria_de_dict_completo(self):
        """Deve criar instância de dicionário completo"""
        dados = {
            "id": 1,
            "nome": "João",
            "email": "joao@email.com",
            "perfil": "autor"
        }

        usuario = UsuarioLogado.from_dict(dados)

        assert usuario is not None
        assert usuario.id == 1
        assert usuario.nome == "João"
        assert usuario.email == "joao@email.com"
        assert usuario.perfil == "autor"

    def test_retorna_none_para_none(self):
        """Deve retornar None quando data é None"""
        resultado = UsuarioLogado.from_dict(None)

        assert resultado is None

    def test_levanta_erro_campo_faltando(self):
        """Deve levantar ValueError quando campo está faltando"""
        dados_incompletos = {
            "id": 1,
            "nome": "João",
            # falta email e perfil
        }

        with pytest.raises(ValueError) as exc_info:
            UsuarioLogado.from_dict(dados_incompletos)

        assert "Campos obrigatórios ausentes" in str(exc_info.value)

    def test_levanta_erro_mostra_campos_faltantes(self):
        """Mensagem de erro deve mostrar quais campos faltam"""
        dados_incompletos = {
            "id": 1,
            "nome": "João",
            "email": "joao@email.com"
            # falta perfil
        }

        with pytest.raises(ValueError) as exc_info:
            UsuarioLogado.from_dict(dados_incompletos)

        assert "perfil" in str(exc_info.value)


class TestFromUsuario:
    """Testes para o método from_usuario()"""

    def test_cria_de_usuario(self):
        """Deve criar UsuarioLogado de objeto Usuario"""
        # Mock do objeto Usuario
        usuario_mock = MagicMock()
        usuario_mock.id = 123
        usuario_mock.nome = "Maria"
        usuario_mock.email = "maria@email.com"
        usuario_mock.perfil = "LEITOR"

        usuario_logado = UsuarioLogado.from_usuario(usuario_mock)

        assert usuario_logado.id == 123
        assert usuario_logado.nome == "Maria"
        assert usuario_logado.email == "maria@email.com"
        assert usuario_logado.perfil == "LEITOR"
