create table public.orion_contrato (
    id_contrato int4 null,
    cc_contrato int4 null,
    cg_nombre varchar(50) null,
    cg_ap_paterno varchar(50) null,
    cg_ap_materno varchar(50) null,
    cg_rfc varchar(50) null,
    df_nacimiento timestamp null,
    telefono varchar(50) null,
    cg_calle varchar(50) null,
    cg_colonia varchar(50) null,
    cg_ciudad varchar(50) null,
    cg_entidad varchar(50) null,
    cg_municipio varchar(50) null,
    cg_entre_calles varchar(50) null,
    monto_pago numeric(10,2) null,
    total_contrato numeric(10,2) null,
    num_pago_vencido int4 null,
    dias_vencido int4 null,
    nivel_riesgo varchar(1) null,
    ilocalizables varchar(2) null,
    ilocalizable_sistema varchar(2) null,
    band_rpc varchar(2) null,
    calificacion_cliente varchar(1) null,
    maximo_retraso int4 null,
    sucursal varchar(50) null,
    producto varchar(50) null,
    frecuencia_pago varchar(2) null,
    tipo_analisis varchar(6) null
);


create table public.orion_cliente(

	cc_deudor int4 null,
	cg_nombre varchar(50) null,
	cg_ap_paterno varchar(50) null,
	cg_ap_materno varchar(50) null,
	cg_rfc varchar(50) null,
	df_nacimiento varchar(50) null,
	telefono varchar(50) null,
	cg_calle varchar(50) null,
	cg_colonia varchar(50) null,
	cg_ciudad varchar(50) null,
	cg_entidad varchar(50) null,
	cg_municipio varchar(50) null,
	cg_entre_calles varchar(50) null 

);