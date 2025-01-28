insert into elemento (ID_Elemento, Nombre_Elemento) values
(1, 'Activo corriente'),
(2, 'Activo corriente (existencias)'),
(3, 'Activo no corriente'),
(4, 'Pasivos'),
(5, 'Patrimonio'),
(6, 'Gastos'),
(7, 'Ingresos'),
(8, 'Cuenta de cierre'),
(9, 'Cuentas analíticas de explotación');


INSERT INTO Cuenta (ID_Cuenta, Nombre_Cuenta, ID_Elemento) VALUES
(10, 'Efectivo y equivalentes de efectivo', 1),
(11, 'Inversiones financieras', 1),
(12, 'Cuentas por cobrar comerciales –Terceros', 1),
(13, 'Cuentas por cobrar comerciales –Relacionadas', 1),
(14, 'Cuentas por cobrar al personal, a los accionistas (socios), directores y gerentes', 1),
(16, 'Cuentas por cobrar diversas –Terceros', 1),
(17, 'Cuentas por cobrar diversas –Relacionadas', 1),
(18, 'Servicios y otros contratados por anticipado', 1),
(20, 'Mercaderías', 2),
(21, 'Productos terminados', 2),
(22, 'Subproductos, desechos y desperdicios', 2),
(23, 'Productos en proceso', 2),
(24, 'Materias primas', 2),
(25, 'Materiales auxiliares, suministros y repuestos', 2),
(26, 'Envases y embalajes', 2),
(27, 'Activos no corrientes mantenidos para la venta', 2),
(28, 'Existencias por recibir', 2),
(29, 'Desvalorización de existencias', 2),
(30, 'Inversiones mobiliarias', 3),
(31, 'Inversiones inmobiliarias', 3),
(32, 'Activos adquiridos en arrendamiento financiero', 3),
(33, 'Inmuebles, maquinaria y equipo', 3),
(34, 'Intangibles', 3),
(35, 'Activos biológicos', 3),
(36, 'Desvalorización de activo inmovilizado', 3),
(37, 'Activo diferido', 3),
(38, 'Otros activos', 3),
(39, 'Depreciación, amortización y agotamiento acumulados', 3),
(40, 'Tributos y aportes al sistema de pensiones y de salud por pagar', 4),
(41, 'Remuneraciones y participaciones por pagar', 4),
(42, 'Cuentas por pagar comerciales – Terceros', 4),
(43, 'Cuentas por pagar comerciales – Relacionadas', 4),
(44, 'Cuentas por pagar a los accionistas, directores y gerentes', 4),
(45, 'Obligaciones financieras', 4),
(46, 'Cuentas por pagar diversas – Terceros', 4),
(47, 'Cuentas por pagar diversas – Relacionadas', 4),
(48, 'Provisiones', 4),
(49, 'Pasivo diferido', 4),
(50, 'Capital', 5),
(51, 'Acciones de inversión', 5),
(52, 'Capital adicional', 5),
(56, 'Resultados no realizados', 5),
(57, 'Excedente de revaluación', 5),
(58, 'Reservas', 5),
(60, 'Compras', 6),
(61, 'Variación de existencias', 6),
(62, 'Gastos de personal, directores y gerentes', 6),
(63, 'Gastos de servicios prestados por terceros', 6),
(64, 'Gastos por tributos', 6),
(65, 'Otros gastos de gestión', 6),
(66, 'Pérdida por medición de activos no financieros al valor razonable', 6),
(67, 'Gastos financieros', 6),
(68, 'Valuación y deterioro de activos y provisiones', 6),
(69, 'Costo de ventas', 6),
(70, 'Ventas', 7),
(71, 'Variación de la producción almacenada', 7),
(72, 'Producción de activo inmovilizado', 7),
(73, 'Descuentos, rebajas y bonificaciones obtenidos', 7),
(74, 'Descuentos, rebajas y bonificaciones concedidos', 7),
(75, 'Otros ingresos de gestión', 7),
(76, 'Ganancia por medición de activos no financieros al valor razonable', 7),
(77, 'Ingresos financieros', 7),
(78, 'Cargas cubiertas por provisiones', 7),
(79, 'Cargas imputables a cuentas de costos y gastos', 7),
(81, 'Producción del ejercicio', 8),
(82, 'Valor agregado', 8),
(83, 'Excedente bruto (insuficiencia bruta) de explotación', 8),
(84, 'Resultado de explotación', 8),
(85, 'Resultado antes de participaciones e impuestos', 8),
(87, 'Participaciones de los trabajadores', 8),
(88, 'Impuesto a la renta', 8),
(89, 'Determinación del resultado del ejercicio', 8),
(91, 'Costos por distribuir', 9),
(92, 'Costos de producción', 9),
(93, 'Centros de costos', 9),
(94, 'Gastos administrativos', 9),
(95, 'Gastos de ventas', 9),
(96, 'Gastos financieros', 9);





insert into diario (Fecha, glosa) values
('2025/01/27', 'Datos de prueba');


-- Insertar transacciones para el 27 de enero de 2025
INSERT INTO Transaccion (Cantidad, DH, ID_Diario, ID_Cuenta) VALUES
(100.00, 'Debe', 1, 10),  -- 100.00 en 'Debe' para la cuenta 10 (Efectivo y equivalentes de efectivo)
(100.00, 'Haber', 1, 50), -- 100.00 en 'Haber' para la cuenta 50 (Capital)

(200.00, 'Debe', 1, 11),  -- 200.00 en 'Debe' para la cuenta 11 (Inversiones financieras)
(200.00, 'Haber', 1, 30), -- 200.00 en 'Haber' para la cuenta 30 (Inversiones mobiliarias)

(150.00, 'Debe', 1, 20),  -- 150.00 en 'Debe' para la cuenta 20 (Mercaderías)
(150.00, 'Haber', 1, 40), -- 150.00 en 'Haber' para la cuenta 40 (Tributos por pagar)

(50.00, 'Debe', 1, 60),   -- 50.00 en 'Debe' para la cuenta 60 (Compras)
(50.00, 'Haber', 1, 70);  -- 50.00 en 'Haber' para la cuenta 70 (Ventas)

