from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class StatusCarregador(str, Enum):
    DISPONIVEL = "Disponível"
    EM_USO = "Em Uso"
    MANUTENCAO = "Manutenção"
    FORA_DE_SERVICO = "Fora de Serviço"


class TipoConector(str, Enum):
    TYPE2 = "Tipo 2 (IEC 62196)"
    CCS2 = "CCS Combo 2"
    CHADEMO = "CHAdeMO"
    GB_T = "GB/T"


class ConsultaRecarga(BaseModel):
    ponto_id: str = Field(description="Identificador único do ponto de recarga GoodWe/ChargeGrid")
    modelo_carregador: str = Field(description="Modelo do carregador GoodWe (ex: HCA Series, GW11K-HCA)")
    status: StatusCarregador = Field(description="Estado atual de operação do carregador")
    potencia_kw: float = Field(description="Potência nominal do carregador em kW")
    conector_tipo: TipoConector = Field(description="Tipo de conector padrão do equipamento")
    taxa_kwh: float = Field(description="Valor cobrado por kWh em BRL")
    mensagem_usuario: str = Field(description="Resumo da orientação fornecida ao usuário")
    requer_tecnico: bool = Field(default=False, description="Indica se há falha elétrica exigindo suporte especializado")

    @field_validator("potencia_kw")
    @classmethod
    def validar_potencia(cls, v: float) -> float:
        if v <= 0 or v > 350:
            raise ValueError("A potência do carregador EV deve estar entre 0.1 kW e 350 kW.")
        return round(v, 2)

    @field_validator("taxa_kwh")
    @classmethod
    def validar_taxa(cls, v: float) -> float:
        if v < 0:
            raise ValueError("A taxa por kWh não pode ser negativa.")
        return round(v, 2)


class RespostaChatbot(BaseModel):
    resposta_texto: str = Field(description="Resposta explicativa em linguagem natural para o usuário")
    dados_estruturados: Optional[ConsultaRecarga] = Field(default=None, description="Dados parseados caso seja consulta de estação")
    fora_de_escopo: bool = Field(default=False, description="Flag indicando se a pergunta violou o escopo GoodWe")
    alerta_seguranca: bool = Field(default=False, description="Flag ativada para recusa de manipulação elétrica/risco físico")
