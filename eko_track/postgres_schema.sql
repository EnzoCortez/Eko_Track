-- Script de creación de esquema para PostgreSQL - Eko Track
-- Generado automáticamente basado en models.py

-- 1. Tabla de Usuarios
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 2. Tabla de Categorías de Reporte
CREATE TABLE report_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    base_priority INTEGER DEFAULT 1
);

-- 3. Tabla de Configuración Municipal
CREATE TABLE municipality_settings (
    id SERIAL PRIMARY KEY,
    total_budget FLOAT DEFAULT 0.0
);

-- 4. Tabla de Reportes
CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criticality VARCHAR(20) NOT NULL DEFAULT 'Bajo',
    estimated_cost FLOAT DEFAULT 0.0,
    allocated_budget FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'Pendiente',
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    location VARCHAR(50) NOT NULL DEFAULT 'Norte',
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "user" (id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES report_category (id)
);

-- DATOS INICIALES (SEED DATA)

-- Insertar Configuración Municipal (Presupuesto Inicial: $50,000)
INSERT INTO municipality_settings (total_budget) VALUES (50000.0);

-- Insertar Categorías de Reporte
INSERT INTO report_category (name, base_priority) VALUES 
('Residuos', 8),
('Agua', 10),
('Aire', 7),
('Ruido', 4);

-- Insertar Usuario Administrador
-- Usuario: admin
-- Contraseña: admin
-- Hash generado con scrypt (compatible con la app Flask)
INSERT INTO "user" (username, password, is_admin) VALUES 
('admin', 'scrypt:32768:8:1$Kjmp8cY00OTo6QUW$3763f350ba15378293180e6b47eb1134142102109f285745a4844fc06062a2ffad7253194229457426f62e952e585c23ec81b376c4ee7a886ccc29ea6310f48a', TRUE);

-- Fin del script
