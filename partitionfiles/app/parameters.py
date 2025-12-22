
import pandas as pd
import base64

# Variáveis
list_columns_invalids = ["id","cliente","pais","ext","tel","std", "obs","cep","numeros","tam","tel_fmt", "status"]

ddds_brasil = [
    "11",  # SP - São Paulo (capital e região metropolitana)
    "12",  # SP - Vale do Paraíba
    "13",  # SP - Baixada Santista
    "14",  # SP - Bauru e região
    "15",  # SP - Sorocaba e região
    "16",  # SP - Ribeirão Preto e região
    "17",  # SP - São José do Rio Preto
    "18",  # SP - Presidente Prudente e região
    "19",  # SP - Campinas e região

    "21",  # RJ - Rio de Janeiro (capital)
    "22",  # RJ - Norte Fluminense
    "24",  # RJ - Sul Fluminense

    "27",  # ES - Grande Vitória
    "28",  # ES - Sul do Espírito Santo

    "31",  # MG - Belo Horizonte e região
    "32",  # MG - Zona da Mata
    "33",  # MG - Leste de Minas
    "34",  # MG - Triângulo Mineiro
    "35",  # MG - Sul de Minas
    "37",  # MG - Centro-Oeste de Minas
    "38",  # MG - Norte de Minas

    "41",  # PR - Curitiba e região
    "42",  # PR - Centro-Sul do Paraná
    "43",  # PR - Norte do Paraná
    "44",  # PR - Noroeste do Paraná
    "45",  # PR - Oeste do Paraná
    "46",  # PR - Sudoeste do Paraná

    "47",  # SC - Norte de Santa Catarina
    "48",  # SC - Grande Florianópolis e Sul
    "49",  # SC - Oeste de Santa Catarina

    "51",  # RS - Porto Alegre e região
    "53",  # RS - Sul do Rio Grande do Sul
    "54",  # RS - Serra Gaúcha
    "55",  # RS - Noroeste Gaúcho

    "61",  # DF - Brasília
    "62",  # GO - Goiânia e região
    "63",  # TO - Tocantins
    "64",  # GO - Sul de Goiás

    "65",  # MT - Cuiabá e região
    "66",  # MT - Interior de Mato Grosso
    "67",  # MS - Mato Grosso do Sul

    "68",  # AC - Acre
    "69",  # RO - Rondônia

    "71",  # BA - Salvador e região
    "73",  # BA - Sul da Bahia
    "74",  # BA - Norte da Bahia
    "75",  # BA - Centro-Norte da Bahia
    "77",  # BA - Oeste da Bahia

    "79",  # SE - Sergipe

    "81",  # PE - Recife e região
    "82",  # AL - Alagoas
    "83",  # PB - Paraíba
    "84",  # RN - Rio Grande do Norte
    "85",  # CE - Fortaleza e região
    "86",  # PI - Norte do Piauí
    "87",  # PE - Interior de Pernambuco
    "88",  # CE - Sul do Ceará
    "89",  # PI - Sul do Piauí

    "91",  # PA - Belém e região
    "92",  # AM - Manaus e região
    "93",  # PA - Oeste do Pará
    "94",  # PA - Sudeste do Pará
    "95",  # RR - Roraima
    "96",  # AP - Amapá
    "97",  # AM - Interior do Amazonas
    "98",  # MA - São Luís e região
    "99",  # MA - Interior do Maranhão
]

sujeira = ['99 99999999999'
            , '011 0000000000'
            , '5555560000000'
            , '11 1111111111 '
            , '5555555555555'
            , '(81)00000-0000'
            , '2100000000'
            , '3100000000'
            , '7190000000'
            , '47900000000'
            , '(11)00000-0000'
            , '(21)0000-0000'
            , '(22)00000-0001'
            , '(31)00000-0000'
            , '(48)00000-0000'
            , '(51)00000-0000'
            , '(61)00000-0000'
            , '(62)0000-0000'
            , '(62)00000-0000'
            , '(71)00000-0000'
            , '(80)00000-0000'
            , '(85)00000-0000'
            , '(88)00000-0000'
            , '(91)00000-0000'
            , '10 000000000'
            , '11 00000000'
            , '11 000000000'
            , '11 00000001'
            , '11 00400000'
            , '11 90000000'
            , '12 00000000'
            , '12 00000001'
            , '13 00000000'
            , '15 00000000'
            , '16 00000000'
            , '16 000000000'
            , '17 00000000'
            , '18 00000000'
            , '19 00000000'
            , '21 00000000'
            , '21 000000000'
            , '21 000000007'
            , '22 00006072'
            , '23 00007852'
            , '24 00000000'
            , '31 00000000'
            , '31 000000000'
            , '32 00000000'
            , '34 00000000'
            , '35 000000000'
            , '35 00000181'
            , '41 00000000'
            , '41 000000000'
            , '41 04020000'
            , '41 104020000'
            , '41 125530000'
            , '43 07800000'
            , '43 12960000'
            , '44 18700000'
            , '45 00000000'
            , '47 00000000'
            , '47 000000000'
            , '47 00000003'
            , '48 00000000'
            , '48 000000000'
            , '50 00002454'
            , '51 00000000'
            , '51 00000001'
            , '56 00001819'
            , '61 00000000'
            , '62 00000000'
            , '62 000000000'
            , '62 00000008'
            , '62 00000088'
            , '63 00004798'
            , '71 00000000'
            , '75 000000000'
            , '80 00000000'
            , '80 000001213'
            , '81 00000000'
            , '81 000000000'
            , '85 00000000'
            , '85 000000000'
            , '85 00000001'
            , '85 00000002'
            , '85 00000325'
            , '88 00000000'
            , '91 00000000'
            , '91 000000000'
            , '91 000000001'
            , '91 90000000'
            , '92 00000000'
            , '98 00000000'
            , '(11)9999-9999'
            , '(11)1111-1111'
            , '(11)1234-5678'
            , '62 900000000'
            , '48 30000000'
            , '31 30000000'
            , '30 30000000'
            , '91900000000'
            , '21 20000000'
            , '92 20000000'
            , '61 30000000'
            , '11 970000000'
            , '84 900000000'
            , '81 900000000'
            , '79 30000000'
            , '16 900000000'
            , '79 990000000'
            , '21 900000000'
            , '34 900000000'
            , '19 20000000'
            , '51 30000000'
            , '85 900000000'
            , '11 900000000'
            , '22 30000000'
            , '99999999999'
            , '98 999999999'
            , '99 999999999'
            , '98 911111111'
            , '15 55555555'
            , '16 55555555'
            , '(08)0028-3161'
            , '08 00722346'
            , '000- 000-000'
            , '41 0000000'
            , '00- 000-0000'
            , '31 9000000'
            , '(11)2345-678'
            , '81  9000000'
            , '85  0000000'
            , '21  0000000'
            , '31  0000000'
            , '51  3000000'
            , '48  0000000'
            , '9 90000000'
            , '9 98100000'
            , '3 63100000'
            , '000-000-000'
            , '9 99999999'
            , '99 9999999'
            , '99  9999999'
            , '0 00000000'
            , '00  0000000'
            , '00-0000-0003'
            , '47900000000'
            , '5555555555555'
            , '11 1111111111'
            , '551199999999'
            , '0047900000000'
            , '271007100000'
            , '000000000000000'
]

# De Para Telefones
de_para_telefones = []
de_para_telefones.append({"tel": "24 33402042R211", "row": {"tel":"24 33402042","ext":"FAX R211","obs":"IVETE CONTAS PAGAR"}})
de_para_telefones.append({"tel": "24 33402042212", "row": {"tel":"24 33402042","ext":"ALEX R212","obs":""}})
de_para_telefones.append({"tel": "18-3851-1035-018", "row": {"tel":"18 38511035","ext":"","obs":""}})
de_para_telefones.append({"tel": "11 56418111-221", "row": {"tel":"11 956418111","ext":"","obs":""}})
de_para_telefones.append({"tel": "911) 950059876", "row": {"tel":"11 950059876","ext":"","obs":""}})
de_para_telefones.append({"tel": "9110986277724", "row": {"tel":"11 986277724","ext":"","obs":""}})

de_para_telefones.append({"tel": "(51)998458-5032", "row": {"tel":"51 984585032","ext":"","obs":""}})
de_para_telefones.append({"tel": "(34)998891-2316", "row": {"tel":"34 988912316","ext":"","obs":""}})
de_para_telefones.append({"tel": "(31)998493-6167", "row": {"tel":"31 984936167","ext":"","obs":""}})
de_para_telefones.append({"tel": "(11)995830-1432", "row": {"tel":"11 958301432","ext":"","obs":""}})

de_para_telefones.append({"tel": "11 998141 8799", "row": {"tel":"11 981418799","ext":"","obs":""}})

de_para_telefones_dict = {
    item["tel"]: {
        "tel_para": item["row"]["tel"],
        "ext_para": item["row"]["ext"],
        "obs_para": item["row"]["obs"]
    }
    for item in de_para_telefones
}

# Funções

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def limpar_df(df):
    df = df.fillna("")
    df = df.replace('nan', '')
    df = df.astype(str)
    return df

def ler_arquivo(path, encoding='utf-8-sig'):    
    df = pd.read_csv(
                path,
                sep=";",           
                encoding=encoding, 
                dtype=str,         
            )
    
    df = limpar_df(df)    
    return df

def de_para(numero):        
    match numero:
                case '3525-0820/88858559': return '35250820|988858559' #sem ddd
                case '987908591/99328948': return '81987908591|81999328948' #sem ddd
                case '(11)3779-6672 (11)99548-1722': return '1137796672|11995481722'
                case '19 98104134832120629': return '19981041348|1932120629'
                case '(51) 9684-8414 / 3047-6467': return '51996848414|5130476467'
                case '(51) 3012-2618 / 9235-2618': return '5130122618|51992352618'
                case '(51) 8554-4240 / 3339-3653': return '51985544240|5133393653'
                case '81 34759882 987769231': return '8134759882|81987769231'
                case '(81)985706212 (81) 984329443': return '81985706212|81984329443'
                case '(81)992444025 (81)984393984': return '81992444025|81984393984'
                case '(21)973181206/(021)964788613': return '21973181206|21964788613'
                case '(71)981885972/981631315': return '71981885972|71981631315'
                case '(11) 2526-4900/ (41) 3353-4645': return '1125264900|4133534645'
                case '(84)991543494//994339444': return '84991543494|84994339444'
                case '(51)995277468/(51)999537900': return '51995277468|51999537900'
                case '(13)97401-8877/(13)99690-6930': return '13974018877|13996906930'
                case '(71)98144-1092/(71)3239-0717': return '71981441092|7132390717'
                case '(71)3307-1405 / (71)98714-5261': return '7133071405|71987145261'
                case '(62) 32866797/994998874': return '6232866797|62994998874'
                case '(62)3256-2075/98482-9553': return '6232562075|62984829553'
                case '(71)986824789 (71)981771346': return '71986824789|71981771346'

                case _: return 'Não Mapeada'
              
# Dataframes - Dados Fontes

df_fax = ler_arquivo("phonenumbers/src/tel_fax.csv")
df_fax.rename(columns={"tel_fmt":"tel_fax"}, inplace=True)

df_cep_ini = ler_arquivo("phonenumbers/src/cep_ddd_cli.csv")


