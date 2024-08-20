/* Category Table */
-- Stores all categories info
CREATE TABLE categories (
    category_id CHAR(36) PRIMARY KEY, -- UUID for primary key
    category_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
/* Product Table */
-- Stores all products info
CREATE TABLE products (
    product_id CHAR(36) PRIMARY KEY, -- UUID for primary key
    product_name VARCHAR(100) NOT NULL,
    category_id CHAR(36),
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    product_image VARCHAR(255), -- Path to the product image
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);



