DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS prod_order;

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prod_order (
  oid INTEGER NOT NULL,
  pid INTEGER NOT NULL,
  FOREIGN KEY (oid) REFERENCES orders (id),
  FOREIGN KEY (pid) REFERENCES products (id)
);
