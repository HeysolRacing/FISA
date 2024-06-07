def validar_gestion_map(row):
    contrato_dict = row.asDict()

    dias_vencido = contrato_dict["dias_vencido"]
    nivel_riesgo = contrato_dict["nivel_riesgo"]
    band_RPC = contrato_dict["band_rpc"]
    ilocalizables = contrato_dict["ilocalizables"]
    ilocalizable_sistema = contrato_dict["ilocalizable_sistema"]
    sucursal = contrato_dict["sucursal"]
    producto = contrato_dict["producto"]
    frecuencia_pago = contrato_dict["frecuencia_pago"]
    tipo_analisis = contrato_dict["tipo_analisis"]

    if 90 <= dias_vencido <= 179:
        contrato_dict["gestion"] = 'C001'
    elif 30 <= dias_vencido <= 59:
        contrato_dict["gestion"] = "C002"
    elif 60 <= dias_vencido <= 89:
        contrato_dict["gestion"] = "C004"
    elif 60 <= dias_vencido <= 89:
        contrato_dict["gestion"] = "C005"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "A":
        contrato_dict["gestion"] = "C006"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "M":
        contrato_dict["gestion"] = "C021"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "M":
        contrato_dict["gestion"] = "C022"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "M" and band_RPC >= 5:
        contrato_dict["gestion"] = "C023"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "M" and band_RPC >= 5:
        contrato_dict["gestion"] = "C024"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "B":
        contrato_dict["gestion"] = "C025"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "B":
        contrato_dict["gestion"] = "C026"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "B" and band_RPC >= 5:
        contrato_dict["gestion"] = "C027"
    elif 1 <= dias_vencido <= 29 and nivel_riesgo == "B" and band_RPC >= 5:
        contrato_dict["gestion"] = "C028"
    elif ilocalizables == "SI" or ilocalizable_sistema == "SI":
        contrato_dict["gestion"] = "C014"
    elif ilocalizables == "SI" or ilocalizable_sistema == "SI":
        contrato_dict["gestion"] = "C015"
    elif ilocalizables == "SI" or ilocalizable_sistema == "SI":
        contrato_dict["gestion"] = "C016"
    elif sucursal == 261 and 1 <= dias_vencido <= 89:
        contrato_dict["gestion"] = "C017"
    elif sucursal == 261 and 90 <= dias_vencido <= 179:
        contrato_dict["gestion"] = "C018"
    elif 90 <= dias_vencido <= 179 and producto == "FDIG":
        contrato_dict["gestion"] = "C048"
    elif 60 <= dias_vencido <= 89 and producto == "FDIG":
        contrato_dict["gestion"] = "C074"
    elif 30 <= dias_vencido <= 59 and producto == "FDIG":
        contrato_dict["gestion"] = "C073"
    elif 15 <= dias_vencido <= 29 and producto == "FDIG":
        contrato_dict["gestion"] = "C072"
    elif 1 <= dias_vencido <= 14 and producto == "FDIG":
        contrato_dict["gestion"] = "C071"
    elif 30 <= dias_vencido <= 89 and sucursal in [14, 16, 22] and producto in ["REDI", "REDF"]:
        contrato_dict["gestion"] = "C070"
    elif 1 <= dias_vencido <= 29 and sucursal in [14, 16, 22] and producto in ["REDI", "REDF"]:
        contrato_dict["gestion"] = "C032"
    elif 1 <= dias_vencido <= 179 and producto == "FTPE":
        contrato_dict["gestion"] = "C031"
    elif 1 <= dias_vencido <= 29 and sucursal in [261] and producto != "FDIG":
        contrato_dict["gestion"] = "C030"
    elif 1 <= dias_vencido <= 29 and sucursal in [261] and producto != "FDIG":
        contrato_dict["gestion"] = "C045"
    elif 30 <= dias_vencido <= 89 and producto == "FNCC" and sucursal == 261:
        contrato_dict["gestion"] = "C044"
    elif 1 <= dias_vencido <= 29 and producto == "FNCC" and sucursal == 0:
        contrato_dict["gestion"] = "C060"
    elif 30 <= dias_vencido <= 89 and producto == "FNCC" or sucursal == 0:
        contrato_dict["gestion"] = "C060"
    elif 1 <= dias_vencido <= 29 and producto == "FNCC" or sucursal == 0:
        contrato_dict["gestion"] = "C061"
    elif 1 <= dias_vencido <= 3 and frecuencia_pago != "S":
        contrato_dict["gestion"] = "C062"
    elif 1 <= dias_vencido <= 2 and frecuencia_pago == "S":
        contrato_dict["gestion"] = "C052"
    elif dias_vencido == 0 and sucursal in [14, 16, 22]:
        contrato_dict["gestion"] = "C051"
    elif -3 <= dias_vencido <= -1 and sucursal in [14, 16, 22] and producto in ["REDI", "REDF"]:
        contrato_dict["gestion"] = "C050"
    elif 90 <= dias_vencido <= 179 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C041"
    elif 60 <= dias_vencido <= 89 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C040"
    elif 30 <= dias_vencido <= 59 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C089"
    elif 15 <= dias_vencido <= 29 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C042"
    elif 1 <= dias_vencido <= 14 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C038"
    elif -30 <= dias_vencido <= 0 and producto in ["PYRE", "MNPN"] and tipo_analisis != "EXPR":
        contrato_dict["gestion"] = "C037"
    elif -30 <= dias_vencido <= 0 and producto in ["PYRE"] and tipo_analisis == "EXPR":
        contrato_dict["gestion"] = "C036"
    else:
        contrato_dict["gestion"] = ""

    return contrato_dict
