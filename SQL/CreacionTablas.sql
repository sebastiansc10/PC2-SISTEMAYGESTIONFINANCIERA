drop table if exists Diario cascade;
CREATE TABLE Diario
(
  Fecha DATE NOT NULL,
  Glosa VARCHAR(200),
  ID_Diario SERIAL PRIMARY KEY
);

drop table if exists Elemento cascade;
CREATE TABLE Elemento
(
  ID_Elemento SERIAL PRIMARY KEY,
  Nombre_Elemento VARCHAR(50) NOT NULL
);

drop table if exists Cuenta cascade;
CREATE TABLE Cuenta
(
  ID_Cuenta INT PRIMARY KEY,
  Nombre_Cuenta VARCHAR(100) NOT NULL,
  ID_Elemento INT NOT NULL,
  FOREIGN KEY (ID_Elemento) REFERENCES Elemento(ID_Elemento)
);

drop table if exists Transaccion cascade;
CREATE TABLE Transaccion
(
  Cantidad NUMERIC(10, 2) NOT NULL,
  DH VARCHAR(5) NOT NULL CHECK (DH IN ('Debe', 'Haber')),
  ID_Transaccion SERIAL PRIMARY KEY,
  ID_Diario INT NOT NULL,
  ID_Cuenta INT NOT NULL,
  FOREIGN KEY (ID_Diario) REFERENCES Diario(ID_Diario),
  FOREIGN KEY (ID_Cuenta) REFERENCES Cuenta(ID_Cuenta)
);
